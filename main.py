from scraper import TradeMapScraper
def main():
    username = "CYLiu3@univacco.com"
    password = "CYLiu852"
    product_country_pairs = [("321210", "251")]

    # 爬取數據
    scraper = TradeMapScraper()
    scraper.scrape(username, password, product_country_pairs)

    # 處理數據
    for product_code, country_code in product_country_pairs:
        raw_file = f"data/raw/{product_code}_{country_code}.csv"

if __name__ == "__main__":
    main()
