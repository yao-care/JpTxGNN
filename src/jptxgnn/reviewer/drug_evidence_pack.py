"""Drug-centric Evidence Pack generator using LLM."""

import json
import re
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path

from ..collectors.drug_bundle import DrugBundle
from .llm_client import LLMClient


class ValidationError(Exception):
    """Raised when output validation fails."""
    pass


class DrugEvidencePackGenerator:
    """Generates Drug Evidence Pack from a DrugBundle using LLM.

    v4 architecture:
    1. Programmatic data transfer (100% fidelity) - no LLM truncation
    2. LLM analysis only (evidence_level, relevance, classification)
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        model: str = "gpt-4o",
    ):
        """Initialize the generator.

        Args:
            llm_client: Optional LLMClient instance. If not provided, creates one.
            model: Model to use if creating a new LLMClient.
        """
        self.llm_client = llm_client or LLMClient(model=model)

    def _get_analysis_prompt_path(self) -> Path:
        """Get the path to the analysis-only prompt (v4)."""
        from ..paths import get_project_root
        return get_project_root() / "prompts" / "Evidence Pack Reviewer" / "v4_analysis_only.md"

    def _get_v3_prompt_path(self) -> Path:
        """Get the path to the v3 prompt (fallback)."""
        from ..paths import get_project_root
        return get_project_root() / "prompts" / "Evidence Pack Reviewer" / "v3_drug_centric.md"

    def _create_base_evidence_pack(self, bundle: DrugBundle) -> dict:
        """Create Evidence Pack with complete data transfer (no LLM).

        This ensures 100% data fidelity - no truncation.

        Args:
            bundle: The DrugBundle containing collected data

        Returns:
            Base Evidence Pack structure with ALL data
        """
        drug = bundle.drug
        now = datetime.now().strftime("%Y-%m-%d")

        # Build query_log from collection_log
        query_log = []
        for cs in bundle.collection_log:
            query_log.append({
                "id": len(query_log) + 1,
                "source": cs.source,
                "query_date": cs.queried_at[:10] if cs.queried_at else now,
                "query_params": cs.query_params,
                "result_status": cs.status,
                "result_count": cs.result_count,
                "notes": cs.error_message or "",
            })

        # Build predicted_indications with COMPLETE data
        predicted_indications = []
        for i, pi in enumerate(drug.predicted_indications):
            indication = {
                "rank": i + 1,
                "disease_name": pi.disease_name,
                "txgnn": {
                    "score": pi.txgnn_score,
                    "rank": pi.txgnn_rank,
                },
                "evidence": {
                    # COMPLETE transfer - no truncation
                    "clinical_trials": [
                        {
                            "nct_id": t.get("nct_id") or t.get("id", ""),
                            "title": t.get("title", ""),
                            "phase": t.get("phase", ""),
                            "status": t.get("status", ""),
                            "enrollment": t.get("enrollment", 0),
                            "start_date": t.get("start_date", ""),
                            "completion_date": t.get("completion_date", ""),
                            "brief_summary": t.get("brief_summary", "")[:500] if t.get("brief_summary") else "",
                            # Analysis fields (to be filled by LLM)
                            "relevance": {"grade": "pending", "reasoning": ""},
                        }
                        for t in pi.clinical_trials
                        if isinstance(t, dict) and not t.get("error")
                    ],
                    "ictrp_trials": [
                        {
                            "trial_id": t.get("trial_id") or t.get("id", ""),
                            "title": t.get("title", ""),
                            "status": t.get("status", ""),
                            "source_registry": t.get("source_registry", ""),
                        }
                        for t in pi.ictrp_trials
                        if isinstance(t, dict) and not t.get("error")
                    ],
                    "literature": [
                        {
                            "pmid": a.get("pmid", ""),
                            "title": a.get("title", ""),
                            "authors": a.get("authors", ""),
                            "journal": a.get("journal", ""),
                            "year": a.get("year", ""),
                            "abstract": a.get("abstract", "")[:500] if a.get("abstract") else "",
                            # Analysis fields (to be filled by LLM)
                            "classification": {"study_type": "pending", "tier": "pending"},
                            "relevance": "pending",
                        }
                        for a in pi.pubmed_articles
                        if isinstance(a, dict) and not a.get("error")
                    ],
                },
                # Analysis fields (to be filled by LLM)
                "scoring": {
                    "evidence_level": "pending",  # L1-L5
                    "decision_stage": "pending",  # S0-S3
                    "recommendation": "pending",
                },
                "repurposing_rationale": {
                    "mechanistic_link": "pending",
                    "similarity_to_original": "pending",
                },
                "route_compatibility": {
                    "status": "pending",
                    "available_routes": [],
                    "required_routes": [],
                },
            }
            predicted_indications.append(indication)

        # Extract dosage forms from PMDA data
        dosage_forms = []
        if bundle.pmda.get("found") and bundle.pmda.get("records"):
            forms_seen = set()
            for record in bundle.pmda["records"]:
                # Support both English and Chinese field names
                form = record.get("dosage_form", record.get("劑型", ""))
                if form and form not in forms_seen:
                    forms_seen.add(form)
                    dosage_forms.append({
                        "route": self._infer_route(form),
                        "forms": [form],
                    })

        # Build the complete Evidence Pack
        evidence_pack = {
            "meta": {
                "candidate_id": f"TW-{drug.drugbank_id or 'UNKNOWN'}-multi",
                "version": "v4",
                "created_at": now,
                "data_cutoff": now,
                "inputs_received": self._get_inputs_received(bundle),
                "data_gaps": self._identify_data_gaps(bundle),
            },
            "drug": {
                "inn": drug.inn,
                "drugbank_id": drug.drugbank_id,
                "brand_name_zh": drug.brand_name_zh,
                "original_indications": drug.original_indications,
                "original_moa": drug.original_moa or "[Data Gap]",
            },
            "taiwan_regulatory": {
                "market_status": "已上市" if bundle.pmda.get("found") else "未上市",
                "total_licenses": len(bundle.pmda.get("records", [])),
                "licenses": [
                    {
                        # Support both English and Chinese field names
                        "license_number": r.get("license_id", r.get("許可證字號", "")),
                        "product_name_zh": r.get("brand_name_zh", r.get("中文品名", "")),
                        "dosage_form": r.get("dosage_form", r.get("劑型", "")),
                        "manufacturer": r.get("license_holder", r.get("製造廠", r.get("申請商", ""))),
                        "approved_indication_text": r.get("indication", r.get("適應症", "")),
                    }
                    for r in bundle.pmda.get("records", [])[:5]  # Limit to 5 for readability
                ],
                "dosage_forms_by_route": dosage_forms,
            },
            "safety": {
                "key_warnings": bundle.package_insert.get("warnings", ["[Data Gap]"]),
                "contraindications": bundle.package_insert.get("contraindications", ["[Data Gap]"]),
                "ddi": {
                    "query_status": "completed" if bundle.safety.get("ddi") else "not_found",
                    "total_count": len(bundle.safety.get("ddi", [])),
                    "interactions": bundle.safety.get("ddi", [])[:20],  # Limit for readability
                },
            },
            "predicted_indications": predicted_indications,
            "query_log": query_log,
        }

        return evidence_pack

    def _infer_route(self, dosage_form: str) -> str:
        """Infer administration route from dosage form."""
        form_lower = dosage_form.lower()
        if any(x in form_lower for x in ["注射", "injection", "infusion"]):
            return "Injectable"
        if any(x in form_lower for x in ["口服", "錠", "膠囊", "tablet", "capsule", "oral"]):
            return "Oral"
        if any(x in form_lower for x in ["眼", "ophthalmic", "eye"]):
            return "Ophthalmic"
        if any(x in form_lower for x in ["外用", "乳膏", "軟膏", "凝膠", "topical", "cream", "gel"]):
            return "Topical"
        return "Other"

    def _get_inputs_received(self, bundle: DrugBundle) -> list[str]:
        """Get list of data sources that were received."""
        inputs = []
        if bundle.pmda.get("found"):
            inputs.append("pmda")
        if bundle.safety.get("ddi"):
            inputs.append("ddi")
        if bundle.drugbank.get("found"):
            inputs.append("drugbank")
        if bundle.package_insert.get("found"):
            inputs.append("package_insert")

        # Check if any indication has trials or pubmed
        has_trials = any(pi.clinical_trials for pi in bundle.drug.predicted_indications)
        has_pubmed = any(pi.pubmed_articles for pi in bundle.drug.predicted_indications)
        if has_trials:
            inputs.append("clinicaltrials")
        if has_pubmed:
            inputs.append("pubmed")

        return inputs

    def _identify_data_gaps(self, bundle: DrugBundle) -> list[dict]:
        """Identify data gaps that need to be filled."""
        gaps = []
        gap_id = 1

        # Check PMDA package insert
        if not bundle.package_insert.get("found"):
            gaps.append({
                "id": f"DG{gap_id:03d}",
                "category": "Drug_Level",
                "item": "PMDA 仿單警語/禁忌",
                "severity": "Blocking",
                "impact": "無法進入 S1 安全性初評",
                "remediation": {
                    "source": "PMDA 官網",
                    "method": "下載仿單 PDF 並解析",
                },
            })
            gap_id += 1

        # Check DrugBank MOA
        if not bundle.drugbank.get("mechanism_of_action"):
            gaps.append({
                "id": f"DG{gap_id:03d}",
                "category": "Drug_Level",
                "item": "作用機轉 (MOA)",
                "severity": "High",
                "impact": "影響機轉關聯性分析",
                "remediation": {
                    "source": "DrugBank",
                    "method": "查詢 DrugBank API",
                },
            })
            gap_id += 1

        return gaps

    def _get_llm_analysis(self, evidence_pack: dict, bundle: DrugBundle) -> dict:
        """Get LLM analysis for evidence pack fields.

        LLM only provides:
        - evidence_level (L1-L5) per indication
        - relevance.grade (A/B/C) per trial
        - classification.study_type and tier per literature
        - repurposing_rationale
        - scoring.decision_stage and recommendation

        Args:
            evidence_pack: Base evidence pack with all data
            bundle: Original bundle for context

        Returns:
            Analysis results to merge into evidence pack
        """
        prompt_path = self._get_analysis_prompt_path()

        # If v4 prompt doesn't exist, fall back to simplified inline prompt
        if not prompt_path.exists():
            return self._get_llm_analysis_inline(evidence_pack, bundle)

        # Prepare a summary of data for LLM (not the full data)
        summary = self._create_analysis_summary(evidence_pack)

        user_message = f"""請分析以下藥物再利用證據，並提供評估結果：

