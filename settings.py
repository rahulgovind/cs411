from dotenv import dotenv_values

_env = dotenv_values(".env")

DB_HOST = _env['DB_HOST']
DB_PORT = _env['DB_PORT']
DB_DATABASE = _env['DB_DATABASE']
DB_USERNAME = _env['DB_USERNAME']
DB_PASSWORD = _env['DB_PASSWORD']
SECRET_KEY = _env['SECRET_KEY']
