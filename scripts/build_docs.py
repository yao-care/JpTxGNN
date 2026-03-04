#!/usr/bin/env python3
"""將 Notes 轉換為 Jekyll 文件網站頁面"""

import json
import re
import shutil
from pathlib import Path


def fix_markdown_tables(content: str) -> str:
    """修復 Markdown 表格，確保表格前有空行（Kramdown 需要）"""
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        # 如果這行是表格開始（以 | 開頭）
        if line.strip().startswith('|') and i > 0:
            prev_line = lines[i - 1].strip()
            # 如果前一行不是空行且不是表格行（即表格開始處）
            if prev_line and not prev_line.startswith('|'):
                # 插入空行
                fixed_lines.append('')
        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def get_evidence_level(content: str) -> str:
    """從 markdown 內容提取最佳證據等級"""
    # v5 格式：從「快速總覽」表格提取
    # | 證據等級 | L2 (單一 RCT/多個 Phase 2) |
    v5_match = re.search(r'\|\s*證據等級\s*\|\s*(L[1-5])', content)
    if v5_match:
        return v5_match.group(1)

    # v4 格式：從「預測新適應症總覽」表格提取
    table_match = re.search(
        r'### 預測新適應症總覽.*?(?=\n---|\n##)',
        content,
        re.DOTALL
    )
    if table_match:
        table_content = table_match.group(0)
        levels = re.findall(r'\|\s*L([1-5])\s*\|', table_content)
        if levels:
            return f"L{min(int(l) for l in levels)}"
    return "L5"


def get_indication_count(content: str) -> int:
    """從 markdown 內容計算適應症數量"""
    # v5 格式：從「臨床試驗證據」表格計算行數
    if "## 臨床試驗證據" in content:
        # 計算試驗表格中的數據行（排除標題行）
        trials_match = re.search(
            r'## 臨床試驗證據.*?\n\|[^\n]+\n\|[-|\s]+\n(.*?)(?=\n##|\n$)',
            content,
            re.DOTALL
        )
        if trials_match:
            data_rows = [l for l in trials_match.group(1).strip().split('\n') if l.strip().startswith('|')]
            if data_rows:
                return 1  # v5 格式聚焦單一預測適應症

    # v4 格式：計算 "### 6.X" 模式的數量
    matches = re.findall(r'### 6\.\d+', content)
    return len(matches) if matches else 1


