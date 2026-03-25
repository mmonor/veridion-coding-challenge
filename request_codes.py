import pandas as pd
import requests

df = pd.read_csv("clean_data.csv",names=['domain'])

for domain in df['domain']:

    url = f"https://{domain}"

    try:
        r = requests.get(url,timeout=5)
        print(f"{url} ----> {r.status_code}\n")
    except requests.exceptions.RequestException as e:
        print(f"{url} ----> {e}\n")