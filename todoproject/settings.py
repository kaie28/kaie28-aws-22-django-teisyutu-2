
import os
import environ  # ★
from pathlib import Path   #★

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ★ .envファイル(22番でDjangoシークレトキーやEC2のMy IPなど自動で呼び出し)を探して読み込む設定 （ ● このBASE_DIRの下に、下記2行を追記）

env = environ.Env() #★
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) #★


SECRET_KEY = os.getenv('SECRET_KEY')
MY_IP = os.getenv('MY_IP')

DEBUG = True

ALLOWED_HOSTS = [

    os.environ.get('MY_IP', 'localhost'),
    '127.0.0.1',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',

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

ROOT_URLCONF = 'todoproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', 

                ],  #context_processors の閉じカッコ
        },  # oPTIONS の閉じカッコ
    },  # 辞書データの閉じカッコ
]



            
WSGI_APPLICATION = 'todoproject.wsgi:application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_data' / 'db.sqlite3',    
　　　　　#↑～☆☆最新修正で「db_data」に追加する。(＝docker-compose.ymlファイルと連結)で、本番環境でも文字情報が消えない設定にする。
　　　　　#↑　注意(※以前では「db.sqlite3」のみの設定にしてた。＝本番環境では文字消える/開発環境では消えないの設定だったので、危険なので上記に変更した)
 
    }
}


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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
