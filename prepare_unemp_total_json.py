import pandas as pd

#load unemployment data
unemp = pd.read_excel(
    "data/Unemployed by Year.xlsx",
)

#rename columns
unemp = unemp.rename(columns={
    "Total population": "total_population",
    "Labour Force": "labour_force",
    "Registered Unemployed": "registered_unemployed",
})

#delete '%' sign in UNRATE column
unemp['UNRATE'] = unemp['UNRATE'].str.rstrip('%')

#replace commas with dots
unemp = unemp.apply(
    lambda col: pd.to_numeric(
        col.astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
)

unemp.to_json("frontend/uud/public/data/unemployment_2000_2021_y.json", orient="records", indent=2)