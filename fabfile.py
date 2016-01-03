# -*- coding: utf-8 -*-
import requests
import time
from fabric.api import *
from fabric.contrib.console import confirm
from sys import platform as _platform



env.user = 'hoodpub'
env.hosts = ['www.hoodpub.com']
env.use_ssh_config = True


def host_type():
    run('uname -s')


def flake8():
    local('cd web; flake8 hoodpub book')


def tests():
    local('cd web; REUSE_DB=1 python manage.py test -v3 book hoodpub')


def tests_facebook_read(read_check=True):
    if read_check == 'no':
        return
    local('cd web; python manage.py check_facebook_read')


def diff_pip():
    if _platform == "darwin":
        local("cd web; diff <(cat requirements.txt | sort) <(pip freeze | sort)", shell='/bin/bash')

def db_backup():
    name = 'hoodpub_db_%s.sql' % time.strftime("%Y-%m-%d")
    run('pg_dump hoodpub  -h localhost -U mycms_user  > /tmp/%s' % name)
    get('/tmp/%s' % name, 'db/%s' % name)

def db_recreate():
    local('psql postgres -h postgres -U mycms_user -c "drop database hoodpub"')
    local('psql postgres -h postgres -U mycms_user -c "create database hoodpub"')
    local('psql hoodpub -U mycms_user  -h postgres < ../db/hoodpub_db_2015-11-13.sql')

def host_ping():
    res = requests.get('https://www.hoodpub.com/book/899517045X/#/')
    if res.status_code != 200:
        return confirm('SERVER is NOT RESPONDING NOW! YOU\'RE AWARE OF IT?', default=True)

def host_app_restart():
    run('/etc/init.d/hoodpub2-uwsgi stop')
    host_app_start()


def host_app_start():
    # run('rm /home/hoodpub/work/hoodpub/run/uwsgi*')
    run('/etc/init.d/hoodpub2-uwsgi start')


def host_celery_restart():
    with prefix('source /home/hoodpub/.virt_env/hoodpub2/bin/activate'):
        with shell_env(DB_NAME='hoodpub',
                       DB_USER='mycms_user',
                       DB_PASS='mycms_pass',
                       DB_SERVICE='postgres',
                       DB_PORT='5432'):
            run('/etc/init.d/celeryd restart')


def tag_newrelic():
    sha1 = local('git rev-parse --short HEAD', capture=True)
    msg = local('git log -1 --pretty=%B', capture=True)
    dict_obj = {
        'key': 'a8a9c629f2f123adbb9855a7d82e33918e92b5447712c07',
        'app_name': 'hoodpub',
        'description': '%s[%s-%s]' % (msg, sha1, time.strftime("%Y-%m-%d")),
        }
    local('curl -H "x-api-key:{key}" -d "deployment[app_name]={app_name}"\
    -d "deployment[description]={description}"\
    https://api.newrelic.com/deployments.xml'.format(**dict_obj))


def git_diff():
    res = local("git fetch origin; git diff origin/master", capture=True)
    if res:
        return confirm('You have unmerged changes. Do you want to keep going?', default=True)
    return True

def put_newrelic_config():
    put('newrelic/newrelic-plugin.cfg',
        'work/hoodpub/newrelic/')
    with prefix('source /home/hoodpub/.virt_env/hoodpub2/bin/activate'):
        with cd('/home/hoodpub/work/hoodpub/web'):
            run('git fetch -p')

def deploy(sha=None, read_check=True):
    diff_pip()
    flake8()
    tests()
    tests_facebook_read(read_check)
    if not git_diff():
        return

    put('web/main/settings_local.py',
        'work/hoodpub/web/main/')
    with prefix('source /home/hoodpub/.virt_env/hoodpub2/bin/activate'):
        with cd('/home/hoodpub/work/hoodpub/web'):
            run('git fetch -p')
            sha = sha if sha else 'origin/master'
            run('git reset --hard %s' % sha)
            run('pip install -r requirements.txt')
            with shell_env(DB_NAME='hoodpub',
                           DB_USER='mycms_user',
                           DB_PASS='mycms_pass',
                           DB_SERVICE='postgres',
                           DB_PORT='5432'):
                run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')
                run('/etc/init.d/hoodpub2-uwsgi stop')
                run('rm -rf ../run/*')
                run('/etc/init.d/hoodpub2-uwsgi start')
    run('curl http://www.hoodpub.com/ -H \"Host: www.hoodpub.com\"> /dev/null')
    tag_newrelic()
    host_ping()
