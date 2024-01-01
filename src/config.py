from decouple import config

DB_URL = config('DATABASE_URL')

# JWT
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
ALGORITHM = config('ALGORITHM')

# Admin Creation
ADM_TOKEN_NAME = config('ADM_TOKEN_NAME')
ADM_TOKEN_SUB = config('ADM_TOKEN_SUB')
ADM_TOKEN = config('ADM_TOKEN')
