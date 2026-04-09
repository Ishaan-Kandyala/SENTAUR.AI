from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import Users
from backend.weather import get_weather, outfit_for
from backend.emailer import send_email

def send_daily_updates():
    for user in Users.select():
        weather = get_weather(user.city)
        temp = weather["main"]["temp"]
        outfit = outfit_for(temp)

        body = f"""
Good morning!

Today's temperature in {user.city}: {temp}°C
Suggested outfit: {outfit}

Have a great day!
"""
        send_email(user.email, "Your Daily Weather & Outfit", body)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_updates, "cron", hour=7, minute=0)
    scheduler.start()