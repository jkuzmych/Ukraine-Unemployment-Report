"""
Process unemployment data by regions.

This script:
1. Loads unemployment data by regions from Excel file
2. Transforms data into pivot table format (years as rows, regions as columns)
3. Generates JSON file for unemployment rates by region visualization
"""

import json
import math
import pandas as pd

# Configuration

INPUT_FILE = "data/Unemployed 2008-2021 by Regions.xlsx"
OUTPUT_FILE = "frontend/uud/public/data/unemployment_by_region.json"

COLUMN_MAPPING = {
    "attributes": "region",
    "period": "year",
    "data": "unrate"
}

# Data Loading and Cleaning

def load_data():
    """Load unemployment data from Excel file."""
    unemp = pd.read_excel(INPUT_FILE)
    
    unemp = unemp.drop(columns=["code"], errors="ignore")
    
    unemp = unemp.rename(columns=COLUMN_MAPPING)
    
    return unemp


def convert_numeric_columns(df):
    """
    Convert columns to numeric, replacing commas with dots.
    
    Args:
        df: DataFrame with columns to convert
    
    Returns:
        DataFrame with numeric columns
    """
    # Get all columns except 'region'
    num_cols = df.columns.difference(["region"])
    
    # Replace commas with dots and convert to numeric
    df[num_cols] = df[num_cols].apply(
        lambda col: pd.to_numeric(
            col.astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        )
    )
    
    return df

# Data Transformation

def pivot_data(df):
    """
    Reshape data to pivot table format: years as rows, regions as columns.
    
    Args:
        df: DataFrame with columns: year, region, unrate
    
    Returns:
        Pivoted DataFrame with years as index and regions as columns
    """
    pivoted = (
        df
        .pivot_table(
            index="year",
            columns="region",
            values="unrate"
        )
        .reset_index()
    )
    
    return pivoted


def remove_nan_values(data_dict):
    """
    Remove NaN values from data records.
    
    Args:
        data_dict: List of dictionaries with data points
    
    Returns:
        List of dictionaries with NaN values removed
    """
    for year_data in data_dict:
        for region_key in list(year_data.keys()):
            if math.isnan(year_data[region_key]):
                year_data.pop(region_key)
    
    return data_dict

# Chart Structure Building

def build_chart_structure(data_dict, columns):
    """
    Build the complete chart data structure.
    
    Args:
        data_dict: List of dictionaries with the data points
        columns: List of column names (excluding 'year')
    
    Returns:
        Dictionary with complete chart structure
    """
    result = {
        "data": data_dict,
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
        "visibleByDefault": ["Ukraine"]
    }
    
    for region in columns:
        result["encoding"]["series"][region] = {
            "label": region
        }
    
    return result


def main():
    """Main processing function."""
    # Load and clean data
    unemp = load_data()
    unemp = convert_numeric_columns(unemp)
    
    # Transform to pivot table format
    unemp = pivot_data(unemp)
    
    # Convert to dictionary format
    unemp_dict = unemp.to_dict(orient="records")
    
    # Remove NaN values
    unemp_dict = remove_nan_values(unemp_dict)
    
    # Build chart structure
    # Get all columns except 'year'
    region_columns = [col for col in unemp.columns if col != "year"]
    result = build_chart_structure(unemp_dict, region_columns)
    
    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
