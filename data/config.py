import os

print(os.environ.items())
print(os.environ['BOT_TOKEN'], os.environ['DATABASE_URL'])
BOT_TOKEN = os.environ['BOT_TOKEN']
POSTGRES_URI = os.environ['DATABASE_URL']
