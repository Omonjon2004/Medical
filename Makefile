unt:
	pip uninstall $(name)
    #make uns name=your_uninstall
mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser --username $(username)
    # make user username=your_username
sort:
	black .
	isort .

base:
	pip freeze > base.txt

app:
	python3 manage.py startapp $(name)
    # make app name=mynewapp
shell:
	python manage.py shell
ist:
	pip install $(name)
	#make ins name=install_name
test:
	python3 manage.py test
collect:
	python3 manage.py collectstatic

freeze:
	pip freeze > requirements/base.txt
