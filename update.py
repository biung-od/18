import pandas as pd
import requests
import os
import chardet

# 定義檔案處理函數
def convert_to_utf8(input_path, output_path):
    try:
        # 自動檢測檔案的編碼
        with open(input_path, 'rb') as file:
            raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        print(f"檢測到的編碼: {detected_encoding}")

        # 以原始編碼讀取檔案內容
        with open(input_path, 'r', encoding=detected_encoding, errors='ignore') as infile:
            content = infile.read()

        # 以 UTF-8 格式寫入到新的檔案
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(content)

        print(f"檔案已成功轉換為 UTF-8 格式，並保存為: {output_path}")
    except Exception as e:
        print(f"轉換過程中發生錯誤: {e}")

# 處理指定的 CSV 檔案
def process_csv_files():
    # 檔案路徑設定
    base_dir = r"C:\Users\OD\Documents\GitHub\18"
    input_files = ["0975080325.csv", "0980963487.csv", "prof.csv","251.csv"]
    output_files = ["0975080325_utf8.csv", "0980963487_utf8.csv", "prof_utf8.csv","251_utf8.csv"]

    # 遍歷檔案進行轉換
    for input_file, output_file in zip(input_files, output_files):
        input_path = os.path.join(base_dir, input_file)
        output_path = os.path.join(base_dir, output_file)
        convert_to_utf8(input_path, output_path)


# 為 HTML 建立 CSS 樣式
css_style = """
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 20px; }
        table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #4CAF50; color: white; cursor: pointer; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
<script>
    document.addEventListener("DOMContentLoaded", function () {
        const headers = document.querySelectorAll("th");
        headers.forEach((header, index) => {
            header.addEventListener("click", () => {
                sortTable(index); // 執行排序
                applyCellStyles(); // 在排序後重新應用樣式
            });
        });

        applyCellStyles(); // 初始載入時應用樣式

        // 修正的數值排序邏輯
        function sortTable(columnIndex) {
            const table = document.querySelector("table");
            const rows = Array.from(table.rows).slice(1); // 排除表頭
            const isAscending = table.getAttribute("data-sort-asc") === "true";

            rows.sort((a, b) => {
                // 取出儲存格的文字並轉為數值
                const aValue = parseFloat(a.cells[columnIndex].innerText.replace('%', '').trim());
                const bValue = parseFloat(b.cells[columnIndex].innerText.replace('%', '').trim());

                // 若值為非數字，排序到最後
                if (isNaN(aValue)) return 1;
                if (isNaN(bValue)) return -1;

                // 根據升序或降序進行排序
                return isAscending ? aValue - bValue : bValue - aValue;
            });

            rows.forEach(row => table.appendChild(row)); // 更新排序後的表格
            table.setAttribute("data-sort-asc", !isAscending); // 切換升序或降序
        }

        function applyCellStyles() {
            const rows = document.querySelectorAll("tbody tr");
            rows.forEach(row => {
                // "今年績效" 字體顏色
                const performanceCell = row.cells[6];
                if (performanceCell) {
                    const value = parseFloat(performanceCell.textContent.replace('%', ''));
                    if (!isNaN(value)) {
                        if (value > 0) {
                            performanceCell.style.color = "red"; // 正值顯示紅字
                        } else if (value < 0) {
                            performanceCell.style.color = "green"; // 負值顯示綠字
                        }
                    }
                }

                // "應持有比例" 背景顏色
                const holdRatioCell = row.cells[5];
                if (holdRatioCell) {
                    const ratioValue = parseFloat(holdRatioCell.textContent.replace('%', ''));
                    if (!isNaN(ratioValue)) {
                        if (ratioValue >= 2.5) { // 修正條件：包含等於 2.5%
                            holdRatioCell.style.backgroundColor = "pink"; // 大於或等於2.5%用粉紅色
                                } else if (ratioValue > 1 && ratioValue <= 2) {
                                holdRatioCell.style.backgroundColor = "plum"; // 介於1%至2%用粉紫色
                                } else if (ratioValue >= 0.75) {
                                holdRatioCell.style.backgroundColor = "lightblue"; // 大於0.75%
                                }

                    }
                }
            });
        }
    });
</script>

"""

