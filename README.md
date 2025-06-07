TradeMap 自動化爬蟲工具
這是一個我自己開發的小工具，用來從 TradeMap.org 上抓進口貿易資料。因為 TradeMap 本身雖然資料很豐富，但使用者介面偏向人工操作，不太適合需要大量查詢或自動化流程的情境，所以我就用 Selenium 做了這個自動化爬蟲，幫忙把資料抓下來儲存成 CSV，後續就能方便做分析或整合到其他系統。

💡 功能簡介
這個工具主要做以下幾件事：

自動登入 TradeMap 帳號

選擇產品（HS code）與目標國家

設定為「進口資料」的模式

擷取網頁上的表格資料

轉成 DataFrame 並儲存為 .csv 檔

自動登出、關閉瀏覽器

全程有 log 紀錄發生了什麼事

整個過程會模擬人類操作，包括打字速度、隨機等待時間、隨機 User-Agent，盡量讓行為自然一點，減少被網站封鎖的風險。

🧱 專案結構
bash
複製
編輯
.
├── main.py                  # 主程式：設定帳號/密碼和要查詢的項目，開始爬蟲
├── scraper.py               # TradeMapScraper 類別，封裝所有爬蟲邏輯
├── logs/
│   └── scraper_log.txt      # 執行過程中寫入的 log
└── data/
    └── raw/                 # 所有輸出的 .csv 檔案會存這裡
🚀 如何使用
1. 安裝必要套件
這個工具是用 Python 寫的，要先安裝以下套件（建議使用虛擬環境）：

bash
複製
編輯
pip install selenium beautifulsoup4 pandas
2. 安裝 ChromeDriver
這個爬蟲是操作 Chrome 瀏覽器，需要安裝對應版本的 ChromeDriver。安裝完記得把它放到環境變數中或是跟程式放在同一個目錄。

3. 設定登入資訊與查詢參數
打開 main.py，修改以下幾行：

python
複製
編輯
username = "你的TradeMap帳號"
password = "你的密碼"
product_country_pairs = [("321210", "251")]  # [(產品代碼, 國家代碼)]
每一組 (產品代碼, 國家代碼) 代表一個查詢任務。產品代碼是 HS Code，國家代碼可以從 TradeMap 網站中查到。

4. 執行程式
bash
複製
編輯
python main.py
程式會自動打開 Chrome 瀏覽器、登入、選擇條件、擷取資料，最後登出並關閉視窗。

📁 輸出結果
程式會把查詢結果存成 .csv，檔案放在 data/raw/ 目錄下。檔名格式是 {產品代碼}_{國家代碼}.csv，例如：

bash
複製
編輯
data/raw/321210_251.csv
內容就是 TradeMap 表格上的欄位和資料，方便之後用 Excel 或 Python 處理。

🛠 一些技術細節
透過 Selenium + ChromeDriver 操作網站互動

BeautifulSoup 抓 HTML 表格轉成結構化資料

為了防止被偵測為 bot，有加入隨機延遲、模擬打字等行為

登入與登出都有錯誤處理，如果網站結構改了，log 檔會記錄錯誤方便追蹤

⚠️ 注意事項
TradeMap 有流量限制，如果查太多可能會被暫時鎖帳號，請斟酌使用。

帳號密碼目前是寫在 main.py 裡面，建議實際部署時改用 .env 或其他方式管理機密資訊。

如果 TradeMap 的頁面結構未來有變，程式可能需要跟著調整。

🔄 TODO（可能之後會加上的功能）
支援 .env 管理帳密

讓 CLI 可以帶參數執行（不用寫死在程式裡）

加入 retry 機制（網站 timeout 或失敗時自動重試）

支援出口資料（目前是固定抓進口）

自動解析多頁資料

有興趣可以自由 fork 或改寫，如果你也需要大量查詢 TradeMap 資料，應該會派得上用場。
