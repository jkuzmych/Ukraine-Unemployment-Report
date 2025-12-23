import pandas as pd

#load data
df = pd.read_excel(
    "data/Unemployed 2015-2021 by Quater Ukraine.xlsx",
    header = 1
)


#drop "code" column
df = df.drop(columns = ["code"], errors = "ignore")


#rename remaining columns
df = df.rename(columns={
    "atributes": "age_category",
    "period": "label",
    "total population": "total_unemployed",
    "females": "unemployed_female",
    "males": "unemployed_male",
    "urban area": "unemployed_urban",
    "rural area": "unemployed_rural"
})

#split "period" into year and quarter
df["year"] = (
    df["label"]
    .str.extract(r"(\d{4})", expand = False)
    .astype("Int16")
)

df["quarter"] = (
    df["label"]
    .str.extract(r"Q([1-4])", expand = False)
    .astype("Int8")
)


#create 3 dataframe by atribute

df_15_years_and_over = df[df["age_category"] == "15 years and over"].copy()
df_15_years_and_over = df_15_years_and_over.drop(columns=['age_category'])

numeric_cols = ["total_unemployed", "unemployed_female", "unemployed_male",
                "unemployed_urban", "unemployed_rural"]

#delete all rows with all NA values
df_15_years_and_over = df_15_years_and_over.dropna(subset=numeric_cols, how="all")


df_15_70_years = df[df["age_category"] == "15-70 years"].copy()
df_15_70_years = df_15_70_years.drop(columns=['age_category'])

df_working_age = df[df["age_category"] == "working age"].copy()
df_working_age = df_working_age.drop(columns=['age_category'])

#dataframe to json
df_working_age.to_json("data/json/unemployment_working_age.json",
            orient="records",
            indent=2)


