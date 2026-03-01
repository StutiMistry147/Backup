import requests

def fetch_co2_data():
    url = "http://api.worldbank.org/v2/country/USA/indicator/EN.ATM.CO2E.PC?format=json"
    response = requests.get(url)
    data = response.json()[1]

    years = []
    values = []

    for entry in data:
        if entry["value"] is not None:
            years.append(int(entry["date"]))
            values.append(entry["value"])

    df = pl.DataFrame({
        "Year": years,
        "CO2_per_Capita": values
    })

    df.write_csv("data/processed/usa_co2.csv")
    print("Saved USA CO2 data.")
