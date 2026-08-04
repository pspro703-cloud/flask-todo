import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqllite:///instance/todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TODOS_PER_PAGE =10