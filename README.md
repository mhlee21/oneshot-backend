```
# dumpdata
python manage.py dumpdata movies -o movies.json

# loaddata (db 없는 경우 migrate부터 시작)
python manage.py migrate
python manage.py loaddata movies.json
```

# Django Restful API 문서 확인
```
http://127.0.0.1:8000/api/v1/swagger/
```