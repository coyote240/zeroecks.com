from fabric.api import env, task, run, sudo, cd, local, put
from fabric.colors import green
import pkg_resources


env.use_ssh_config = True
env.project_name = 'zeroecks.com'
env.virtualenv_path = '/var/env/{project_name}'.format(**env)
env.distribution_path = '/var/dist/{project_name}'.format(**env)
env.config_path = '/etc/{project_name}'.format(**env)
env.resource_path = '/var/www/{project_name}'.format(**env)
env.package_version = pkg_resources.get_distribution(env.project_name).version
env.flyway_download = 'https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/4.2.0/flyway-commandline-4.2.0-linux-x64.tar.gz' # noqa

'''
create database user
- system user with password

install config files
- /var/zeroecks/templates
- /var/zeroecks/assets

install site config
- path to templates
- path to assets
- database user/pass

supervisord
- path to config
- path to startup script

install certbot
register cert
install cert

data migrations
- install conf to <flyway>/conf
- run
'''


@task
def version():
    print(env.package_version)


@task
def setup():
    '''Prepare the host for deployment.
    Update and upgrade Debian packages.
    Create necessary directories.
    '''
    notice('Preparing host for deployment')

    sudo('''echo '\ndeb http://ftp.debian.org/debian jessie-backports main' \
            >> /etc/apt/sources.list''')

    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    sudo('mkdir -p {virtualenv_path}'.format(**env))
    sudo('mkdir -p {distribution_path}'.format(**env))
    sudo('mkdir -p {config_path}'.format(**env))
    sudo('mkdir -p {resource_path}'.format(**env))


@task
def install_dependencies():
    notice('Installing python dependencies')

    sudo('apt-get install -y python3-pip')
    sudo('pip3 install virtualenv')

    with cd(env.virtualenv_path):
        sudo('virtualenv -p python3 .', pty=True)


@task
def install_servers():
    notice('Installing dependent services')

    sudo('apt-get install -y -t jessie-backports '
         'nginx postgresql redis-server supervisor')


@task
def install_flyway():
    notice('Installing Flyway')

    run('wget {flyway_download}'.format(**env))
    run('tar xzf flyway-commandline-4.2.0-linux-x64.tar.gz')


@task
def package_distro():
    notice('Packaging project and copying to host.')

    local_path = 'dist/{project_name}-{package_version}*'.format(**env)

    local('python setup.py sdist bdist_wheel')
    put(local_path, '{distribution_path}'.format(**env), use_sudo=True)

    sudo('{virtualenv_path}/bin/pip install '
         '{distribution_path}/{project_name}-{package_version}.tar.gz'.format(**env)) # noqa


@task
def install_site():

    with cd('/etc/nginx/'):
        sudo('rm sites-enabled/default')
        sudo('ln -s sites-available/{project_name} '
             'sites-enabled/{project_name}'.format(**env))


@task
def install_configs():
    pass


@task
def restart_servers():
    sudo('supervisorctl update')


@task
def data_migration():
    pass


@task
def deploy():
    setup()
    install_dependencies()
    install_servers()
    package_distro()
    install_site()


def notice(msg):
    print(green(msg))
