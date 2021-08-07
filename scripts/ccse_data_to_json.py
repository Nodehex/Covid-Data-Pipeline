import os
import json
import pandas as pd

def merge_provinces(country_name, df):
        country = df.loc[[country_name]].drop(columns=["Province/State"])
        country = country.sum(axis=0).rename(country_name)
        df = df.drop([country_name]).append(country)
        return df

def ccse_data_to_json(csv_dir, json_dir, file_name, alpha3, csv_file_name):

    df = pd.read_csv(f"{csv_dir}/{csv_file_name}.csv", index_col=0)
    df = df.drop(columns=["Lat", "Long"])

    df = df.reset_index().set_index("Country/Region")
    df = df.rename({"Congo (Brazzaville)": "Congo", "Congo (Kinshasa)": "Democratic Republic of Congo"})

    # Dropping non country columns.
    df = df.drop(["Diamond Princess", "MS Zaandam", "Summer Olympics 2020"])

    # Merge countries with provinces into a single row.
    merge_countries_list = ["China", "Australia", "Canada"]
    for merge_country in merge_countries_list:
        df = merge_provinces(merge_country, df)

    mask = (df["Province/State"] != "0") & (pd.isnull(df["Province/State"]) != True)
    df2 = df.loc[mask]
    df2 = df2.set_index("Province/State")
    df2.index = df2.index.rename("Country/Region")

    df = df[(df["Province/State"] == "0") | (pd.isnull(df["Province/State"]) == True)]

    df = df.append(df2)
    df = df.drop(columns="Province/State")

    df = df.stack().reset_index(level=1)
    df = df.rename(columns={"level_1": "date", 0: "recovered"})

    df["date"] = pd.to_datetime(df["date"]).apply(lambda x: x.strftime("%Y-%m-%d"))

    df = df.rename({"Cabo Verde": "Cape Verde", "US": "United States", "West Bank and Gaza": "Palestine", "Burma": "Myanmar",
                    "Channel Islands": "Jersey", "Holy See": "Vatican", "Korea, South": "South Korea",
                    "Falkland Islands (Islas Malvinas)": "Falkland Islands", "Falkland Islands (Malvinas)": "Falkland Islands",
                    "Sint Maarten": "Sint Maarten (Dutch part)", "Taiwan*": "Taiwan", "St Martin": "Saint Martin",
                    "Wallis and Futuna": "Wallis and Futuna Islands",
                    "Saint Helena, Ascension and Tristan da Cunha": "Saint Helena" })

    df["Country"] = df.index.get_level_values(0)
    df["alpha3"] = df["Country"].map(alpha3)
    # df = df.drop(columns="Country")

    if df["alpha3"].isnull().values.any():
        # DEBUG
        df[df.isnull().any(axis=1)].to_csv(f"{csv_dir}/debug.csv", index=False)
        raise ValueError(f"An Alpha3 value is null in the John Hopkins Recovery Data!")

    data = {}
    for group in df.groupby(level=0):
        data[group[0]] = {
            "alpha3": group[1]["alpha3"].unique()[0],
            "recovered": group[1][["date", "recovered"]].values.tolist()
        }

    open(f"{json_dir}/{file_name}.json", "w").write(json.dumps(data))

if __name__ == "__main__":
    print("run this from main.py")