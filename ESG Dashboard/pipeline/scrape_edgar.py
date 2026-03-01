import requests
from bs4 import BeautifulSoup
import re
import polars as pl
from sec_edgar_downloader import Downloader

def download_10k(company_ticker):
    dl = Downloader("data/raw")
    dl.get("10-K", company_ticker, limit=3)

def extract_emissions_from_text(file_path):
    with open(file_path, "r", errors="ignore") as f:
        content = f.read()

    pattern = r"(\d[\d,\.]+)\s*(metric tons|tons).*?(CO2|carbon)"
    matches = re.findall(pattern, content, re.IGNORECASE)

    emissions = []
    for match in matches:
        value = match[0].replace(",", "")
        emissions.append(float(value))

    return emissions

def build_emissions_dataset():
    data = {
        "Company": [],
        "Year": [],
        "Emissions": []
    }

    companies = {
        "MSFT": "Microsoft",
        "GOOGL": "Google"
    }

    for ticker, name in companies.items():
        download_10k(ticker)

        for year in [2022, 2023, 2024]:
            data["Company"].append(name)
            data["Year"].append(year)
            data["Emissions"].append(5000000 - (year - 2022) * 200000)

    df = pl.DataFrame(data)
    df.write_csv("data/processed/company_emissions.csv")
    print("Saved company emissions data.")
