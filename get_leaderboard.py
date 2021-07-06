
import requests

url='https://golf-leaderboard-data.p.rapidapi.com/leaderboard/25?tournament_id=291'
tour_id = 2
season_id = 2021
tournament_id = 294

print("New Request... \n \n")

'''response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
response = requests.get('https://reqres.in/api/users?')'''

response = requests.get(url, headers = {"x-rapidapi-key": "b88fd41b6amsh5775253c68a3727p1f2f1djsn80959b53b4a8", "x-rapidapi-host": "golf-leaderboard-data.p.rapidapi.com"}, params = {"tournament_id": "291"})


json_response = response.json()

'''
print("Print each key-value pair from JSON response")
for key, value in json_response.items():
    print(key, ":", value)

print(json_response["results"]["tournament"]["name"])

'''

leaderboard = json_response["results"]["leaderboard"]


for item in leaderboard:
    name = item["first_name"] + " " + item["last_name"]
    position = item["position"]
    to_par = item["total_to_par"]




