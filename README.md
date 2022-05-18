```
# dumpdata
python manage.py dumpdata movies -o movies.json

# loaddata (db 없는 경우 migrate부터 시작)
python manage.py migrate
python manage.py loaddata movies.json
```