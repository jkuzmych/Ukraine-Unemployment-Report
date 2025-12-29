import pandas as pd

#load data
unemp = pd.read_excel(
    "data/Unemployed 2008-2021 by Regions.xlsx",
)

#drop "code" column
unemp = unemp.drop(columns=["code"], errors="ignore")

#rename columns
unemp = unemp.rename(columns={
    "attributes": "Region",
    "period": "Period",
    "data": "UNRATE",
})

#replace commas with dots
num_cols = unemp.columns.difference(["Region"])

unemp[num_cols] = unemp[num_cols].apply(
    lambda col: pd.to_numeric(
        col.astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
)

unemp = (
    unemp
    .pivot(index="Period", columns="Region", values="UNRATE")
    .reset_index(),
)

#write jsons
unemp.to_json("frontend/uud/public/data/unemployment_by_region.json", orient="records", indent=2)
