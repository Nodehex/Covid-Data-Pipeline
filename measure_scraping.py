import requests
from bs4 import BeautifulSoup
import datefinder
import pandas as pd
wiki = "https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory"

country_url_dict = {
    'France': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_France",
    'Spain': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain",
    'Germany': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Germany",
    'Netherlands': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Netherlands",
    'Czech Republic': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Czech_Republic",
    'Poland': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Poland",
    'Italy': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Italy#Management",
    'United Kingdom': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_Kingdom#Timeline",
    'Ireland': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Republic_of_Ireland",
    'Denmark': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Denmark",
    'Norway': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Norway",
    'Sweden': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Sweden",
    'Finland': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Finland",
    'United States': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States",
    'Canada': "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Canada"
}

df = pd.DataFrame()
print(df)
# country_events = {}
for country in country_url_dict.items():
    print(country[0], country[1])
    request = requests.get(country[1])
    soup = BeautifulSoup(request.text)
    events = []
    timeline = soup.find(id='Timeline').parent
    # print(timeline)
    for elem in timeline.next_siblings:
        if elem.name == 'h2':
            break
        if elem.name != 'p':
            continue
        # matches = list(datefinder.find_dates(elem.text))
        events.append(elem.text)
    df[country[0]] = events
    # country_events[country[0]] = events

# print(country_events)
print(df)
