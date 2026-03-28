#!/usr/bin/env python3
"""RxNorm 橋接模組

使用 RxNorm API 取得藥物同義詞，提高成分映射成功率。
RxNorm 是美國國家醫學圖書館維護的標準化藥物術語系統。

API 文件：https://lhncbc.nlm.nih.gov/RxNav/APIs/
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import requests

logger = logging.getLogger(__name__)

# RxNorm API 基礎 URL
RXNORM_BASE_URL = "https://rxnav.nlm.nih.gov/REST"

# 快取檔案路徑
CACHE_FILE = Path(__file__).parent.parent.parent.parent / "data" / "external" / "rxnorm_cache.json"


class RxNormBridge:
    """RxNorm API 橋接器

    使用 RxNorm API 查詢藥物同義詞，並快取結果以避免重複請求。
    """

    def __init__(self, cache_file: Optional[Path] = None):
        """初始化橋接器

        Args:
            cache_file: 快取檔案路徑，預設為 data/external/rxnorm_cache.json
        """
        self.cache_file = cache_file or CACHE_FILE
        self.cache: Dict[str, dict] = {}
        self._load_cache()
        self.request_count = 0
        self.last_request_time = 0.0

    def _load_cache(self):
        """載入快取"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                logger.info(f"Loaded {len(self.cache)} cached RxNorm entries")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cache: {e}")
                self.cache = {}

    def _save_cache(self):
        """儲存快取"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _rate_limit(self):
        """速率限制（每秒最多 20 請求）"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < 0.05:  # 50ms 間隔
            time.sleep(0.05 - elapsed)
        self.last_request_time = time.time()

    def _api_request(self, endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
        """發送 API 請求

        Args:
            endpoint: API 端點（相對於基礎 URL）
            params: 查詢參數

        Returns:
            JSON 回應，若失敗則回傳 None
        """
        self._rate_limit()
        url = f"{RXNORM_BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            self.request_count += 1

            if response.status_code == 200:
                return response.json()
            else:
                logger.debug(f"API request failed: {response.status_code}")
                return None
        except requests.RequestException as e:
            logger.warning(f"API request error: {e}")
            return None

    def get_rxcui(self, name: str) -> Optional[str]:
        """根據藥物名稱取得 RxCUI

        Args:
            name: 藥物名稱

        Returns:
            RxCUI 字串，若找不到則回傳 None
        """
        name_upper = name.upper().strip()

        # 檢查快取
        cache_key = f"rxcui:{name_upper}"
        if cache_key in self.cache:
            return self.cache[cache_key].get("rxcui")

        # 查詢 API
        result = self._api_request("rxcui.json", {"name": name, "search": 2})

        rxcui = None
        if result:
            id_group = result.get("idGroup", {})
            rxnorm_id = id_group.get("rxnormId")
            if rxnorm_id:
                rxcui = rxnorm_id[0] if isinstance(rxnorm_id, list) else rxnorm_id

        # 儲存到快取
        self.cache[cache_key] = {"rxcui": rxcui, "name": name_upper}
        return rxcui

    def get_synonyms(self, rxcui: str) -> List[str]:
        """取得 RxCUI 的所有同義詞

        Args:
            rxcui: RxCUI 識別碼

        Returns:
            同義詞列表
        """
        # 檢查快取
        cache_key = f"synonyms:{rxcui}"
        if cache_key in self.cache:
            return self.cache[cache_key].get("synonyms", [])

        synonyms = set()

        # 方法 1：取得所有相關概念
        result = self._api_request(f"rxcui/{rxcui}/allrelated.json")
        if result:
            all_related = result.get("allRelatedGroup", {})
            concept_groups = all_related.get("conceptGroup", [])
            for group in concept_groups:
                concept_props = group.get("conceptProperties", [])
                for prop in concept_props:
                    name = prop.get("name", "").upper()
                    if name:
                        synonyms.add(name)

        # 方法 2：取得藥物屬性（包含同義詞）
        result = self._api_request(f"rxcui/{rxcui}/properties.json")
        if result:
            props = result.get("properties", {})
            name = props.get("name", "").upper()
            if name:
                synonyms.add(name)
            synonym_str = props.get("synonym", "")
            if synonym_str:
                for syn in synonym_str.split(";"):
                    syn = syn.strip().upper()
                    if syn:
                        synonyms.add(syn)

        synonyms_list = list(synonyms)

        # 儲存到快取
        self.cache[cache_key] = {"synonyms": synonyms_list}
        return synonyms_list

    def get_ingredients(self, rxcui: str) -> List[Tuple[str, str]]:
        """取得藥物的活性成分

        Args:
            rxcui: RxCUI 識別碼

        Returns:
            成分列表，每個元素為 (rxcui, name) 元組
        """
        # 檢查快取
        cache_key = f"ingredients:{rxcui}"
        if cache_key in self.cache:
            return self.cache[cache_key].get("ingredients", [])

        ingredients = []

        # 取得成分關係（tty=IN 表示 Ingredient）
        result = self._api_request(f"rxcui/{rxcui}/related.json", {"tty": "IN"})
        if result:
            related_group = result.get("relatedGroup", {})
            concept_groups = related_group.get("conceptGroup", [])
            for group in concept_groups:
                concept_props = group.get("conceptProperties", [])
                for prop in concept_props:
                    ing_rxcui = prop.get("rxcui", "")
                    ing_name = prop.get("name", "").upper()
                    if ing_rxcui and ing_name:
                        ingredients.append((ing_rxcui, ing_name))

        # 儲存到快取
        self.cache[cache_key] = {"ingredients": ingredients}
        return ingredients

    def find_drugbank_candidates(self, name: str) -> List[str]:
        """透過 RxNorm 尋找可能的 DrugBank 映射候選名稱

        Args:
            name: 原始成分名稱

        Returns:
            可能的 DrugBank 名稱候選列表
        """
        candidates = set()
        name_upper = name.upper().strip()

        # 1. 取得 RxCUI
        rxcui = self.get_rxcui(name_upper)
        if not rxcui:
            # 嘗試移除常見後綴後再查詢
            simplified = name_upper
            suffixes = [" HCL", " HYDROCHLORIDE", " SODIUM", " POTASSIUM",
                       " SULFATE", " MALEATE", " ACETATE", " CITRATE"]
            for suffix in suffixes:
                if simplified.endswith(suffix):
                    simplified = simplified[:-len(suffix)].strip()
                    break
            if simplified != name_upper:
                rxcui = self.get_rxcui(simplified)

        if not rxcui:
            return []

        # 2. 取得同義詞
        synonyms = self.get_synonyms(rxcui)
        candidates.update(synonyms)

        # 3. 取得成分資訊
        ingredients = self.get_ingredients(rxcui)
        for _, ing_name in ingredients:
            candidates.add(ing_name)
            # 也取得成分的同義詞
            ing_rxcui = self.get_rxcui(ing_name)
            if ing_rxcui:
                ing_synonyms = self.get_synonyms(ing_rxcui)
                candidates.update(ing_synonyms)

        # 移除原始名稱
        candidates.discard(name_upper)

        return list(candidates)

    def save(self):
        """儲存快取到檔案"""
        self._save_cache()
        logger.info(f"Saved {len(self.cache)} RxNorm cache entries")


def build_rxnorm_synonym_map(
    unmapped_ingredients: List[str],
    drugbank_names: Set[str],
    max_queries: int = 500,
) -> Dict[str, str]:
    """為未映射成分建立 RxNorm 同義詞對照表

    Args:
        unmapped_ingredients: 未映射的成分名稱列表
        drugbank_names: DrugBank 中所有藥物名稱（大寫）
        max_queries: 最大 API 查詢次數

    Returns:
        同義詞對照字典 {原始成分: DrugBank 名稱}
    """
    bridge = RxNormBridge()
    synonym_map = {}
    queries = 0

    logger.info(f"Building RxNorm synonym map for {len(unmapped_ingredients)} ingredients")

    for ingredient in unmapped_ingredients:
        if queries >= max_queries:
            logger.info(f"Reached max queries limit ({max_queries})")
            break

        ingredient_upper = ingredient.upper().strip()

        # 跳過已知無法映射的類型（中草藥、萃取物等）
        skip_patterns = ["EXTRACT", "POWDER", "OIL", "TINCTURE", "DRIED",
                        "TOXOID", "VACCINE", "ANTIGEN", "RADIX", "HERBA"]
        if any(pattern in ingredient_upper for pattern in skip_patterns):
            continue

        # 查詢 RxNorm
        candidates = bridge.find_drugbank_candidates(ingredient_upper)
        queries += 1

        # 找出與 DrugBank 匹配的候選
        for candidate in candidates:
            if candidate in drugbank_names:
                synonym_map[ingredient_upper] = candidate
                logger.debug(f"Found mapping: {ingredient_upper} -> {candidate}")
                break

        # 每 50 次查詢儲存一次快取
        if queries % 50 == 0:
            bridge.save()
            logger.info(f"Processed {queries} queries, found {len(synonym_map)} mappings")

    # 最終儲存
    bridge.save()
    logger.info(f"Completed: {queries} queries, {len(synonym_map)} new mappings")

    return synonym_map


if __name__ == "__main__":
    # 測試範例
    logging.basicConfig(level=logging.INFO)

    bridge = RxNormBridge()

    # 測試幾個成分
    test_names = [
        "THIAMINE DISULFIDE",
        "SILYMARIN",
        "CARBOCYSTEINE",
        "CEPHRADINE",
        "KETOROLAC TROMETHAMINE",
    ]

    for name in test_names:
        print(f"\n=== {name} ===")
        rxcui = bridge.get_rxcui(name)
        print(f"RxCUI: {rxcui}")

        if rxcui:
            candidates = bridge.find_drugbank_candidates(name)
            print(f"Candidates: {candidates[:10]}")  # 只顯示前 10 個

    bridge.save()
