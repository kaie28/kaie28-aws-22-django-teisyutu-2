
import os　#　1★
import environ  # 1★django-environライブラリを使うので。
from pathlib import Path   #　1★

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


##　1【大元の流れ】本番デプロイでのIPなど変数化の仕組み
# .tfvars ➔ .env ➔ settings.pyファイルが一時期本物にすり替わったenvファイルからコピーする→　本物のMY_IPを得る ➔ ALLOWED_HOSTS という箱に保管する　という流れ。
# ★22番SSHトンネル(自分専用ポート番号)から入り、vpcへ入る。
# ★.tfvarsファイルが本物　envファイルはダミー。
#.tfvarsファイルで救い上げた本物の内容(IPやシークレットキーなど)が、一時的にenvファイルに はめ込まれる。
#それをsettings.pyファイルは、一時期本物にすり替わったenvファイルからコピーして、本物を得る流れになる。


#1-1 大まかな指示★settings.pyファイルが、一時的に本物にすり替わった.envファイル内容を探して読み込む設定 （★★このBASE_DIRの下に、下記2行を追記）
env = environ.Env() 
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) 


#1-2 具体的指示★上記にある1-1の流れと同じで、settings.pyファイルが、一時的に本物になっているenvファイル(シークレットキーやIP）をコピーしに行く)ver
SECRET_KEY = env('SECRET_KEY', default= '')　　#←シークレットキーを変数化にして本物公開の危険性を防ぐ。
MY_IP = env('MY_IP', default='127.0.0.1') 　　　#←変数化（IP）、変数がないときはデフォルトで127.0.0.1（＝世界共通ローカルIP)で反映させて「エラー予防


#1-3 DEBUGでの支持★唯一このDEBUGだけは、envファイルには本物の情報が記入されているので、.tfvarsファイルを通さずに、envファイルから直接本物の情報をコピーして組み込む。
DEBUG = env.bool('DEBUG', default=False)　　　


#1-4 コピーした本物を保管する箱★一時的に本物になっている.envファイルからsettings.pyファイルがコピーしてきた「本物IP」などを入れる箱(ALLOWED_HOSTS)の定義。
#即ち、コピーして得られた本物の情報は、内装系のDjangoアプリ内で保管することになる。

ALLOWED_HOSTS = [
    MY_IP,               # ← 一時的に本物になった .envファイル からsettings.pyファイルがコピーする。そのコピーした本物IPなどを保管する箱」
    'localhost',         # ←サーバー自身の、内部通信の専用の名前(★住所名を示す)　　　→実際通るDjango内線★ポート番号(★部屋・玄関番号)である(localhost:8000)とも繋がる。
    '127.0.0.1',　　　　　# ←サーバー自身の、内部通信の★住所番号(127.0.0.1)　＝IP（世界共通ローカルIP)　

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



# 2  外部からDjangoの内部の玄関窓口から、WSGIで仲介（翻訳）させるための設定。
#また、DATABASES の正体（翻訳された文字を保管する場所）
# todoproject.wsgi は翻訳ルールが書かれたファイル」の★場所を示す。
# :application　は翻訳処理を行う「担当プログラム（窓口）」の★名前を示す。

WSGI_APPLICATION = 'todoproject.wsgi:application'


# 3 Docker(コンテナ)が再構築されたり、破壊されても、以前の投降したToDoアプリの文字データ（タスクの内容など）が、絶対に消えないようにするための安全な保管庫の住所を設定。
#★★「db_data」を追加する。(＝docker-compose.ymlファイルと連結する)で、本番環境でも★文字情報が消えない設定にする。
#【補足】docker-compose.ymlファイル（db_volume）を、Djangoのデータ置き場（/usr/src/app/db_data/）にガチッと連結するさせているので・・。
#　注意(※以前では「db.sqlite3」のみの設定にしてたが、＝本番環境では文字消える/開発環境では消えないの設定だったので、危険なので★上記に急遽、変更した)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',　　　　　　
        'NAME': BASE_DIR / 'db_data' / 'db.sqlite3',    #　←★Dockerの標準機能である 「ボリュームマウント（Volume Mount）を使用する。コンテナの外（現実世界）と中（コンテナの世界）を繋ぐため、文字が消えない設定に出来る。
　　　　　
 
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
