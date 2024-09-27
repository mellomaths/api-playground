import requests
from datetime import datetime


class DateHelper:
    
    @staticmethod
    def get_now_timestamp():
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        return timestamp


class Credentials:
    email: str
    password: str
    
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
    

class FogoCruzadoApi:
    
    token: str = None
    expiration: int = 0
    
    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials
        self.api_base_url = "https://api-service.fogocruzado.org.br/api/v2"
        self.api_base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
    def add_bearer_token_to_headers(self, headers: dict, token: str) -> dict:
        headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def is_authenticated(self):
        timestamp = DateHelper.get_now_timestamp()
        return self.token is not None and timestamp < self.expiration

    
    def authenticate(self) -> str:
        response = requests.post(f"{self.api_base_url}/auth/login", json={
            "email": self.credentials.email,
            "password": self.credentials.password,
        }, headers=self.api_base_headers)
        if response.status_code != 201:
            print(response.status_code)
            print(response.text)
            return None
        
        data = response.json()
        self.token = data['data']['accessToken']
        self.expiration = DateHelper.get_now_timestamp() + data['data']['expiresIn']
        return self.token
    
    def refresh_access_token(self) -> str:
        headers = self.add_bearer_token_to_headers(self.api_base_headers, self.token)
        
        response = requests.post(f"{self.api_base_url}/auth/refresh", headers=headers)
        if response.status_code != 201:
            print(response.status_code)
            print(response.text)
        
        data = response.json()
        return data['data']['accessToken']
    
    def get_states(self) -> list[dict]:
        if not self.is_authenticated():
            self.authenticate()
        
        headers = self.add_bearer_token_to_headers(self.api_base_headers, self.token)
        response = requests.get(f"{self.api_base_url}/states", headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            return []
        
        data = response.json()
        return data['data']
    
    def get_cities(self) -> list[dict]:
        if not self.is_authenticated():
            self.authenticate()
            
        headers = self.add_bearer_token_to_headers(self.api_base_headers, self.token)
        response = requests.get(f"{self.api_base_url}/cities", headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            return []
        
        data = response.json()
        return data['data']
    
    def get_occurrences(self, state_id: str, initial_date: str, final_date: str, page: int = 1) -> tuple[list[dict], bool, int]:
        if not self.is_authenticated():
            self.authenticate()
            
        headers = self.add_bearer_token_to_headers(self.api_base_headers, self.token)
        response = requests.get(f"{self.api_base_url}/occurrences?initialdate={initial_date}&finaldate={final_date}&idState={state_id}&order=ASC&page={page}&take=100", headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            return [], False, 0
        
        data = response.json()
        has_next_page = data["pageMeta"]["hasNextPage"]
        page_count = data["pageMeta"]["pageCount"]
        data = data["data"]
        return data, has_next_page, page_count
    
    def get_all_occurrences(self, state_id: str, initial_date: str, final_date: str) -> list[dict]:
        page = 1
        occurrences = []
        has_next_page = True
        while has_next_page:
            data, has_next_page, page_count = self.get_occurrences(state_id, initial_date, final_date, page)
            occurrences += data
            page += 1
            
        return occurrences      
    