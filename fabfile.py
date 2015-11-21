from fabric.api import *
import time

env.user = 'hoodpub'
env.hosts = ['www.hoodpub.com']
env.use_ssh_config = True


def host_type():
    run('uname -s')

def flake8():
    local('cd web; flake8 hoodpub book')

def tests():
    local('cd web; REUSE_DB=1 python manage.py test -v3 book hoodpub')


def db_backup():
    name = 'hoodpub_db_%s.sql' % time.strftime("%Y-%m-%d")
    run('pg_dump hoodpub  -h localhost -U mycms_user  > /tmp/%s' % name)
    get('/tmp/%s' % name, 'db/%s' % name)

def db_recreate():
    local('psql postgres -h postgres -U mycms_user -c "drop database hoodpub"')
    local('psql postgres -h postgres -U mycms_user -c "create database hoodpub"')
    local('psql hoodpub -U mycms_user  -h postgres < ../db/hoodpub_db_2015-11-13.sql')

def host_restart():
    run('/etc/init.d/hoodpub2-uwsgi stop')
    run('rm /home/hoodpub/work/hoodpub/run/uwsgi*')
    host_start()

def host_start():
    run('/etc/init.d/hoodpub2-uwsgi start')

def tag_newrelic():
    sha1 = local('git rev-parse --short HEAD', capture=True)
    dict_obj = {
        'key': 'a8a9c629f2f123adbb9855a7d82e33918e92b5447712c07',
        'app_name': 'hoodpub',
        'description': '%s' % sha1,
        }

    local('curl -H "x-api-key:{key}" -d "deployment[app_name]={app_name}"\
    -d "deployment[description]={description}"\
    https://api.newrelic.com/deployments.xml'.format(**dict_obj))


def deploy():

    flake8()
    tests()

    put('web/main/settings_local.py',
        'work/hoodpub/web/main/')
    with prefix('source /home/hoodpub/.virt_env/hoodpub2/bin/activate'):
        with cd('/home/hoodpub/work/hoodpub/web'):
            run('git pull origin master')
            run('pip install -r requirements.txt')
            with shell_env(DB_NAME='hoodpub',
                           DB_USER='mycms_user',
                           DB_PASS='mycms_pass',
                           DB_SERVICE='postgres',
                           DB_PORT='5432'):
                run('python manage.py migrate')
                run('python manage.py collectstatic   --noinput')
                run('/etc/init.d/hoodpub2-uwsgi stop')
                run('rm -rf ../run/*')
                run('/etc/init.d/hoodpub2-uwsgi start')
    run('curl http://www.hoodpub.com/ -H \"Host: www.hoodpub.com\"> /dev/null')
    tag_newrelic()
