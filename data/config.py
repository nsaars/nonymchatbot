import pathlib
from dotenv import dotenv_values

env_file = str(pathlib.Path(__file__).parent.resolve()) + r'\.env'
config = dotenv_values(env_file)

IP = config['IP']
PORT = config['PORT']
PG_USER = config['PG_USER']
PG_PASS = config['PG_PASS']
DATABASE = config['DATABASE']
BOT_TOKEN = config['BOT_TOKEN']
ADMINS = (732928701,)

POSTGRES_URI = f'postgres://{PG_USER}:{PG_PASS}@{IP}:{PORT}/{DATABASE}'

