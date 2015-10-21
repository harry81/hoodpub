from fabric.api import *

env.user = 'hoodpub'
env.hosts = ['www.hoodpub.com']
env.use_ssh_config = True


def host_type():
    run('uname -s')


def deploy():
    put('web/mycms/settings_local.py',
        'work/mycms/web/mycms/')
    with prefix('source /home/hoodpub/.virt_env/berlin/bin/activate'):
        with cd('/home/hoodpub/work/mycms/web'):
            run('git pull')
            run('pip install -r requirements.txt')
            with shell_env(DB_NAME='mycms',
                           DB_USER='mycms_user',
                           DB_PASS='mycms_pass',
                           DB_SERVICE='postgres',
                           DB_PORT='5432'):
                run('python manage.py migrate')
                run('python manage.py collectstatic   --noinput')
                run('sudo /etc/init.d/berlin-uwsgi stop')
                run('rm -rf ../run/uwsgi-49701.pid')
                run('sudo /etc/init.d/berlin-uwsgi start')
    local('curl http://berlin.hoodpub.com/ > /dev/null ')
