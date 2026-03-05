import glob
import os
from collections import Counter

def analyze_files():
    file_pattern = "tmppartition_freight_*_*_paper.netl_*"
    files = glob.glob(file_pattern)

    output_lines = []

    if not files:
        output_lines.append("未在當前目錄找到符合格式的檔案。")
    else:
        header = f"{'檔案名稱':<150} | {'出現最多次 (字串, 次數)':<25} | {'出現最少次 (字串, 次數)':<25}"
        output_lines.append(header)
        output_lines.append("-" * 210)

        for filename in sorted(files):
            if not (filename.endswith("512") or filename.endswith("1024") or filename.endswith("1536") or filename.endswith("2048") or filename.endswith("2560")):
                continue

            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]

                    if not lines:
                        output_lines.append(f"{filename:<150} | {'(檔案空白)':<25} | {'(檔案空白)':<25}")
                        continue

                    counter = Counter(lines)
                    most_common = counter.most_common(1)[0]
                    least_common = counter.most_common()[-1]

                    output_lines.append(f"{filename:<150} | {str(most_common):<25} | {str(least_common):<25}")

            except Exception as e:
                output_lines.append(f"讀取檔案 {filename} 時發生錯誤: {e}")

    output_path = "analysis_result.txt"
    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(output_lines) + "\n")

    print(f"結果已寫入：{output_path}")

if __name__ == "__main__":
    analyze_files()