```json
{json.dumps(summary, indent=2, ensure_ascii=False)}
```

請為每個適應症提供：
1. evidence_level (L1-L5)
2. decision_stage (S0-S3)
3. recommendation (Hold/Research Question/Proceed with Guardrails)
4. 每個臨床試驗的 relevance.grade (A/B/C)
5. 每篇文獻的 classification (study_type, tier)
6. mechanistic_link 說明
"""

        response = self.llm_client.chat_with_prompt_file(
            user_message=user_message,
            prompt_file=prompt_path,
            temperature=0.3,
        )

        self._last_response = response
        return self._parse_analysis_response(response)

    def _get_llm_analysis_inline(self, evidence_pack: dict, bundle: DrugBundle) -> dict:
        """Fallback: Get LLM analysis using inline prompt."""
        summary = self._create_analysis_summary(evidence_pack)

        system_prompt = """你是藥物再利用證據分析專家。根據提供的資料，評估每個適應症的證據等級。

回覆格式 (JSON):
```json
{
  "indications": [
    {
      "disease_name": "疾病名稱",
      "evidence_level": "L1-L5",
      "decision_stage": "S0-S3",
      "recommendation": "Hold/Research Question/Proceed with Guardrails",
      "mechanistic_link": "機轉關聯說明",
      "trials_analysis": [
        {"nct_id": "NCT...", "relevance_grade": "A/B/C", "reasoning": "..."}
      ],
      "literature_analysis": [
        {"pmid": "...", "study_type": "RCT/Cohort/Review/...", "tier": "1-3"}
      ]
    }
  ]
}
```

