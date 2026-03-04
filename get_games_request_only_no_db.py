import requests
from datetime import datetime
from datetime import timedelta
import mysql.connector


now = datetime.now()
now_EDT = now - timedelta(hours=4)

#print(now_EDT)

'''now = datetime.strptime('2021-07-15 20:15:00', '%Y-%m-%d %H:%M:%S')'''


#Games API call
url = "https://api-basketball.p.rapidapi.com/games"

querystring = {"timezone":"America/New_York","season":"2022-2023","league":"116","date":"2023-03-16"}

headers = {
    'x-rapidapi-host': "api-basketball.p.rapidapi.com",
    'x-rapidapi-key': "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8"
}

response = requests.request("GET", url, headers=headers, params=querystring)

json_response = response.json()
games = json_response["response"]

print("json response:")
print(games)

