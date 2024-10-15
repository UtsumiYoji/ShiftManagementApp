set -e

for dir in */; do
    if [ -d "$dir/migrations" ]; then
        echo "Deleting $dir/migrations"
        rm -rf "$dir/migrations"
    fi
done

python3 ./manage.py makemigrations user
python3 ./manage.py makemigrations work_location
python3 ./manage.py makemigrations management
python3 ./manage.py makemigrations shift
python3 ./manage.py migrate
python3 ./manage.py makemigrations
python3 ./manage.py loaddata fixture.json
python3 ./manage.py collectstatic --noinput
