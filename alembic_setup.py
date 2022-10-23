import argparse
import configparser

parser = argparse.ArgumentParser()

parser.add_argument('--user', dest='user', type=str)
parser.add_argument('--password', dest='password', type=str)
parser.add_argument('--database', dest='database', type=str)

args = parser.parse_args()
user = args.user
password = args.password
host = os.environ.get("DB_HOST", "localhost")
database = args.database
config = configparser.ConfigParser()
config.sections()
config.read('alembic.ini')
connectionString = f"mysql+aiomysql://{user}:{password}@{host}/{database}"
config['alembic']["sqlalchemy.url"] = connectionString


with open('alembic.ini', 'w') as configfile:
    config.write(configfile)