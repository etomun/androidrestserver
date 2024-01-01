from decouple import config

# JWT
ATE_MINUTES = config('ACCESS_TOKEN_EXP_MINUTES', default=30, cast=int)
RTE_DAYS = config('REFRESH_TOKEN_EXP_DAYS', default=3, cast=int)