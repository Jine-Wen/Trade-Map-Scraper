# TradeMap 自動化爬蟲工具

## 🚀 簡介
我是小白，由於公司業務需求，開發「TradeMap 自動化爬蟲工具」，省去人手操作 TradeMap 網站的時間成本  
只要設定好 HS Code、國家代碼，工具就會自己登入、抓資料，最後生成 CSV，讓你能馬上拿去分析或整合到其他系統

---

## 💡 主要功能
1. **自動登入**：使用 Selenium 模擬瀏覽器登入 TradeMap 帳號  
2. **條件設定**：自動選擇 HS Code & 目標國家、切換到「進口資料」  
3. **資料擷取**：抓取網頁上的表格並用 BeautifulSoup 解析  
4. **存成 CSV**：把抓到的資料轉成 Pandas DataFrame，再匯出到 data/raw/  
5. **自動登出**：完成後安全登出並關閉瀏覽器  
6. **完整日誌**：執行過程都會記錄到 logs/scraper_log.txt  

> 為了降低被網站封鎖的風險，工具內建：
> - 隨機延遲（模擬人類瀏覽）
> - 隨機打字速度
> - 隨機 User-Agent  

---

## 🏗 專案結構
    .
    ├── main.py                # 主程式：設定帳密 & 查詢項目，啟動爬蟲
    ├── scraper.py             # TradeMapScraper 類別，封裝所有爬蟲邏輯
    ├── logs/
    │   └── scraper_log.txt    # 執行日誌
    └── data/
        └── raw/               # 爬取的 CSV 結果

---

## 📦 安裝教學

1. **複製／下載專案**  
       
       git clone https://github.com/你的帳號/trademap-scraper.git  
       cd trademap-scraper  

2. **建立並啟用虛擬環境**
       
       python3 -m venv venv  
       source venv/bin/activate  

3. **安裝必要套件**  
       
       pip install selenium beautifulsoup4 pandas  

4. **下載 ChromeDriver**  
   - 依照你的 Chrome 版本，下載對應的 ChromeDriver（https://chromedriver.chromium.org/）  
   - 把執行檔放到 `$PATH` 或與 `main.py` 同一資料夾  

---

## ⚙️ 設定 & 執行

1. 打開 `main.py`，把你的 TradeMap 帳號、密碼，以及要查的 HS Code & 國家代碼填好：  
       
       username = "你的TradeMap帳號"  
       password = "你的密碼"  
       # 範例：查 HS Code 321210 的國家代碼 251  
       product_country_pairs = [("321210", "251")]  

2. 執行程式：  
       
       python main.py  

3. 成功執行後，資料會輸出到：  
       
       data/raw/321210_251.csv  

---

## 🛠 技術細節
- **Selenium + ChromeDriver**：自動化操作瀏覽器  
- **BeautifulSoup**：解析 HTML，提取表格內容  
- **Pandas**：整理成 DataFrame，再匯出 CSV  
- **反偵測機制**：隨機延遲、打字、User-Agent，降低被封風險  
- **Error Handling**：若頁面結構變動或其他問題，會捕捉錯誤並寫進 logs/scraper_log.txt  

---

## ⚠️ 使用注意
- TradeMap 有流量限制，若大量查詢可能會被暫時鎖帳號  
- 目前帳密是寫在程式裡，請務必在正式環境改用 `.env` 或其他安全方式管理  
- 若 TradeMap 網站改版，可能需要更新爬蟲邏輯

---
## 以上為相關的介紹，請勿進行惡意的攀爬或是癱瘓系統的行為👍，感謝!!
