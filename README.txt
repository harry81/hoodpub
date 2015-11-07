### data migration
```
python /Users/hyunminchoi/Dropbox/work/hoodpub/tools/db_converter.py all_database_151021.sql all_database_151021.psql
```

### run celery
```
python manage.py celery worker --loglevel=DEBUG
```

### nginx ssl setting
http://stackoverflow.com/questions/6783268/django-uwsgi-nginx-ssl/14893209#14893209
