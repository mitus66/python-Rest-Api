# quotes_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from mongoengine import connect, get_connection

# Вказуємо параметри підключення до MongoDB
# Використовуйте рядок підключення, якщо у вас він є, інакше просто ім'я бази даних
# Завантажуємо змінні оточення з файлу .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-@e^z+a92m0x^$v-v-@y$1$c)p43q7^d&0o(s0^1#*!_@^e&1x'
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authors',
    'quotes',
    'users',
    # ...
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quotes_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # <-- Переконайтеся, що тут стоїть True
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quotes_project.wsgi.application'

# Налаштування для сесій, якщо вони потрібні
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uk-ua' # Змінено на українську

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'users:login'


# Звідси починається логіка підключення до MongoDB
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("Помилка: MONGO_URI не знайдено у змінних оточення. Перевірте файл .env")
    # Якщо рядок підключення відсутній, ми все одно намагаємося підключитися до localhost,
    # щоб не зупиняти додаток повністю, але ви отримаєте помилку підключення.
    # Це допоможе вам зрозуміти, що проблема саме в MONGO_URI.
    connect(host="mongodb://localhost:27017")
else:
    connect(host=MONGO_URI)
    print("Успішно підключено до MongoDB Atlas!")

'''Цей рядок налаштовує Django для виведення електронних листів у консоль. 
   Це зручно для тестування, щоб не налаштовувати реальний SMTP-сервер.'''
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'