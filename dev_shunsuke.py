from tminnovation.settings import *

DEBUG = True


DATABASES = {

       'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'tminnovation',
       'USER': 'shunsuke',
       'PASSWORD': 'shun0210',
       'HOST': '127.0.0.1',
       'POST': '5432'
     }
}


"""

DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
ALLOWED_HOSTS = ['127.0.0.1']
