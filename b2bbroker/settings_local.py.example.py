DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<db_name>',
        'USER': '<user>',
        'PASSWORD': '<password>',
        'HOST': '<host>',
        'PORT': '<port>',
    },
}

ALLOWED_HOSTS = ['127.0.0.1']
