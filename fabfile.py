from fabric.api import *
import time

env.user = 'hoodpub'
env.hosts = ['www.hoodpub.com']
env.use_ssh_config = True


def host_type():
    run('uname -s')


def db_backup():
    name = 'hoodpub_db_%s.sql' % time.strftime("%Y-%m-%d")
    run('pg_dump hoodpub  -h localhost -U mycms_user  > /tmp/%s' % name)
    get('/tmp/%s' % name, 'db/%s' % name)


def deploy():

    local('cd web; flake8 hoodpub book')
    local('cd web; REUSE_DB=1 python manage.py test -v3 book hoodpub')

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
