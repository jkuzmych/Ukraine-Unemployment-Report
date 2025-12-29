import pandas as pd

#load unemployment data
unemp = pd.read_excel(
    "data/Unemployed 2015-2021 by Quarter Ukraine.xlsx",
    header=1
)

#drop "code" column in unemployment data
unemp = unemp.drop(columns=["code"], errors="ignore")

#rename columns to avoid spaces
unemp = unemp.rename(columns={
    "atributes": "age_category",
    "total population": "total",
    "urban area": "urban",
    "rural area": "rural"
})

#drop rows wehere all numeric values are "NA"
unemp_numeric_cols = ["total", "females", "males",
                "urban", "rural"]
unemp = unemp.dropna(subset=unemp_numeric_cols, how="all")

#load employment data
emp = pd.read_excel(
    "data/Employed 2015-2021 by Quarter Ukraine.xlsx",
    header=1
)

#drop "code" column in employment data
emp = emp.drop(columns=["code"], errors="ignore")

#rename columns to avoid spaces
emp = emp.rename(columns={
    "attributes": "age_category",
    "total population": "total",
    "urban area": "urban",
    "rural area": "rural"
})

#drop rows wehere all numeric values are "NA"
emp_numeric_cols = ["total", "females", "males",
                "urban", "rural"]
emp = emp.dropna(subset=emp_numeric_cols, how="all")

#calculate %(pc) of unemployment in every category by formula (unemp/(unemp+emp)*100)
for col in ["total", "females", "males", "urban", "rural"]:
    unemp[f"{col}_pc"] = unemp[col] / (emp[col] + unemp[col]) * 100

# Round all columns ending with _pc to 2 decimal places
pc_columns = [col for col in unemp.columns if col.endswith("_pc")]
for col in pc_columns:
    unemp[col] = unemp[col].round(2)

#crete three separate dtaaframes for each age group(so every data point would have only one data for each period)
unemp_15_years_and_over = unemp[unemp["age_category"] == "15 years and over"].copy().drop(columns=['age_category'])

unemp_15_70_years = unemp[unemp["age_category"] == "15-70 years"].copy().drop(columns=['age_category'])

unemp_working_age = unemp[unemp["age_category"] == "working age"].copy().drop(columns=['age_category'])

#helper function to write json
def write_json(df, output_path):
    df.to_json(output_path, orient="records", indent=2)
 

#dataframe to json with blank lines between records
write_json(unemp_15_years_and_over, 
            "frontend/uud/public/data/unemployment_15_years_and_over.json")

write_json(unemp_15_70_years, 
            "frontend/uud/public/data/unemployment_15_70_years.json")

write_json(unemp_working_age, 
            "frontend/uud/public/data/unemployment_working_age.json")
