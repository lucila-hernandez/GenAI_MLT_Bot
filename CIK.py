import requests

class SecEdgar:
    """
    Store and fetch store EDGAR company data from the SEC in dictionaries.
    Allows lookup of comany CIK by name or ticker.
    """
    def __init__(self,fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}

        # Send HTTP request to get the JSON data from the SEC
        headers = {'user-agent': 'MLT LHD lucila.d.delcarmen@gmail.com'}
        r = requests.get(self.fileurl, headers=headers)

        # Gets the full JSON response from the SEC and turns it into a Python dictionary
        self.filejson = r.json()

        # This gets just the list of companies  not the field names
        data_list = self.filejson["data"]

        # Loop through each row and store CIK info in both dictionaries
        for row in data_list:
            cik = row[0]
            name = row[1]
            ticker = row[2]
            exchange = row[3]
            cik_info = (cik, name, ticker, exchange)
            # Normalize and store using uppercase name and ticker
            self.namedict[name.upper().strip()] = cik_info
            self.tickerdict[ticker.upper().strip()] = cik_info
        
    def name_to_cik(self, name):
        """
        Given a company name, return a tuple with (CIK, Name, Ticker, Exange).
        Normalizes input by uppercasing and stripping spaces.
        """
        norm_input = name.upper().strip() 
        for name, value in self.namedict.items():
            if norm_input == name:
                return value
            return f"Company name '{name}' not found"

    def ticker_to_cik(self, ticker):
        """
        Given a company ticker, return a tuple with (CIK, Name, Ticker, Exange).
        Normalizes input by uppercasing and stripping spaces.
        """
        norm_input = ticker.upper().strip()
        for ticker, value in self.tickerdict.items():
            if norm_input == ticker:
                return value
            return f"Ticker '{ticker}' not found"

se = SecEdgar('https://www.sec.gov/files/company_tickers_exchange.json')

print(se.name_to_cik("Salesforce, Inc"))
print(se.ticker_to_cik("CRM"))


