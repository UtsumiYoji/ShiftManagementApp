python ./manage.py makemigrations user
python ./manage.py makemigrations work_location
python ./manage.py makemigrations management
python ./manage.py migrate
python ./manage.py makemigrations
python ./manage.py loaddata fixture.json
python ./manage.py collectstatic
