from os import urandom

IS_DEBUG = True

DB_CONNECTION_STRING = "sqlite://:memory:"
JWT_KEY = urandom(32)
AUTH_JWT_TTL = 86400 * (7 if IS_DEBUG else 1)
BCRYPT_ROUNDS = 5 if IS_DEBUG else 13
