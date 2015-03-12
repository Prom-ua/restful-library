import os


SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'oijOIJouhitac8e658765r7UTfjhb'
)

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5433/libraryapi'
)
