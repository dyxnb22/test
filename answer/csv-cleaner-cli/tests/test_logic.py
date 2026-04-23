#!/usr/bin/env python3
import csv
from pathlib import Path

# --- 辅助函数：读取 CSV ---
def read_csv(path: Path) -> list[dict[str, str]]:
    """以列表形式读取 CSV 内容，列表中的每一项都是一个字典"""
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

# --- 主测试逻辑 ---
def main() -> int:
    # 动态定位项目根目录，确保脚本在不同位置执行都能找到文件
    root = Path(__file__).resolve().parent.parent
    output_file = root / "solution" / "cleaned_data.csv"

    # 1. 检查文件是否存在：如果上一步的清洗脚本没运行或失败了，这里直接报错
    if not output_file.exists():
        print("FAIL: cleaned_data.csv was not generated")
        return 1

    # 2. 读取结果并定义“预期正确的结果”
    rows = read_csv(output_file)
    expected = [
        {"id": "1", "name": "Alice Smith", "email": "alice@example.com", "age": "30", "score": "88.46"},
        {"id": "4", "name": "Dora", "email": "dora@example.com", "age": "", "score": ""},
        {"id": "5", "name": "Frank", "email": "frank@example.com", "age": "", "score": "60.10"},
        {"id": "6", "name": "Grace Hopper", "email": "grace@example.com", "age": "85", "score": "100.00"},
    ]

    # 3. 比对：将实际读取的结果与期望结果进行深度对比
    if rows != expected:
        print("FAIL: cleaned output mismatch")
        print("Expected:", expected)
        print("Actual:", rows)
        return 1  # 失败时返回非0退出码，通知调用者测试未通过

    # 4. 全部通过
    print("PASS")
    return 0

if __name__ == "__main__":
    # 使用 SystemExit 将 main 函数的返回值转化为程序的退出状态码
    raise SystemExit(main())
