"""
Process real vs. registered unemployment data.

This script:
1. Loads unemployment data from Excel file
2. Separates real unemployment and registered unemployment
3. Generates JSON file comparing real vs. registered unemployment
"""

import json
import pandas as pd


INPUT_FILE = "data/Unemployed by Year.xlsx"
OUTPUT_REAL_REGISTERED_FILE = "frontend/uud/public/data/unemployment_real_registered.json"
# OUTPUT_LABOUR_FORCE_FILE = "frontend/uud/public/data/labour_force_data.json"

COLUMN_MAPPING = {
    "Total population": "total_population",
    "Labour Force": "labour_force",
    "Registered Unemployed": "registered_unemployed"
}


def load_data():
    """Load unemployment data from Excel file."""
    unemp = pd.read_excel(INPUT_FILE)
    
    unemp = unemp.rename(columns=COLUMN_MAPPING)
    
    unemp['UNRATE'] = unemp['UNRATE'].str.rstrip('%')
    
    # Convert all columns to numeric (replace commas with dots)
    unemp = unemp.apply(
        lambda col: pd.to_numeric(
            col.astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        )
    )
    
    return unemp

def process_real_vs_registered(unemp):
    """
    Process real vs. registered unemployment data.
    
    Args:
        unemp: DataFrame with unemployment data
    
    Returns:
        Dictionary with chart structure for real vs. registered unemployment
    """
    unemp_real_registered = unemp.drop(
        columns=["total_population", "labour_force", "employed", "UNRATE"]
    )
    
    unemp_real_registered = unemp_real_registered.rename(columns={
        "unemployed": "Real unemployed",
        "registered_unemployed": "Registered unemployed"
    })
   
    unemp_real_registered_dict = [
        {k: v for k, v in row.items() if pd.notna(v)}
        for row in unemp_real_registered.to_dict(orient="records")
    ]
  
    columns = list(unemp_real_registered.columns)
    result = {
        "data": unemp_real_registered_dict,
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
        "visibleByDefault": ["Real unemployed", "Registered unemployed"]
    }
    
    for category in columns:
        result["encoding"]["series"][category] = {
            "label": category
        }
    
    return result


def process_labour_force(unemp):
    """
    Process labour force data (employed vs. unemployed).
    
    Args:
        unemp: DataFrame with unemployment data
    
    Returns:
        Dictionary with chart structure for labour force
    """
    lf = unemp.drop(
        columns=["total_population", "labour_force", "registered_unemployed", "UNRATE"]
    )
 
    lf = lf.dropna()
    
    lf = lf.rename(columns={
        "unemployed": "Unemployed",
        "employed": "Employed"
    })
  
    lf_dict = lf.to_dict(orient="records")

    columns = list(lf.columns)
    result = {
        "data": lf_dict,
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
        "visibleByDefault": ["Unemployed", "Employed"]
    }
    
    for category in columns:
        result["encoding"]["series"][category] = {
            "label": category
        }
    
    return result

def main():
    """Main processing function."""
    unemp = load_data()
    
    result_real_registered = process_real_vs_registered(unemp)
    
    with open(OUTPUT_REAL_REGISTERED_FILE, "w", encoding="utf-8") as f:
        json.dump(result_real_registered, f, indent=2, ensure_ascii=False)
    
    # result_lf = process_labour_force(unemp)
    # print(result_lf)

    # Uncomment to write a json
    # with open(OUTPUT_LABOUR_FORCE_FILE, "w", encoding="utf-8") as f:
    #     json.dump(result_lf, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
