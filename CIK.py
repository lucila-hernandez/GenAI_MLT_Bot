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
        self.headers = {'user-agent': 'MLT LHD lucila.d.delcarmen@gmail.com'}
        
        r = requests.get(self.fileurl, headers=self.headers)

        # Get the full JSON response from the SEC and convert it to a Python dictionary
        self.filejson = r.json()

        # Extract the list of company data 
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

    def _fetch_submissions(self,cik):
        """
        Fetches the company's recent filings from the SEC Submissions API.
        """
        padded_cik = cik.zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error: {http_err} (status code: {r.status_code})")
        except requests.exceptions.RequestException as req_err:
            print(f"Network error: {req_err}")
        except ValueError as json_err:
            print("Error decoding JSON response.")
        return None
    
    def annual_filing(self, cik, year):
        """
        Retrieves the URL for the company's 10-K (annual report) filing for a given year.
        """
        result = self._fetch_submissions(cik)
        if result is None:
            return "Failed to retrieve annual filing data due to an API error."
        recent = result["filings"]["recent"]
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accession_number = recent.get("accessionNumber", [])
        primary_document = recent.get("primaryDocument", [])

        for i in range(len(forms)):
            if forms[i] == "10-K" and dates[i].startswith(str(year)):
                accession = accession_number[i].replace("-", "")
                document = primary_document[i]
                clean_cik = cik.lstrip("0")
                url = f"https://www.sec.gov/Archives/edgar/data/{clean_cik}/{accession}/{document}"
                return url

        return f"No 10-K filing found"

    def quarterly_filing(self, cik, year, quarter):
        """
        Retrieves the URL for the company's 10-Q (quarterly report) filing for a given year and quarter.
        """
        result = self._fetch_submissions(cik)
        if result is None:
            return "Failed to retrieve quarterly filing data due to an API error."
        recent = result["filings"]["recent"]
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accession_number = recent.get("accessionNumber", [])
        primary_document = recent.get("primaryDocument", [])

        for i in range(len(forms)):
            if forms[i] == "10-Q" and dates[i].startswith(str(year)):
                month = int(dates[i].split("-")[1])
                if (quarter == 1 and month in [1, 2, 3]) or \
                (quarter == 2 and month in [4, 5, 6]) or \
                (quarter == 3 and month in [7, 8, 9]) or \
                (quarter == 4 and month in [10, 11, 12]):

                    accession = accession_number[i].replace("-", "")
                    document = primary_document[i]
                    clean_cik = cik.lstrip("0")
                    url = f"https://www.sec.gov/Archives/edgar/data/{clean_cik}/{accession}/{document}"
                    return url

        return f"No 10-Q filing found"

se = SecEdgar('https://www.sec.gov/files/company_tickers_exchange.json')

print(se.name_to_cik("NETFLIX INC"))
print(se.ticker_to_cik("NFLX"))
print()
cik = "1065280" 
print(se.annual_filing(cik, 2023))      
print(se.quarterly_filing(cik, 2023, 2)) 
