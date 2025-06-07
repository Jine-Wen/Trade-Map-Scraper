from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import logging

class TradeMapScraper:
    def __init__(self):
        self.setup_logging()
        self.driver = self.setup_driver_with_headers()

    def setup_logging(self):
        log_file = 'logs/scraper_log.txt'
        logger = logging.getLogger('TradeMapScraper')

        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        self.logger = logger
        self.logger.info("Logger initialized.")

    def setup_driver_with_headers(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
        chrome_options.add_argument(f"user-agent={self.get_random_user_agent()}")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
        })
        self.logger.info("WebDriver initialized with headers.")
        return driver

    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36",
        ]
        return random.choice(user_agents)

    def random_delay(self, min_seconds=2, max_seconds=5):
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def simulate_typing(self, element, text):
        for char in text:
            element.send_keys(char)
            self.random_delay(0.1, 0.3)  # 模擬人類打字速度

    def select_dropdown_option(self, dropdown_id, option_value):
        try:
            dropdown = self.wait_and_find_element(By.ID, dropdown_id)
            dropdown.click()
            self.random_delay(1, 2)
            option = self.wait_and_find_element(By.XPATH, f"//select[@id='{dropdown_id}']/option[@value='{option_value}']")
            option.click()
            self.random_delay(3, 5)
            self.logger.info(f"Selected option '{option_value}' in dropdown '{dropdown_id}'.")
        except Exception as e:
            self.logger.error(f"Error selecting dropdown option: {e}")
            raise

    def select_trade_type(self):
        try:
            trade_type_dropdown = self.wait_and_find_element(By.ID, "ctl00_NavigationControl_DropDownList_TradeType")
            trade_type_dropdown.click()
            import_option = self.wait_and_find_element(By.XPATH, "//select[@id='ctl00_NavigationControl_DropDownList_TradeType']/option[@value='I']")
            import_option.click()
            self.logger.info("Trade type set to 'Import'")
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"Error setting trade type to 'Import': {e}")
            raise

    def wait_and_find_element(self, by, value, timeout=20):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def login(self, username, password):
        self.driver.get("https://www.trademap.org/Country_SelProduct_TS.aspx")
        try:
            self.random_delay(3, 6)
            self.wait_and_find_element(By.ID, "ctl00_MenuControl_Label_Login").click()
            self.random_delay(1, 3)
            username_field = self.wait_and_find_element(By.ID, "Username")
            password_field = self.wait_and_find_element(By.ID, "Password")
            
            # 模擬打字輸入帳號和密碼
            self.simulate_typing(username_field, username)
            self.simulate_typing(password_field, password)
            
            self.wait_and_find_element(By.XPATH, '//button[@name="button" and @value="login"]').click()
            self.random_delay(5, 8)
            self.wait_and_find_element(By.ID, "ctl00_MenuControl_marmenu_sub_login_logout")
            self.logger.info("Login successful.")
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            raise
    def logout(self):
        try:
            menu_item = self.wait_and_find_element(By.ID, "ctl00_MenuControl_li_marmenu_login")
            
            actions = ActionChains(self.driver)
            actions.move_to_element(menu_item).perform()
            self.random_delay(1, 3)  

            logout_button = self.wait_and_find_element(By.ID, "ctl00_MenuControl_marmenu_sub_login_logout")
            self.driver.execute_script("arguments[0].click();", logout_button)  
            self.random_delay(2, 5)
            self.logger.info("Logged out successfully.")
        except Exception as e:
            self.logger.error(f"Error during logout: {e}")
            raise      

    def scrape_table_data(self, table_id):
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            table = soup.find("table", id=table_id)
            if not table:
                self.logger.error(f"Table with id {table_id} not found.")
                return pd.DataFrame()

            rows = []
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                rows.append([cell.get_text(strip=True) for cell in cells])

            data = pd.DataFrame(rows[1:], columns=rows[0]) if rows else pd.DataFrame()
            self.logger.info(f"Scraped {len(data)} rows from table '{table_id}'.")
            return data
        except Exception as e:
            self.logger.error(f"Error scraping table data: {e}")
            return pd.DataFrame()

    def scrape_trade_data(self, product_code, country_code):
        try:
            product_code_level1 = product_code[:2]
            product_code_level2 = product_code[:4] if len(product_code) > 2 else None
            product_code_level3 = product_code if len(product_code) > 4 else None

            self.select_dropdown_option("ctl00_NavigationControl_DropDownList_Product", product_code_level1)

            if product_code_level2:
                self.select_dropdown_option("ctl00_NavigationControl_DropDownList_Product", product_code_level2)

            if product_code_level3:
                self.select_dropdown_option("ctl00_NavigationControl_DropDownList_Product", product_code_level3)

            self.select_dropdown_option("ctl00_NavigationControl_DropDownList_Country", country_code)

            self.select_trade_type()

            self.adjust_page_size(300)
            data = self.scrape_table_data("ctl00_PageContent_MyGridView1")
            return data
        except Exception as e:
            self.logger.error(f"Error during trade data scraping: {e}")
            return pd.DataFrame()

    def adjust_page_size(self, size=300):
        try:
            self.driver.execute_script(
                f"document.forms['aspnetForm'].ctl00$PageContent$GridViewPanelControl$DropDownList_PageSize.value = '{size}';"
                "document.forms['aspnetForm'].submit();"
            )
            self.random_delay(8, 12)
            self.logger.info(f"Adjusted page size to {size}.")
        except Exception as e:
            self.logger.error(f"Error adjusting page size: {e}")
            raise

    def scrape(self, username, password, product_country_pairs):
        try:
            self.login(username, password)
            for product_code, country_code in product_country_pairs:
                data = self.scrape_trade_data(product_code, country_code)
                self.save_data(data, f"{product_code}_{country_code}.csv")
        finally:
            try:
                self.logout()
            except Exception as e:
                self.logger.error("Failed to log out properly.")
            finally:
                self.driver.quit()
                self.logger.info("Driver quit.")

    def save_data(self, df, filename):
        output_path = f"data/raw/{filename}"
        if not df.empty:
            df.to_csv(output_path, index=False)
            self.logger.info(f"Data saved to {output_path}")
        else:
            self.logger.warning("No data to save.")
