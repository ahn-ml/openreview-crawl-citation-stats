import requests
import openreview
import pandas as pd
from tqdm import tqdm


conf_year = input("put Year")

venue_id = f"ICLR.cc/{conf_year}/Conference/"

client = openreview.Client(baseurl='https://api.openreview.net')
# Single-blind venues

# API V1 (Double Blind Submissions)
submissions = client.get_all_notes(invitation=f"{venue_id}-/Blind_Submission")

api_key = ...
url = "https://api.scrapingdog.com/google_scholar"

params = {
    "api_key": api_key,
    "query": "",
}

paper_titles = []
citation_statistics = []


for submission in tqdm(submissions):
    if "Submitted" in submission.content["venue"]:
        continue
    else:
        paper_title = submission.content["title"]
        paper_titles.append(paper_title)
        params["query"] = "intitle:"+paper_title
        response = requests.get(url, params=params)
        while(response.status_code != 200):
            response = requests.get(url, params=params)
        data = response.json()
        if data['scholar_results'][0]['inline_links']['cited_by']['total'] == 'Related articles':
            citation_statistics.append(0)
        else:
            _, _, val = data['scholar_results'][0]['inline_links']['cited_by']['total'].split(" ")
            citation_statistics.append(int(val))



stats = {'name': paper_titles, 'num_citation': citation_statistics}
     
df = pd.DataFrame(stats)
df = df.sort_values(by=['num_citation'], ascending=False)

df.to_csv(f'ICLR-{conf_year}-citation_stats.csv')

