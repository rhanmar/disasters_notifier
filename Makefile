build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

attach:
	docker attach disasters_notifier_web_1

tests:
	docker exec -it disasters_notifier_web_1 python ./manage.py test

make_migrations:
	docker exec -it disasters_notifier_web_1 python ./manage.py makemigrations

migrate:
	docker exec -it disasters_notifier_web_1 python ./manage.py migrate

show_migrations:
	docker exec -it disasters_notifier_web_1 python ./manage.py showmigrations

show_urls:
	docker exec -it disasters_notifier_web_1 python ./manage.py show_urls

exec_web:
	docker exec -it disasters_notifier_web_1 /bin/bash

exec_db:
	docker exec -it disasters_notifier_db_1 /bin/bash

linters:
	docker exec -it disasters_notifier_web_1 pylint map/
	docker exec -it disasters_notifier_db_1 pylint users/
	docker exec -it disasters_notifier_db_1 flake8 map/
	docker exec -it disasters_notifier_db_1 flake8 users/

run_telegram_bot:
	docker exec -it disasters_notifier_web_1 python ./manage.py run_tg_bot

create_superuser:
	docker exec -it disasters_notifier_web_1 python ./manage.py createsuperuser

shell:
	docker exec -it disasters_notifier_web_1 python ./manage.py shell

