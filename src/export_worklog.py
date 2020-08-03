import datetime
import json
import requests

URL = "https://jira.example.com"
USER = "admin"
PASSWORD = "password"

AUTH = requests.auth.HTTPBasicAuth(USER, PASSWORD)

def get_ids(data):
    return [x["worklogId"] for x in data["values"]]

def get_worklog_records(ids):
    url = "%s/rest/api/2/worklog/list" % URL
    data = {"ids": ids}
    headers = {"content-type": "application/json"}
    r = requests.post(url, json=data, headers=headers, auth=AUTH)
    return r.json()

res = []
url = "%s/rest/api/2/worklog/updated?since=0" % URL
while url:
    r = requests.get(url, auth=AUTH)
    data = r.json()
    url = data.get("nextPage")
    ids = get_ids(data)
    res.append(get_worklog_records(ids))

fn = "data/worklog.json"
f = open(fn, "wt")
f.write(json.dumps(res, indent=2))
f.close()