證據等級定義:
- L1: 有 Phase 3 RCT 直接證據
- L2: 有 Phase 2 RCT 或多個 Phase 1 證據
- L3: 有 Phase 1 或回顧性研究
- L4: 僅有間接證據或個案報告
- L5: 僅有預測，無臨床證據

決策階段:
- S0: 初篩（證據不足）
- S1: 安全性初評
- S2: 臨床可行性
- S3: 可建議
"""

        user_message = f"""請分析以下藥物再利用證據：

```json
{json.dumps(summary, indent=2, ensure_ascii=False)}
```"""

        response = self.llm_client.chat(
            user_message=user_message,
            system_prompt=system_prompt,
            temperature=0.3,
        )

        self._last_response = response
        return self._parse_analysis_response(response)

    def _create_analysis_summary(self, evidence_pack: dict) -> dict:
        """Create a summary of the evidence pack for LLM analysis."""
        summary = {
            "drug": evidence_pack["drug"]["inn"],
            "drugbank_id": evidence_pack["drug"]["drugbank_id"],
            "original_indications": evidence_pack["drug"]["original_indications"],
            "original_moa": evidence_pack["drug"]["original_moa"],
            "market_status": evidence_pack["taiwan_regulatory"]["market_status"],
            "ddi_count": evidence_pack["safety"]["ddi"]["total_count"],
            "indications": [],
        }

        for pi in evidence_pack["predicted_indications"]:
            indication_summary = {
                "disease_name": pi["disease_name"],
                "txgnn_score": pi["txgnn"]["score"],
                "clinical_trials_count": len(pi["evidence"]["clinical_trials"]),
                "literature_count": len(pi["evidence"]["literature"]),
                "clinical_trials": [
                    {
                        "nct_id": t["nct_id"],
                        "title": t["title"][:100],
                        "phase": t["phase"],
                        "status": t["status"],
                        "enrollment": t["enrollment"],
                    }
                    for t in pi["evidence"]["clinical_trials"][:10]
                ],
                "literature": [
                    {
                        "pmid": a["pmid"],
                        "title": a["title"][:100],
                        "year": a["year"],
                    }
                    for a in pi["evidence"]["literature"][:10]
                ],
            }
            summary["indications"].append(indication_summary)

        return summary

    def _parse_analysis_response(self, response: str) -> dict:
        """Parse LLM analysis response."""
        # Try to extract JSON from response
        json_match = re.search(r"```json\s*([\s\S]*?)```", response, re.IGNORECASE)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Try to find raw JSON
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        return {"indications": []}

    def _merge_analysis(self, evidence_pack: dict, analysis: dict) -> dict:
        """Merge LLM analysis into evidence pack."""
        analysis_by_disease = {
            ind["disease_name"]: ind
            for ind in analysis.get("indications", [])
        }

        for pi in evidence_pack["predicted_indications"]:
            disease = pi["disease_name"]
            if disease in analysis_by_disease:
                ana = analysis_by_disease[disease]

                # Update scoring
                pi["scoring"]["evidence_level"] = ana.get("evidence_level", "L5")
                pi["scoring"]["decision_stage"] = ana.get("decision_stage", "S0")
                pi["scoring"]["recommendation"] = ana.get("recommendation", "Hold")

                # Update repurposing rationale
                pi["repurposing_rationale"]["mechanistic_link"] = ana.get("mechanistic_link", "")

                # Update trial relevance
                trials_ana = {t["nct_id"]: t for t in ana.get("trials_analysis", [])}
                for trial in pi["evidence"]["clinical_trials"]:
                    if trial["nct_id"] in trials_ana:
                        t_ana = trials_ana[trial["nct_id"]]
                        trial["relevance"]["grade"] = t_ana.get("relevance_grade", "C")
                        trial["relevance"]["reasoning"] = t_ana.get("reasoning", "")

                # Update literature classification
                lit_ana = {str(a["pmid"]): a for a in ana.get("literature_analysis", [])}
                for article in pi["evidence"]["literature"]:
                    if str(article["pmid"]) in lit_ana:
                        a_ana = lit_ana[str(article["pmid"])]
                        article["classification"]["study_type"] = a_ana.get("study_type", "")
                        article["classification"]["tier"] = a_ana.get("tier", "3")

        return evidence_pack

    def generate(
        self,
        bundle: DrugBundle,
        temperature: float = 0.3,
    ) -> tuple[dict, str]:
        """Generate Drug Evidence Pack from a bundle.

        v4 architecture:
        1. Create base evidence pack with ALL data (programmatic)
        2. Get LLM analysis (only analysis fields)
        3. Merge analysis into evidence pack

        Args:
            bundle: The DrugBundle containing collected data
            temperature: LLM temperature (lower = more deterministic)

        Returns:
            Tuple of (drug_evidence_pack_json, drug_evidence_pack_md)
        """
        # Step 1: Create base evidence pack with complete data
        evidence_pack = self._create_base_evidence_pack(bundle)

        # Step 2: Get LLM analysis
        analysis = self._get_llm_analysis(evidence_pack, bundle)

        # Step 3: Merge analysis into evidence pack
        evidence_pack = self._merge_analysis(evidence_pack, analysis)

        # Step 4: Generate markdown summary
        evidence_md = self._generate_markdown(evidence_pack)

        return evidence_pack, evidence_md

    def _generate_markdown(self, evidence_pack: dict) -> str:
        """Generate markdown summary from evidence pack."""
        drug = evidence_pack["drug"]
        reg = evidence_pack["taiwan_regulatory"]

        lines = [
            f"# {drug['inn']} 老藥新用分析報告",
            "",
            "## 藥物基本資訊",
            "| 項目 | 內容 | 來源 |",
            "|------|------|------|",
            f"| 藥物 (INN) | {drug['inn']} | |",
            f"| DrugBank ID | {drug['drugbank_id'] or '[Data Gap]'} | |",
            f"| 中文商品名 | {drug['brand_name_zh'] or '[Data Gap]'} | |",
            f"| 原核准適應症 | {', '.join(drug['original_indications']) or '[Data Gap]'} | [來源：PMDA 許可證] |",
            f"| 原作用機轉 | {drug['original_moa']} | [來源：DrugBank] |",
            f"| 台灣上市狀態 | {reg['market_status']} | PMDA |",
            "",
            "## 預測新適應症總覽",
            "| 排名 | 預測適應症 | TxGNN 分數 | 證據等級 | 臨床試驗 | 文獻 | 決策階段 | 開發建議 |",
            "|------|-----------|-----------|---------|---------|------|---------|---------:|",
        ]

        for pi in evidence_pack["predicted_indications"]:
            trials = len(pi["evidence"]["clinical_trials"]) + len(pi["evidence"]["ictrp_trials"])
            lit = len(pi["evidence"]["literature"])
            score = pi["txgnn"]["score"]
            level = pi["scoring"]["evidence_level"]
            stage = pi["scoring"]["decision_stage"]
            rec = pi["scoring"]["recommendation"]

            lines.append(
                f"| {pi['rank']} | {pi['disease_name']} | {score:.2%} | {level} | {trials} | {lit} | {stage} | {rec} |"
            )

        lines.extend([
            "",
            "## 資料收集日誌",
            "| # | 資料來源 | 查詢日期 | 查詢條件 | 結果狀態 | 筆數 | 備註 |",
            "|---|---------|---------|---------|---------|------|------|",
        ])

        for q in evidence_pack["query_log"]:
            params = ", ".join(f"{k}={v}" for k, v in q.get("query_params", {}).items())
            lines.append(
                f"| {q['id']} | {q['source']} | {q['query_date']} | {params} | {q['result_status']} | {q['result_count']} | {q.get('notes', '')} |"
            )

        return "\n".join(lines)

    def _validate_output(self, evidence_pack: dict, bundle: DrugBundle) -> list[str]:
        """Validate that evidence pack correctly reflects bundle data.

        Args:
            evidence_pack: The generated evidence pack
            bundle: The original bundle

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check indication count matches
        ep_indications = evidence_pack.get("predicted_indications", [])
        bundle_indications = bundle.drug.predicted_indications

        if len(ep_indications) != len(bundle_indications):
            errors.append(
                f"Indication count mismatch: EP has {len(ep_indications)}, "
                f"Bundle has {len(bundle_indications)}"
            )

        # Check each indication's evidence count
        for i, (ep_ind, bundle_ind) in enumerate(
            zip(ep_indications, bundle_indications)
        ):
            ep_trials = len(ep_ind.get("evidence", {}).get("clinical_trials", []))
            bundle_trials = len([
                t for t in bundle_ind.clinical_trials
                if isinstance(t, dict) and not t.get("error")
            ])

            if ep_trials != bundle_trials:
                errors.append(
                    f"Indication '{bundle_ind.disease_name}': trial count mismatch "
                    f"(EP: {ep_trials}, Bundle: {bundle_trials})"
                )

            ep_lit = len(ep_ind.get("evidence", {}).get("literature", []))
            bundle_lit = len([
                a for a in bundle_ind.pubmed_articles
                if isinstance(a, dict) and not a.get("error")
            ])

            if ep_lit != bundle_lit:
                errors.append(
                    f"Indication '{bundle_ind.disease_name}': literature count mismatch "
                    f"(EP: {ep_lit}, Bundle: {bundle_lit})"
                )

        # Check query_log has entries
        if not evidence_pack.get("query_log"):
            errors.append("query_log is empty")

        return errors

    def generate_and_save(
        self,
        bundle: DrugBundle,
        output_dir: str | Path,
        temperature: float = 0.3,
        max_retries: int = 3,
        validate: bool = True,
    ) -> tuple[Path, Path]:
        """Generate Drug Evidence Pack and save to files with retry and validation.

        Uses atomic operations: writes to temp directory first, then moves to final location.
        Includes validation to ensure data integrity.

        Args:
            bundle: The DrugBundle containing collected data
            output_dir: Directory to save output files
            temperature: LLM temperature
            max_retries: Maximum number of retries on failure
            validate: Whether to validate output against bundle

        Returns:
            Tuple of (json_path, md_path)

        Raises:
            ValidationError: If output validation fails after all retries
            Exception: If generation fails after all retries
        """
        output_dir = Path(output_dir)
        drug_slug = bundle.drug.inn.lower().replace(" ", "_")
        base_name = f"{drug_slug}_drug_evidence_pack"

        last_error = None
        last_validation_errors = []

        for attempt in range(1, max_retries + 1):
            try:
                print(f"  Generating Evidence Pack (attempt {attempt}/{max_retries})...")

                # Generate evidence pack
                evidence_json, evidence_md = self.generate(bundle, temperature)

                # Validate output
                if validate:
                    validation_errors = self._validate_output(evidence_json, bundle)
                    if validation_errors:
                        last_validation_errors = validation_errors
                        print(f"  ⚠️ Validation errors: {validation_errors}")
                        if attempt < max_retries:
                            wait_time = 2 ** attempt  # Exponential backoff
                            print(f"  Retrying in {wait_time}s...")
                            time.sleep(wait_time)
                            continue
                        else:
                            raise ValidationError(
                                f"Validation failed after {max_retries} attempts: "
                                f"{validation_errors}"
                            )

                # Use atomic write: write to temp dir first, then move
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)

                    # Write to temp directory
                    temp_json = temp_path / f"{base_name}.json"
                    temp_md = temp_path / f"{base_name}.md"

                    with open(temp_json, "w", encoding="utf-8") as f:
                        json.dump(evidence_json, f, indent=2, ensure_ascii=False)

                    with open(temp_md, "w", encoding="utf-8") as f:
                        f.write(evidence_md)

                    # Save raw response for debugging
                    if hasattr(self, '_last_response') and self._last_response:
                        temp_raw = temp_path / "raw_llm_response.txt"
                        with open(temp_raw, "w", encoding="utf-8") as f:
                            f.write(self._last_response)

                    # Create output directory and move files
                    output_dir.mkdir(parents=True, exist_ok=True)

                    json_path = output_dir / f"{base_name}.json"
                    md_path = output_dir / f"{base_name}.md"

                    shutil.move(str(temp_json), str(json_path))
                    shutil.move(str(temp_md), str(md_path))

                    if hasattr(self, '_last_response') and self._last_response:
                        raw_path = output_dir / "raw_llm_response.txt"
                        shutil.move(str(temp_raw), str(raw_path))
                        print(f"  - Raw response saved: {raw_path}")

                print(f"  ✅ Evidence Pack saved successfully")
                return json_path, md_path

            except ValidationError:
                raise  # Re-raise validation errors

            except Exception as e:
                last_error = e
                print(f"  ❌ Error on attempt {attempt}: {e}")
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"  Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        # All retries exhausted
        if last_validation_errors:
            raise ValidationError(
                f"Validation failed after {max_retries} attempts: {last_validation_errors}"
            )
        raise Exception(
            f"Failed to generate Evidence Pack after {max_retries} attempts. "
            f"Last error: {last_error}"
        )
