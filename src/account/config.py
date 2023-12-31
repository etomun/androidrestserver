from decouple import config

# JWT
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ATE_MINUTES = config('ACCESS_TOKEN_EXP_MINUTES', default=30, cast=int)
RTE_DAYS = config('REFRESH_TOKEN_EXP_DAYS', default=3, cast=int)

# Account
CREATE_ADMIN_KEY = config('CREATE_ADMIN_KEY')
