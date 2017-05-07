from fabric.api import env, task, run, sudo, cd


env.use_ssh_config = True
env.project_name = 'zeroecks'
env.path = '/var/www/{project_name}'.format(**env)
env.virtualenv_path = '/var/env/{project_name}'.format(**env)

'''
install redis, postgres, nginx
install nginx.conf, redis.conf, etc.
activate virtual environment
pull code
install dependencies
restart services
'''


@task
def setup():
    """
    Setup python environment
    """
    sudo('apt-get install -y python3-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('mkdir -p {virtualenv_path}'.format(**env))
    with cd(env.virtualenv_path):
        run('virtualenv -p python3 {virtualenv_path}'.format(**env), pty=True)


@task
def deploy():
    pass


def upload_archive():
    pass


def install_site():
    pass


def install_requirements():
    pass
