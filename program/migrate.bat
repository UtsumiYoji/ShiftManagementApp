@echo off
setlocal

for /d %%D in (*) do (
    if exist %%D\migrations (
        echo Deleting %%D\migrations
        rmdir /s /q %%D\migrations
    )
)

endlocal

python ./manage.py makemigrations user
python ./manage.py makemigrations work_location
python ./manage.py makemigrations management
python ./manage.py makemigrations shift
python ./manage.py migrate
python ./manage.py makemigrations
python ./manage.py loaddata fixture.json
@REM python ./manage.py collectstatic
