1.【公開】

・GitHub →https://github.com/kaie28/kaie28-aws-22-django-teisyutu-2

・アプリは、現在閉鎖中


2【概要】

・webアプリ(主にPython、Django)とAWS(Terraform、Docker)を中心に学習し、本番環境と開発環境の各利点とする機能を両立した形でデプロイしました。


3【開発背景】

・旅行や建築の背景から知識や技術を知り、実物に触れ、探求することが趣味です。将来は気軽に参加できる複数のコアなコミュニティ環境を作り、交流したいという夢があります。

・今回は私が好きな「Instagram」のアプリをヒントに、プログラミング言語やAWSを選び、全ての工程を独学で行いました。勉強内容の順序や学習範囲など入念に計画し、特にセキュリティ強化、データ復元の簡易化、コスト面を重視して構築・設計しました。



4【工夫した点】

・本番環境ではDockerでの公開と同時進行で、リアルタイムで開発モードからログによるエラー追跡が出来るように設計にしました。

・セキュリティ強化のため、IPやシークレットキーの変数化や、.env　.gitgnoreを利用し対策しました。

・始めの頃は「手動型」で構築していましたが、デプロイ直前で全てデータが消えてしまった苦い経験から、再チャレンジし「全自動型」へ移行して復元しやすい状態に強化しました。


5【主な設計機能】

アプリのフロントエンド：HTML、CSS、Bootstrap

アプリのバックエンド　：Python、Django

Webサーバー    : Nginx

アプリサーバー : Django（GunicornによるWSGI運用）/ todoアプリ

インフラ管理   : Terraform(AMI,EC2,VPC,Route)の自動化/ SSH,SSM(IAM)

プロセス管理   : django-docker.service（全自動・常駐化管理）

OS(Linux)     :Ubuntu(AWS/Terraform側) , Debian(Docker/Django側)

DB　          :db.sqlite3(開発/本番ともに)

【DBの注意】

開発/本番環境は共に「db.sqlite3」を使用していますが、本番環境では「db\_data」＝コンテナ外の安全金庫（db\_volume）と連携させているので、コンテナが再起動しても「文字・CSS・画像」の情報は安全に保持できる状態にしています。
(※WebサーバーとDjango連携を最速で学習する/無料範囲内での設計を優先したので、この形式にしました)。
今後はRDS連携の導入も検討しています。




6【主要ファイル】

Django(アプリフロントエンド管理) ：templates ,todo

Django(アプリバックエンド管理)　 ：todoproject ,todo

Terraform(インフラ管理)　　　　　:main.tf , variables.tf , outputs.tf

Docker（WEBサーバー/コンテナ管理):nginx , Dockerfaile , docker-compose.yml

Linuxサーバー（全自動化)         :django-docker.service

セキュリティ管理(※非公開) ：terraform.tfstate(全体)、terraform.tfvars(変数)、.env

セキュリティ管理(公開)　 　：.gitgnore

DB管理(※非公開)          ：db.sqlite3




7【インフラ・コンテナの全体的な構成図】




8【今後の課題】

目標：より安全性の高い、多彩な情報を扱えるための機能を搭載する。

・RDS連携(重要な情報を厳重に保管する)

・Lambda(本部屋とは別室での画像加工)

・S3（写真や動画の巨大な倉庫）



以上です。
ここまでご覧いただき、ありがとうございました。














