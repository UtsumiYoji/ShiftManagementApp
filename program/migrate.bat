python ./manage.py makemigrations user
python ./manage.py makemigrations store
python ./manage.py makemigrations management
python ./manage.py migrate
python ./manage.py makemigrations
python ./manage.py loaddata fixture.json
