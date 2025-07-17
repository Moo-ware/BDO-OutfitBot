import requests
import os
import pickle
import asyncio
import random
from market.decoder import unpack


class APIHandler:
    def __init__(self):
        self.trade_url = 'https://na-trade.naeu.playblackdesert.com'
        self.login_url = 'https://account.pearlabyss.com/en-US/Member/Login/LoginProcess'
        self.session = requests.Session()
        self.login_status = False
        self.email = None
        self.password = None

        if self.load_session() == -1:
            print("Session file not found. Please login.")

    async def check_stock(self):
        # This function will check the stock of all items in the marketplace, and return a list of item_ID that are in stock.
        url = 'https://na-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
        headers = {
        "Content-Type": "application/json",
        "User-Agent": "BlackDesert"
        }
        payload_Male = {
        "keyType": 0,
        "mainCategory": 55,
        "subCategory": 1
        }
        payload_Female = {
        "keyType": 0,
        "mainCategory": 55,
        "subCategory": 2
        }
        buyList = []

        response_Male = requests.request('POST', url, json=payload_Male, headers=headers)
        response_Female = requests.request('POST', url, json=payload_Female, headers=headers)

        for i in unpack(response_Male.content).split('|')[:-1]:
            j = i.split('-')
            if j[1] != '0':      # if item is in stock
                buyList.append([j[0], j[1], j[3]])

        for i in unpack(response_Female.content).split('|')[:-1]:
            j = i.split('-')
            if j[1] != '0':      # if item is in stock
                buyList.append([j[0], j[1], j[3]])

        return buyList
    
    async def check_stock_test(self):
        # THIS IS A TESTING FUNCTION ONLY
        headers = {
        "Content-Type": "application/json",
        "User-Agent": "BlackDesert"
        }
        
        url = 'https://na-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketSubList'
        
        payload={
            "keyType": "0",
            "mainKey": "13771"
        }
        
        response = requests.request('POST', url, json=payload, headers=headers)

        response_split = response.json()['resultMsg'].split('-')
        
        buyList = []
        if response_split[4] != '0':
            buyList.append([response_split[0], response_split[4], '25200'])

        return buyList


    async def login(self):
        # This function will attempt to log in to the marketplace using the provided email and password.
        # Get the PA-STATE cookie from the login page, which is needed for the login payload.
        self.session = requests.Session()
        headers_pastate = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response_loginPage = self.session.get(self.trade_url, headers=headers_pastate)
        loginPage = response_loginPage.request._cookies.get_dict()
        pastate = loginPage['PA-STATE']

        # Create the login payload using the PA-STATE
        login_payload = {
            "hdAccountUrl": "https://account.pearlabyss.com",
            "_isLinkingLogin": "false",
            "_returnUrl": f"https://account.pearlabyss.com/en-US/Member/Login/AuthorizeOauth?response_type=code&scope=profile&state={pastate}&client_id=client_id&redirect_uri=https://na-trade.naeu.playblackdesert.com/Pearlabyss/Oauth2CallBack",
            "_joinType": 1,
            "_email": self.email,
            "_password": self.password,
            "_isIpCheck": "false"
        }

        headers_login = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://account.pearlabyss.com"
        }

        response_login = self.session.post(url=self.login_url, data=login_payload, headers=headers_login)
        login_cookie = response_login.request._cookies.get_dict()


        # Check if the login was successful by checking the cookies set by the server
        if 'TradeAuth_Session' in login_cookie and '__RequestVerificationToken' in login_cookie:
            return 1 # Login successful
        else:
            return 0 # Login failed

    async def buy_item(self, buyList):
        # This function will buy the items in the buyList.
        # buyList is of format [(item_id, stock, price), ...]
        
        url = 'https://na-game-trade.naeu.playblackdesert.com/GameTradeMarket/BuyItem'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8,zh-CN;q=0.7,zh;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        

        for item in buyList:
            i = 0
            while i < int(item[1]):
                payload = {
                    "buyMainKey": item[0],
                    "buySubKey": "0",
                    "buyKeyType": "0",
                    "isWaitItem": "false",
                    "otp": "",
                    "retryBiddingNo": "",
                    "buyPrice": item[2],
                    "buyCount": "1",
                    "buyChooseKey" : "0"
                }
                response = self.session.post(url, headers=headers, data=payload)
                response_json = response.json()

                if response_json['resultCode'] == 0:
                    print(f"Bought {item[0]} for {item[2]} silver.")
                    i += 1
                elif response_json['resultCode'] == 2000:
                    print("Login session expired. Attempting to login again...")
                    self.login()
                else:
                    print(f"Unexpected resultCode: {response_json} when trying to buy {item[0]} for {item[2]} silver.")
                    break  # Break from the while loop if unexpected resultCode

                await asyncio.sleep(random.uniform(1, 2.5))  # Sleep for 1 - 2.5 second between each buy to avoid looking suspicious.


    async def is_session_expired(self):
        # This function will check if the session is expired, by using the AppSessionRefresh endpoint.
        # If the session is not expired, _resultCode will be 0, else it will be -1.

        url = 'https://na-trade.naeu.playblackdesert.com/Home/AppSessionRefresh'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://na-trade.naeu.playblackdesert.com",
            "Referer": "https://na-trade.naeu.playblackdesert.com/Home/list/hot",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        
        response = self.session.post(url, headers=headers)
        status_code = response.json()['_resultCode']

        if status_code == 0:
            return 0   # session is not expired
        else:    
            return -1   # session is expired


    def save_session(self):
        # This function will save the current session to a file, so that we can load it later.

        with open('session.pkl', 'wb') as f:
            pickle.dump(self.session, f)
    
    
    def load_session(self):
        # This function will load the session from a file, so that we can use it later.
        try:
            with open('session.pkl', 'rb') as f:
                self.session = pickle.load(f)
            return 0
        except FileNotFoundError:   # if the file does not exist
            return -1
    

    # Testing only
    async def get_mp_inventory(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        response = self.session.post(url='https://na-trade.naeu.playblackdesert.com/Home/GetMyWalletList', headers=headers)
        return response.json()