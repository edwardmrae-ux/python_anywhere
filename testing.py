from datetime import datetime

current_day = datetime.today().day
current_month = datetime.today().month
current_year = datetime.today().year

url1 = f"https://basketapi1.p.rapidapi.com/api/basketball/matches/{current_day}/{current_month}/{current_year}"

print(url1)