# 將 CSV 轉換為 HTML
def save_html_with_style(df, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(css_style + df.to_html(index=False, escape=False))

# 將 CSV 檔案生成對應 HTML
def generate_html_from_csv():
    base_dir = r"C:\Users\OD\Documents\GitHub\18"
    input_files = ["0975080325_utf8.csv", "0980963487_utf8.csv", "251_utf8.csv"]
    output_html_files = ["0975080325.html", "0980963487.html", "251.html"]

    for input_file, html_file in zip(input_files, output_html_files):
        input_path = os.path.join(base_dir, input_file)
        html_path = os.path.join(base_dir, html_file)

        # 讀取 CSV 並生成 HTML
        try:
            df = pd.read_csv(input_path, engine='python', on_bad_lines='skip')
            save_html_with_style(df, html_path)
            print(f"HTML 檔案已成功保存為: {html_path}")
        except Exception as e:
            print(f"處理 {input_file} 時發生錯誤: {e}")


# 執行生成 HTML 的程式
if __name__ == "__main__":
    generate_html_from_csv()
# 定義 URL 和目標資料夾
urls = [
    "http://192.168.1.166/stock/pandyfinal.csv",
    "http://192.168.1.166/stock/final.csv",
]
target_directory = r"C:\Users\OD\Documents\GitHub\18"

# 確保目標資料夾存在
os.makedirs(target_directory, exist_ok=True)

# 下載並保存每個檔案（prof.csv 例外）
for url in urls:
    if "prof.csv" in url:
        continue  # 不下載 prof.csv，因為它已經儲存在指定目錄
    filename = os.path.join(target_directory, os.path.basename(url))
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 請求是否出錯

        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded and saved: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# 處理和轉換其他 CSV 檔案
process_csv_files()

# 生成對應的 HTML
generate_html_from_csv()

# 處理第一個 CSV 檔案
csv_file_1 = os.path.join(target_directory, 'pandyfinal.csv')
df1 = pd.read_csv(csv_file_1)
html_file_1 = os.path.join(target_directory, 'pandy_data.html')
save_html_with_style(df1, html_file_1)
print(f"HTML 檔案已成功保存為 {html_file_1}")

# 處理第二個 CSV 檔案
csv_file_2 = os.path.join(target_directory, 'final.csv')
df2 = pd.read_csv(csv_file_2)
html_file_2 = os.path.join(target_directory, 'stock_data.html')
save_html_with_style(df2, html_file_2)
print(f"HTML 檔案已成功保存為 {html_file_2}")

# 處理第三個 CSV 檔案（UTF-8 格式檔案）
csv_file_3 = os.path.join(target_directory, 'prof_utf8.csv')
df3 = pd.read_csv(csv_file_3)
html_file_3 = os.path.join(target_directory, 'prof_data.html')
save_html_with_style(df3, html_file_3)
print(f"HTML 檔案已成功保存為 {html_file_3}")

#處理ai生成股票分析股價後合併
def update_ownstock_with_prices(ownstock_file, final_file, output_file):
    try:
        # 讀取 ownstock.csv 和 final.csv
        ownstock = pd.read_csv(ownstock_file)
        final = pd.read_csv(final_file)

        # 確保欄位名稱整潔（移除空格）
        ownstock.columns = ownstock.columns.str.strip()
        final.columns = final.columns.str.strip()

        # 檢查欄位名稱是否匹配
        if '股票名稱' not in ownstock.columns or '股名' not in final.columns:
            raise KeyError("請檢查 CSV 檔案的欄位名稱。ownstock.csv 應有 '股票名稱'，final.csv 應有 '股名'")

        # 統一名稱，移除空格，進行比對
        ownstock['股票名稱'] = ownstock['股票名稱'].str.strip()
        final['股名'] = final['股名'].str.strip()

        # 建立 final 的對應字典，根據股名對應股價
        price_map = final.set_index('股名')['股價'].to_dict()

        # 更新 ownstock.csv 第 2 欄（佔比）為股價
        ownstock['佔比'] = ownstock['股票名稱'].map(price_map).fillna(ownstock['佔比'])

        # 儲存更新後的資料為新的 CSV 文件
        ownstock.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"檔案已成功更新並儲存為 {output_file}")

    except Exception as e:
        print(f"發生錯誤: {e}")

# 檔案名稱
ownstock_file = "ownstock.csv"  # ownstock.csv 的檔案名稱
final_file = "final.csv"        # final.csv 的檔案名稱
output_file = "updated_ownstock.csv"  # 輸出的檔案名稱

# 執行函數
update_ownstock_with_prices(ownstock_file, final_file, output_file)

def clean_and_merge_csv(ownstock_file, stockanalysis_file, output_file):
    try:
        # 嘗試讀取 CSV 文件
        ownstock = pd.read_csv(ownstock_file)
        stockanalysis = pd.read_csv(stockanalysis_file, on_bad_lines='skip')

        # 清理資料 (移除空格)
        ownstock[ownstock.columns[0]] = ownstock[ownstock.columns[0]].str.strip()
        stockanalysis[stockanalysis.columns[0]] = stockanalysis[stockanalysis.columns[0]].str.strip()

        # 確保合併列存在
        if ownstock.columns[0] not in stockanalysis.columns:
            raise KeyError(f"列名稱 {ownstock.columns[0]} 在 stockanalysis.csv 中不存在。")

        # 合併資料
        merged = pd.merge(ownstock, stockanalysis, on=ownstock.columns[0], how='left')

        # 填補缺失值
        merged.fillna("缺失資料", inplace=True)

        # 儲存結果
        merged.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"檔案已成功合併並儲存為 {output_file}")
    
    except Exception as e:
        print("發生錯誤: ")
        print(e)

# 檔案名稱
ownstock_file = "updated_ownstock.csv"
stockanalysis_file = "stockanalysis.csv"
output_file = "allstock.csv"

# 執行函數
clean_and_merge_csv(ownstock_file, stockanalysis_file, output_file)

 
 