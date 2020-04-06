import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qXp42c5sLk8m3NL6'