from collections import defaultdict
from datetime import datetime, timedelta

users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 12)},
    {"name": "Pawel Ciosmak", "birthday": datetime(1984, 4, 9)},
    {"name": "Bruce Willis", "birthday": datetime(1961, 7, 11)},
    {"name": "Pretty Woman", "birthday": datetime(1945, 4, 11)},
    {"name": "Aqua Man", "birthday": datetime(1999, 1, 1)},
    {"name": "Spider Man", "birthday": datetime(1990, 2, 24)}
]

def get_birthdays_per_week(users):

    today = datetime.today().date()
    moved_to_monday = today + timedelta(days=(7 - today.weekday()))
    birthdays_per_week = defaultdict(list)   

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()        
        birthday_this_year = birthday.replace(year=today.year)        
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days       
        birthday_weekday = birthday_this_year.weekday()        
        if birthday_weekday >= 5:
            birthday_weekday = 0  # Monday
        if delta_days < 7 + today.weekday():
            birthday_weekday_name = (moved_to_monday + timedelta(days=birthday_weekday)).strftime("%A")
            birthdays_per_week[birthday_weekday_name].append(name)
    
    if not birthdays_per_week:  
        print("There is noone with bithday this week.")
    else:    
        for day, birthdays in birthdays_per_week.items():
            print(f"{day}: {', '.join(birthdays)}")

get_birthdays_per_week(users)