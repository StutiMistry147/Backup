import polars as pl

def merge_datasets():
    company_df = pl.read_csv("data/processed/company_emissions.csv")
    country_df = pl.read_csv("data/processed/usa_co2.csv")

    merged = company_df.join(country_df, on="Year", how="left")

    merged = merged.with_columns(
        (pl.col("Emissions") / 1_000_000).alias("Emissions_Million_Tons")
    )

    merged.write_csv("data/processed/final_esg_dataset.csv")
    print("Final ESG dataset saved.")
