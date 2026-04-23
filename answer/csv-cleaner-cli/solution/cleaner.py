#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

# --- 清洗辅助函数 ---

def normalize_name(name: str) -> str:
    """将名字标准化：去除多余空格，并将首字母大写"""
    return " ".join(name.split()).title()

def email_valid(email: str) -> bool:
    """校验邮箱格式：必须包含@，且@前后都有内容，且域名中有点号"""
    if "@" not in email:
        return False
    local, domain = email.split("@", 1)
    return bool(local) and "." in domain

def parse_age(age_raw: str) -> str:
    """清洗年龄：去除空格，转换为整数，并限制在 0-120 岁之间"""
    age_raw = age_raw.strip()
    if age_raw == "": return ""
    try:
        age = int(age_raw)
    except ValueError:
        return ""
    return str(age) if 0 <= age <= 120 else ""

def parse_score(score_raw: str) -> str:
    """清洗分数：转换为浮点数，限制在 0-100，并保留两位小数"""
    score_raw = score_raw.strip()
    if score_raw == "": return ""
    try:
        score = float(score_raw)
    except ValueError:
        return ""
    if 0 <= score <= 100:
        return f"{score:.2f}"
    return ""

# --- 核心逻辑 ---

def clean_rows(input_path: Path) -> list[dict[str, str]]:
    """读取 CSV 并执行清洗逻辑"""
    cleaned = []
    seen_ids = set() # 用于跟踪已处理过的 ID，实现自动去重

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None: return cleaned

        # 去除表头中可能的空格
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            if row is None: continue

            # 对每一行的数据进行去空格处理
            normalized = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items()}

            # 如果整行都是空的，直接跳过
            if all(v == "" for v in normalized.values()): continue

            # --- ID 校验 ---
            raw_id = normalized.get("id", "")
            try:
                row_id = int(raw_id)
                if row_id <= 0: continue # ID 必须为正整数
            except ValueError:
                continue

            # ID 去重
            if row_id in seen_ids: continue

            # --- 邮箱校验 ---
            email = normalized.get("email", "").lower()
            if not email_valid(email): continue

            # 添加清洗后的数据到列表
            cleaned.append({
                "id": str(row_id),
                "name": normalize_name(normalized.get("name", "")),
                "email": email,
                "age": parse_age(normalized.get("age", "")),
                "score": parse_score(normalized.get("score", "")),
            })
            seen_ids.add(row_id)

    # 最后按 ID 从小到大排序
    cleaned.sort(key=lambda item: int(item["id"]))
    return cleaned

def write_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    """将处理后的数据写入新 CSV"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "age", "score"])
        writer.writeheader()
        writer.writerows(rows)

def main() -> None:
    """主入口：使用 argparse 解析命令行参数"""
    parser = argparse.ArgumentParser(description="Clean dirty CSV data")
    parser.add_argument("--input", required=True, help="Path to dirty CSV")
    parser.add_argument("--output", required=True, help="Path to cleaned CSV")
    args = parser.parse_args()

    # 执行清洗并写入
    rows = clean_rows(Path(args.input))
    write_rows(rows, Path(args.output))

if __name__ == "__main__":
    main()
