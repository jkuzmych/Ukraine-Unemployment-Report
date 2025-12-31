import pandas as pd
import json
import math

#load data
unemp = pd.read_excel(
    "data/Unemployed 2008-2021 by Regions.xlsx",
)

#drop "code" column
unemp = unemp.drop(columns=["code"], errors="ignore")

#rename columns
unemp = unemp.rename(columns={
    "attributes": "region",
    "period": "year",
    "data": "unrate",
})

#replace commas with dots
num_cols = unemp.columns.difference(["region"])

unemp[num_cols] = unemp[num_cols].apply(
    lambda col: pd.to_numeric(
        col.astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
)


pd.set_option('display.max_rows', None)

#reshape table to the format:"year: region1_rate, region2_rate, etc"
unemp = (
    unemp
    .pivot_table(
        index="year", 
        columns="region", 
        values="unrate",
    )
    .reset_index()
)


unemp_dict = unemp.to_dict(orient="records")


result = {
    "data":unemp_dict,
    "encoding": {
        "xKey": "year",
        "kind": "line",
        "unit": "%",
        "series": {}
    },
    "axes": {
        "x": {"label": "year"},
        "y": {"label": "Unemployment rate", "suffix": "%"}
    },
    "visibleByDefault": [
        "Ukraine"
    ]
}

for region in unemp.columns:
    result["encoding"]["series"][region]={
        "label": region
    }


for year_data in result["data"]:
    for region_key in list(year_data.keys()):
        if math.isnan(year_data[region_key]):
            year_data.pop(region_key)

with open("frontend/uud/public/data/unemployment_by_region.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)