import pandas as pd

def get_alpha3(data_dir, file_name):

    alpha3 = pd.read_csv(f"{data_dir}/{file_name}.csv")
    pattern = {",": "","ç": "c", "ô": "o", "’": "'", "é": ""}
    alpha3["Country or Area"] = alpha3["Country or Area"].replace(pattern, regex=True)
    alpha3["Country or Area"] = alpha3["Country or Area"].str.replace("\(.*\)", "",regex=True)
    alpha3["Country or Area"] = alpha3["Country or Area"].str.replace("\s+the", "",regex=True)
    alpha3["Country or Area"] = alpha3["Country or Area"].str.strip()
    alpha3 = alpha3.set_index("Country or Area")
    alpha3 = alpha3["ISO-alpha3 code"]

    country_fixes = {"Czech Republic": "CZE", "World": "World", "Brunei": "BRN", "Vatican": "VAT", "United States": "USA", "United Kingdom": "GBR",
                     "International": "International", "Tanzania": "TZA", "Kosovo": "RKS","Taiwan": "TWN", "Laos": "LAO", "Syria": "SYR",
                     "Moldova": "MDA", "South Korea": "KOR", "Palestine": "PSE", "Russia": "RUS", "Sint Maarten (Dutch part)": "SXM",
                     "Saint Vincent and the Grenadines": "VCT", "Bonaire, Sint Eustatius and Saba": "BES", "Saint Barthelemy": "BLM",
                     "Reunion": "REU"
                     }
    country_fixes = pd.Series(country_fixes)
    alpha3 = alpha3.append(country_fixes)
    return alpha3

if __name__ == "__main__":
    print("Run from main.py")