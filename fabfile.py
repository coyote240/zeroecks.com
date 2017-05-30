from fabric.api import env, task, run, sudo, cd, local, put


env.use_ssh_config = True
env.project_name = 'zeroecks'
env.path = '/var/www/{project_name}'.format(**env)
env.virtualenv_path = '/var/env/{project_name}'.format(**env)
env.distribution_path = '~/dist/{project_name}'.format(**env)

'''
install redis, postgres, nginx
install supervisord
install nginx.conf, redis.conf, etc.
activate virtual environment
push code
install dependencies
restart services
install certbot
register cert
install cert
'''


@task
def setup():
    '''Prepare the host for deployment.
    Update and upgrade Debian packages.
    Create necessary directories.
    '''
    sudo('''echo '\ndeb http://ftp.debian.org/debian jessie-backports main' \
            >> /etc/apt/sources.list''')

    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    sudo('mkdir -p {virtualenv_path}'.format(**env))
    run('mkdir -p {distribution_path}'.format(**env))


@task
def install_dependencies():
    sudo('apt-get install -y python3-pip python3-virtualenv')

    with cd(env.virtualenv_path):
        sudo('virtualenv -p python3 .', pty=True)
        sudo('source bin/activate')


@task
def install_servers():
    sudo('apt-get install -y -t jessie-backports \
            nginx postgresql redis-server')

    with cd('/etc/nginx/'):
        sudo('rm sites-enabled/default')
        sudo('ln -s sites-available/{project_name} \
                sites-enabled/{project_name}'.format(**env))


@task
def package_distro():
    '''Build and package site, push to host.
    '''
    local('python setup.py sdist bdist_wheel')
    put('dist/*', '{distribution_path}'.format(**env))


@task
def deploy():
    setup()
    package_distro()
