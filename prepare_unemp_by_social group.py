"""
Process unemployment data by social group (gender and area type).

This script:
1. Loads unemployment and employment data from Excel files
2. Calculates unemployment rates by category
3. Generates JSON files for unemployment rates and absolute numbers
   broken down by social groups (Men/Women, Urban/Rural)
"""

import json
import pandas as pd

# Configuration

INPUT_UNEMPLOYMENT_FILE = "data/Unemployed 2015-2021 by Quarter Ukraine.xlsx"
INPUT_EMPLOYMENT_FILE = "data/Employed 2015-2021 by Quarter Ukraine.xlsx"
OUTPUT_RATE_FILE = "frontend/uud/public/data/unrate_by_social_group.json"
OUTPUT_ABSOLUTE_FILE = "frontend/uud/public/data/unemployment_by_social_group.json"

AGE_CATEGORY_FILTER = "15-70 years"
NUMERIC_COLUMNS = ["total", "females", "males", "urban", "rural"]
COLUMN_MAPPING = {
    "atributes": "age_category",
    "attributes": "age_category",
    "total population": "total",
    "urban area": "urban",
    "rural area": "rural"
}

# Data Loading and Cleaning

def load_unemployment_data():
    """Load and clean unemployment data from Excel file."""
    unemp = pd.read_excel(INPUT_UNEMPLOYMENT_FILE, header=1)
    
    unemp = unemp.drop(columns=["code"], errors="ignore")
    
    unemp = unemp.rename(columns=COLUMN_MAPPING)
 
    unemp = unemp.dropna(subset=NUMERIC_COLUMNS, how="all")
    
    return unemp


def load_employment_data():
    """Load and clean employment data from Excel file."""
    emp = pd.read_excel(INPUT_EMPLOYMENT_FILE, header=1)
    
    emp = emp.drop(columns=["code"], errors="ignore")
    
    emp = emp.rename(columns=COLUMN_MAPPING)
    
    emp = emp.dropna(subset=NUMERIC_COLUMNS, how="all")
    
    return emp


def calculate_unemployment_rates(unemp, emp):
    """
    Calculate unemployment rates (%) for each category.
    
    Formula: (unemployed / (employed + unemployed)) * 100
    """
    for col in NUMERIC_COLUMNS:
        unemp[f"{col}_pc"] = (unemp[col] / (emp[col] + unemp[col]) * 100).round(2)
    
    return unemp

# Data Processing

def filter_age_category(unemp, age_category):
    """Filter data by age category and drop the age_category column."""
    filtered = unemp[unemp["age_category"] == age_category].copy()
    return filtered.drop(columns=['age_category'])


def create_rate_dataset(df):
    """Create dataset with unemployment rates (percentages)."""
    rate_df = df.drop(columns=["total", "females", "males", "urban", "rural"], errors="ignore")
    
    rate_df = rate_df.rename(columns={
        "females_pc": "Women",
        "males_pc": "Men",
        "rural_pc": "Rural",
        "urban_pc": "Urban",
        "total_pc": "Total"
    })
    
    return rate_df


def create_absolute_dataset(df):
    """Create dataset with absolute unemployment numbers (in thousands)."""
    absolute_df = df.drop(columns=["total_pc", "females_pc", "males_pc", "urban_pc", "rural_pc"], errors="ignore")
    
    absolute_df = absolute_df.rename(columns={
        "females": "Women",
        "males": "Men",
        "rural": "Rural",
        "urban": "Urban",
        "total": "Total"
    })
    
    return absolute_df


def build_chart_structure(data_dict, unit, y_label, y_suffix, visible_by_default):
    """
    Build the complete chart data structure.
    
    Args:
        data_dict: List of dictionaries with the data points
        unit: Unit of measurement ("%" or "thousands")
        y_label: Y-axis label
        y_suffix: Y-axis suffix
        visible_by_default: List of series to show by default
    
    Returns:
        Dictionary with complete chart structure
    """
    columns = list(data_dict[0].keys()) if data_dict else []
    
    result = {
        "data": data_dict,
        "encoding": {
            "xKey": "period",
            "kind": "line",
            "unit": unit,
            "series": {}
        },
        "axes": {
            "x": {"label": "period"},
            "y": {"label": y_label, "suffix": y_suffix}
        },
        "visibleByDefault": visible_by_default
    }
    
    for category in columns:
        result["encoding"]["series"][category] = {
            "label": category
        }
    
    return result


def main():
    """Main processing function."""

    unemp = load_unemployment_data()
    emp = load_employment_data()
    
    unemp = calculate_unemployment_rates(unemp, emp)
    
    unemp_15_70 = filter_age_category(unemp, AGE_CATEGORY_FILTER)

    unemp_15_70_rate = create_rate_dataset(unemp_15_70)
    unemp_15_70_rate_dict = unemp_15_70_rate.to_dict(orient="records")
    
    result_15_70_rate = build_chart_structure(
        data_dict=unemp_15_70_rate_dict,
        unit="%",
        y_label="Unemployment rate",
        y_suffix="%",
        visible_by_default=["Women", "Men", "Urban", "Rural"]
    )
    
    # Uncomment to write file
    # with open(OUTPUT_RATE_FILE, "w", encoding="utf-8") as f:
    #     json.dump(result_15_70_rate, f, indent=2, ensure_ascii=False)
    

    # Generate Absolute Unemployment Dataset (Thousands)
 
    unemp_15_70_absolute = create_absolute_dataset(unemp_15_70)
    unemp_15_70_absolute_dict = unemp_15_70_absolute.to_dict(orient="records")
    
    print(unemp_15_70_absolute_dict)
    
    result_15_70_absolute = build_chart_structure(
        data_dict=unemp_15_70_absolute_dict,
        unit="thousands",
        y_label="Unemployment",
        y_suffix="thousands",
        visible_by_default=["Women", "Men", "Urban", "Rural"]
    )
    
    # Uncomment to write file
    # with open(OUTPUT_ABSOLUTE_FILE, "w", encoding="utf-8") as f:
    #     json.dump(result_15_70_absolute, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
