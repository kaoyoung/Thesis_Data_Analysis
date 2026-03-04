import glob
import os
from collections import Counter

def analyze_files():
    # 定義檔案名稱的匹配模式
    # 說明：
    # tmp_feright_ : 固定前綴
    # * : 匹配 (con/cut)
    # _            : 分隔符
    # * : 匹配 (sk/uk)
    # -2005_paper.netl_ : 固定中間部分
    # * : 匹配 (512/1024/2048)
    file_pattern = "tmppartition_freight_*_*_paper.netl_*"
    
    # 取得所有符合模式的檔案列表
    files = glob.glob(file_pattern)
    
    if not files:
        print("未在當前目錄找到符合格式的檔案。")
        return

    print(f"{'檔案名稱':<150} | {'出現最多次 (字串, 次數)':<25} | {'出現最少次 (字串, 次數)':<25}")
    print("-" * 110)

    for filename in files:
        # 為了嚴謹，我們可以檢查檔名結尾是否為合法的數字 (512, 1024, 2048)
        # 雖然 glob 已經篩選過，但這裡做二次確認更保險
        if not (filename.endswith("512") or filename.endswith("1024") or filename.endswith("2048")):
            continue

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                # 讀取每一行並去除換行符號
                lines = [line.strip() for line in f if line.strip()]
                
                if not lines:
                    print(f"{filename:<150} | {'(檔案空白)':<25} | {'(檔案空白)':<25}")
                    continue

                # 使用 Counter 進行統計
                counter = Counter(lines)
                
                # 取得最常出現的 (回傳列表中的第一個 tuple)
                most_common = counter.most_common(1)[0]
                
                # 取得最少出現的 (由於 most_common 回傳的是排序後的，最後一個即為最少)
                # 注意：如果有多個字串次數相同，這裡只會取其中一個
                least_common = counter.most_common()[-1]

                print(f"{filename:<50} | {str(most_common):<25} | {str(least_common):<25}")

        except Exception as e:
            print(f"讀取檔案 {filename} 時發生錯誤: {e}")

if __name__ == "__main__":
    analyze_files()