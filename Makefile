up:
	docker-compose up

down:
	docker-compose down

attach:
	docker attach docker attach disasters_notifier_web_1

run_tests:
	docker exec -it disasters_notifier_web_1 python ./manage.py test

makemigrations:
	docker exec -it disasters_notifier_web_1 python ./manage.py makemigrations

migrate:
	docker exec -it disasters_notifier_web_1 python ./manage.py migrate

exec_web:
	docker exec -it disasters_notifier_web_1 /bin/bash

exec_db:
	docker exec -it disasters_notifier_db_1 /bin/bash

linters:
	docker exec -it disasters_notifier_web_1 pylint map/
	docker exec -it disasters_notifier_db_1 pylint users/
	docker exec -it disasters_notifier_db_1 flake8 map/
	docker exec -it disasters_notifier_db_1 flake8 users/



