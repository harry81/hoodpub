### data migration
```
python /Users/hyunminchoi/Dropbox/work/hoodpub/tools/db_converter.py all_database_151021.sql all_database_151021.psql
```

### run celery
```
python manage.py celery worker --loglevel=DEBUG
```
