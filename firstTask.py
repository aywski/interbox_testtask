import requests
from tabulate import tabulate

class CountryInfo:
    BASE_URL = "https://restcountries.com/v3.1/all"

    def __init__(self):
        self.country_data = self._load_all_countries()

    def _load_all_countries(self):
        try:
            response = requests.get(self.BASE_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error loading data: {e}")
            return None

    def get_country_info(self, country_name):
        if not self.country_data:
            return None

        for country in self.country_data:
            if country_name.lower() in [country.get("name", {}).get("common", "").lower(), 
                                        country.get("name", {}).get("official", "").lower()]:
                return {
                    "name": country.get("name", {}).get("common", "N/A"),
                    "capital": country.get("capital", ["N/A"])[0],
                    "flag": country.get("flags", {}).get("png", "N/A")
                }
        return None

    def print_country_info(self, country_names):
        table = []
        for country_name in country_names:
            info = self.get_country_info(country_name)
            if info:
                table.append([info["name"], info["capital"], info["flag"]])
            else:
                table.append([country_name, "N/A", "N/A"])

        print(tabulate(table, headers=["Country", "Capital", "Flag"]))

countries = ["Ukraine", "France", "Japan", "United States"]
country_info = CountryInfo()
country_info.print_country_info(countries)
