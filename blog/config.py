import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:mypassword@localhost:5432/blog'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
