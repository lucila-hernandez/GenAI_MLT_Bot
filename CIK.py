import requests

class SecEdgar:
    """
    Store and fetch EDGAR company data from the SEC in dictionaries.
    Allows lookup of company CIK by name or ticker.
    """
    def __init__(self,fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.tickerdict = {}

        # Send HTTP request to get the JSON data from the SEC
        headers = {'user-agent': 'MLT LHD lucila.d.delcarmen@gmail.com'}
        r = requests.get(self.fileurl, headers=headers)

        # Get the full JSON response from the SEC and convert it to a Python dictionary
        self.filejson = r.json()

        # Extract the list of company data (excluding field names)
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
        Look up a company's CIK information by name.
        Returns a tuple: (CIK, Name, Ticker, Exchange), or an error message if not found.
        """

        norm_input = name.upper().strip() 
        for name, value in self.namedict.items():
            if norm_input == name:
                return value
        return f"Company name not found"

    def ticker_to_cik(self, ticker):
        """
        Look up a company's CIK information by ticker.
        Returns a tuple: (CIK, Name, Ticker, Exchange), or an error message if not found.
        """
        norm_input = ticker.upper().strip()
        for ticker, value in self.tickerdict.items():
            if norm_input == ticker:
                return value
        return f"Ticker not found"

se = SecEdgar('https://www.sec.gov/files/company_tickers_exchange.json')

print(se.name_to_cik("NETFLIX INC"))
print(se.ticker_to_cik("NFLX"))


