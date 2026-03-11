import glob
import os
from collections import Counter

def analyze_files_in_folder(folder_path):
    """
    分析資料夾內以 imb_1, imb_3, imb_100 結尾的檔案。
    """
    # 檔案過濾規則：更新為 imb 系列
    file_pattern = os.path.join(folder_path, "tmppartition_freight_*.netl_*")
    valid_suffixes = ("imb_1", "imb_3", "imb_100")
    
    # 取得符合格式且結尾正確的檔案
    files = [f for f in glob.glob(file_pattern) if f.endswith(valid_suffixes)]
    folder_results = []

    folder_results.append(f"=== 資料夾分析報告: {folder_path} ===")
    
    if not files:
        folder_results.append("未找到符合 imb_1, imb_3, imb_100 結尾的檔案。")
        return folder_results

    # 建立表格標頭
    header = f"{'file name':<60} | {'出現最多次 (字串, 次數)':<50} | {'出現最少次 (字串, 次數)':<50}"
    folder_results.append(header)
    folder_results.append("-" * 170)

    for filename in sorted(files):
        try:
            # 使用生成器逐行讀取，避免記憶體溢位
            with open(filename, 'r', encoding='utf-8') as f:
                counter = Counter(line.strip() for line in f if line.strip())

            if not counter:
                folder_results.append(f"{os.path.basename(filename):<60} | {'(file is empty)':<50} | {'(file is empty)':<50}")
                continue

            # 取得排序後的統計資料
            all_counts = counter.most_common()
            
            # --- 處理出現最多次 (支援並列) ---
            max_freq = all_counts[0][1]
            most_items = [item for item, count in all_counts if count == max_freq]
            # 格式化顯示：若超過 2 個就顯示數量
            most_display = f"{most_items[0]}" if len(most_items) == 1 else f"{tuple(most_items[:2])}..etc{len(most_items)}種"
            most_final = f"{most_display} ({max_freq} times)"

            # --- 處理出現最少次 (支援並列) ---
            min_freq = all_counts[-1][1]
            least_items = [item for item, count in all_counts if count == min_freq]
            least_display = f"{least_items[0]}" if len(least_items) == 1 else f"{tuple(least_items[:2])}..etc{len(least_items)}種"
            least_final = f"{least_display} ({min_freq} times)"

            folder_results.append(f"{os.path.basename(filename):<60} | {most_final:<50} | {least_final:<50}")

        except Exception as e:
            folder_results.append(f"{os.path.basename(filename):<60} | read error: {e}")

    return folder_results

def main():
    # 定義目標資料夾
    subfolders = ["uk-2005", "sk-2005", "com_friendster", "RHG1", "RHG2"]
    
    print("🚀 start analysis ...")

    for folder in subfolders:
        if os.path.isdir(folder):
            print(f"📂 is analysising folder：{folder}...", end=" ", flush=True)
            
            # 取得分析結果
            report = analyze_files_in_folder(folder)
            
            # 設定輸出檔案路徑：直接存在該資料夾內
            output_file = os.path.join(folder, "analysis_result.txt")
            
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write("\n".join(report) + "\n")
            
            print(f"✅ done！file is saved to {output_file}")
        else:
            print(f"⚠️ warning：can't find path {folder}，skip。")

    print("\n✨ mission complete！")

if __name__ == "__main__":
    main()