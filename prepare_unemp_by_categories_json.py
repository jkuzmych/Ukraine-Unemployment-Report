import pandas as pd
import json
import math

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
    unemp[f"{col}_pc"] = (unemp[col] / (emp[col] + unemp[col]) * 100).round(2)

unemp_formatted = []


#crete three separate dtaaframes for each age group(so every data point would have only one data for each period)
#unemp_15_years_and_over = unemp[unemp["age_category"] == "15 years and over"].copy().drop(columns=['age_category'])

unemp_15_70 = unemp[unemp["age_category"] == "15-70 years"].copy().drop(columns=['age_category'])

#unemp_working_age = unemp[unemp["age_category"] == "working age"].copy().drop(columns=['age_category'])

#writing json with unemployment rate data 15-70
unemp_15_70_rate = unemp_15_70.drop(columns=["total", "females", "males", "urban", "rural"], errors="ignore")
unemp_15_70_rate = unemp_15_70_rate.rename(columns={
    "females_pc": "Women",
    "males_pc": "Men",
    "rural_pc": "Rural",
    "urban_pc": "Urban",
    "total_pc": "Total"
})

unemp_15_70_rate_dict = unemp_15_70_rate.to_dict(orient="records")

result_15_70_rate = {
    "data":unemp_15_70_rate_dict,
    "encoding": {
        "xKey": "period",
        "kind": "line",
        "unit": "%",
        "series": {}
    },
    "axes": {
        "x": {"label": "period"},
        "y": {"label": "Unemployment rate", "suffix": "%"}
    },
    "visibleByDefault": [
        "Women", "Men", "Urban", "Rural"
    ]
}

for category in unemp_15_70_rate.columns:
    result_15_70_rate["encoding"]["series"][category]={
        "label": category
    }


# with open("frontend/uud/public/data/unrate_by_social_group.json", "w", encoding="utf-8") as f:
#     json.dump(result_15_70_rate, f, indent=2, ensure_ascii=False)

#writing json with unemployment data 15-70
unemp_15_70 = unemp_15_70.drop(columns=["total_pc", "females_pc", "males_pc", "urban_pc", "rural_pc"], errors="ignore")
unemp_15_70 = unemp_15_70.rename(columns={
    "females": "Women",
    "males": "Men",
    "rural": "Rural",
    "urban": "Urban",
    "total": "Total"
})

unemp_15_70_dict = unemp_15_70.to_dict(orient="records")

print(unemp_15_70_dict)

result_15_70 = {
    "data":unemp_15_70_dict,
    "encoding": {
        "xKey": "period",
        "kind": "line",
        "unit": "%",
        "series": {}
    },
    "axes": {
        "x": {"label": "period"},
        "y": {"label": "Unemployment", "suffix": "thousands"}
    },
    "visibleByDefault": [
        "Women", "Men", "Urban", "Rural"
    ]
}

for category in unemp_15_70.columns:
    result_15_70["encoding"]["series"][category]={
        "label": category
    }

# with open("frontend/uud/public/data/unemployment_by_social_group.json", "w", encoding="utf-8") as f:
#     json.dump(result_15_70, f, indent=2, ensure_ascii=False)

# #helper function to write json
# def write_json(df, output_path):
#     df.to_json(output_path, orient="records", indent=2)

# def generic_write_json(data, output_path):
#     json_data = json.dumps(data, indent=2)
#     with open(output_path, "w") as f:
#         f.write(json_data)
 

#dataframe to json 
# write_json(unemp_15_years_and_over, 
#             "frontend/uud/public/data/unemployment_15_years_and_over.json")

# write_json(unemp_15_70_years, 
#             "frontend/uud/public/data/unemployment_15_70_years.json")

# write_json(unemp_working_age, 
#             "frontend/uud/public/data/unemployment_working_age.json")

#write nested json (grouped by number_data and rate_data)
# def format_period_dict(row, columns):
#     result = {}
#     result['number_data'] = {}
#     result['rate_data']   = {}
#     result['period']      = row['period'].values[0]
#     for column in columns:
#         if column.endswith('_pc'): 
#             result['rate_data'][column] = float(row[column].values[0])
#         else:
#             result['number_data'][column] = float(row[column].values[0])
#     return result

# def format_df(df, indexes, columns):
#     result = []
#     for i in indexes:
#         result.append(format_period_dict(df.loc[[i]], columns))
#     return result

# indexes = unemp_working_age.index.values
# columns = unemp_working_age.columns.tolist()[1:]


# unemp_working_age_jsonlike = format_df(df=unemp_working_age, indexes=indexes, columns=columns)

# generic_write_json(unemp_working_age_jsonlike, 
#              "frontend/uud/public/data/unemployment_working_age.json")