def get_drug_title(content: str) -> str:
    """從 markdown 內容提取藥物名稱"""
    # 尋找標題行
    match = re.search(r'^# .*?[—–-]\s*(\w+)', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Unknown"


def get_parent_by_evidence_level(evidence_level: str) -> str:
    """根據證據等級返回對應的 parent 頁面"""
    if evidence_level in ('L1', 'L2'):
        return '高證據等級 (L1-L2)'
    elif evidence_level in ('L3', 'L4'):
        return '中證據等級 (L3-L4)'
    else:  # L5
        return '僅模型預測 (L5)'


def convert_notes_to_jekyll():
    """轉換所有 notes 到 Jekyll _drugs 集合"""
    notes_dir = Path("data/notes")
    drugs_dir = Path("docs/_drugs")

    # 清空目標目錄
    if drugs_dir.exists():
        shutil.rmtree(drugs_dir)
    drugs_dir.mkdir(parents=True, exist_ok=True)

    drug_list = []
    nav_order = 10

    for drug_dir in sorted(notes_dir.iterdir()):
        if not drug_dir.is_dir() or drug_dir.name.startswith('.'):
            continue

        drug_name = drug_dir.name
        pharmacist_file = drug_dir / "drug_pharmacist_notes.md"
        sponsor_file = drug_dir / "drug_sponsor_notes.md"

        if not pharmacist_file.exists():
            print(f"⚠️  跳過 {drug_name}: 無藥師報告")
            continue

        # 讀取藥師報告
        pharmacist_content = pharmacist_file.read_text(encoding='utf-8')

        # 提取元資料
        drug_title = drug_name.replace('_', ' ').title()
        evidence_level = get_evidence_level(pharmacist_content)
        indication_count = get_indication_count(pharmacist_content)
        parent_page = get_parent_by_evidence_level(evidence_level)

        # 讀取贊助商報告（如果存在）
        sponsor_content = ""
        if sponsor_file.exists():
            sponsor_content = sponsor_file.read_text(encoding='utf-8')

        # 建立 Jekyll 頁面
        jekyll_content = f"""---
layout: default
title: {drug_title}
parent: {parent_page}
nav_order: {nav_order}
evidence_level: {evidence_level}
indication_count: {indication_count}
---

# {drug_title}
{{: .fs-9 }}

證據等級: **{evidence_level}** | 預測適應症: **{indication_count}** 個
{{: .fs-6 .fw-300 }}

---

## 目錄
{{: .no_toc .text-delta }}

1. TOC
{{:toc}}

---

<div id="pharmacist">

## 藥師評估報告

</div>

{pharmacist_content}

---

"""

        if sponsor_content:
            jekyll_content += f"""<div id="sponsor">

## 贊助商報告

</div>

{sponsor_content}
"""

        # 修復表格格式（確保表格前有空行）
        jekyll_content = fix_markdown_tables(jekyll_content)

        # 寫入檔案
        output_file = drugs_dir / f"{drug_name}.md"
        output_file.write_text(jekyll_content, encoding='utf-8')

        drug_list.append({
            'name': drug_name,
            'title': drug_title,
            'evidence_level': evidence_level,
            'indication_count': indication_count
        })

        print(f"✅ {drug_title} ({evidence_level}, {indication_count} 適應症)")
        nav_order += 1

    # 不再建立藥物列表頁面（由 nav-drugs.md 提供）
    # create_drug_list_page(drug_list)

    print(f"\n📊 總計轉換 {len(drug_list)} 個藥物")
    return drug_list


def create_drug_list_page(drug_list: list):
    """建立藥物總覽頁面（使用 Liquid 動態生成）"""
    content = """---
layout: default
title: 藥物總覽
nav_order: 5
---

# 藥物總覽
{: .fs-9 }

共 """ + str(len(drug_list)) + """ 個藥物的驗證報告
{: .fs-6 .fw-300 }

---

## 統計摘要

| 證據等級 | 藥物數 | 說明 |
|---------|--------|------|
"""
    # 按證據等級分組統計
    by_level = {}
    for drug in drug_list:
        level = drug['evidence_level']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(drug)

    level_desc = {
        'L1': '多個 RCT / 系統性回顧',
        'L2': '單一 RCT / Phase 2 試驗',
        'L3': '觀察性研究 / 大型病例系列',
        'L4': '前臨床 / 機轉研究',
        'L5': '僅模型預測'
    }

    for level in sorted(by_level.keys()):
        drugs = by_level[level]
        desc = level_desc.get(level, '')
        content += f"| **{level}** | {len(drugs)} | {desc} |\n"

    content += """
---

## 完整藥物列表

{% assign all_drugs = site.drugs | sort: 'title' %}

| 藥物名稱 | 證據等級 | 適應症數 |
|---------|---------|---------|
{% for drug in all_drugs %}| [{{ drug.title }}]({{ drug.url | relative_url }}) | {{ drug.evidence_level }} | {{ drug.indication_count }} |
{% endfor %}
"""

    Path("docs/drugs.md").write_text(content, encoding='utf-8')


def main():
    """主程式"""
    print("🚀 開始轉換 Notes 到 Jekyll 格式...\n")
    convert_notes_to_jekyll()
    print("\n✨ 完成！執行以下命令預覽：")
    print("   cd docs && bundle install && bundle exec jekyll serve")


if __name__ == "__main__":
    main()
