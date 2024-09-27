import requests


class YahooFinanceApi:
    
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    
    available_companies = [
        "NVIDIA",
        "Apple",
        "Intel",
    ]
    companies_symbol_mapping = {
        "NVIDIA": "NVDA",
        "Apple": "APPL",
        "Intel": "INTC",
    }
    
    def get_stock_price(self, symbol: str) -> dict:
        url = f"{self.base_url}/{symbol}?metrics=high&interval=1d&range=1y"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Error when loading stock prices from url {url}")
            return None
        
        return response.json()["chart"]["result"][0]
    