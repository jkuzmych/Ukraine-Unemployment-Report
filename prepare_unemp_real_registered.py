import pandas as pd
import json

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

#parse unermployment real and registered
unemp_real_registered = unemp.drop(columns=["total_population", "labour_force", "employed", "UNRATE"])

unemp_real_registered = unemp_real_registered.rename(columns={
    "unemployed": "Real unemployed",
    "registered_unemployed": "Registered unemployed"
})

unemp_real_registered_dict = [
    {k: v for k, v in row.items() if pd.notna(v)}
    for row in unemp_real_registered.to_dict(orient="records")
]

result_unemp_real_registered = {
    "data":unemp_real_registered_dict,
    "encoding": {
        "xKey": "year",
        "kind": "line",
        "unit": "thousands",
        "series": {}
    },
    "axes": {
        "x": {"label": "year"},
        "y": {"label": "Unemployment", "suffix": "thousands"}
    },
    "visibleByDefault": [
        "Real unemployed", "Registered unemployed"
    ]
}

for category in unemp_real_registered.columns:
    result_unemp_real_registered["encoding"]["series"][category]={
        "label": category
    }


with open("frontend/uud/public/data/unemployment_real_registered.json", "w", encoding="utf-8") as f:
     json.dump(result_unemp_real_registered, f, indent=2, ensure_ascii=False)
#unemp.to_json("frontend/uud/public/data/unemployment_2000_2021_y.json", orient="records", indent=2)

#parse labour force
lf = unemp.drop(columns=["total_population", "labour_force", "registered_unemployed", "UNRATE"])
lf= lf.dropna()

print(lf)
lf = lf.rename(columns={
    "unemployed": "Unemployed",
    "employed": "Employed"
})

lf_dict = lf.to_dict(orient="records")

result_lf = {
    "data":lf_dict,
    "encoding": {
        "xKey": "year",
        "kind": "line",
        "unit": "thousands",
        "series": {}
    },
    "axes": {
        "x": {"label": "year"},
        "y": {"label": "Unemployment", "suffix": "thousands"}
    },
    "visibleByDefault": [
        "Unemployed", "Employed"
    ]
}

for category in lf.columns:
    result_lf["encoding"]["series"][category]={
        "label": category
    }


# with open("frontend/uud/public/data/labour_force_data.json", "w", encoding="utf-8") as f:
#      json.dump(result_lf, f, indent=2, ensure_ascii=False)