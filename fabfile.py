from fabric.api import env, task, run, sudo, cd, local, put
import pkg_resources


env.use_ssh_config = True
env.project_name = 'zeroecks.com'
env.path = '/var/www/{project_name}'.format(**env)
env.virtualenv_path = '/var/env/{project_name}'.format(**env)
env.distribution_path = '/var/dist/{project_name}'.format(**env)
env.package_version = pkg_resources.get_distribution(env.project_name).version
env.flyway_download = 'https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/4.2.0/flyway-commandline-4.2.0-linux-x64.tar.gz' # noqa

'''
install supervisord
restart services
install certbot
register cert
install cert
data migrations
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
    sudo('''echo '\ndeb http://ftp.debian.org/debian jessie-backports main' \
            >> /etc/apt/sources.list''')

    sudo('apt-get update')
    sudo('apt-get upgrade -y')
    sudo('mkdir -p {virtualenv_path}'.format(**env))
    sudo('mkdir -p {distribution_path}'.format(**env))


@task
def install_dependencies():
    sudo('apt-get install -y python3-pip')
    sudo('pip3 install virtualenv')

    with cd(env.virtualenv_path):
        sudo('virtualenv -p python3 .', pty=True)


@task
def install_servers():
    sudo('apt-get install -y -t jessie-backports '
         'nginx postgresql redis-server')


@task
def install_flyway():
    run('wget {flyway_download}'.format(**env))
    run('tar xzf flyway-commandline-4.2.0-linux-x64.tar.gz')


@task
def package_distro():
    '''Build and package site, push to host.
    '''
    local_path = 'dist/{project_name}-{package_version}*'.format(**env)

    local('python setup.py sdist bdist_wheel')
    put(local_path, '{distribution_path}'.format(**env), use_sudo=True)


@task
def install_site():
    sudo('{virtualenv_path}/bin/pip install '
         '{distribution_path}/{project_name}-{package_version}.tar.gz'.format(**env)) # noqa

    ''' install configs '''

    with cd('/etc/nginx/'):
        sudo('rm sites-enabled/default')
        sudo('ln -s sites-available/{project_name} '
             'sites-enabled/{project_name}'.format(**env))


@task
def deploy():
    setup()
    install_dependencies()
    install_servers()
    package_distro()
    install_site()
