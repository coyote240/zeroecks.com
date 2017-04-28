from fabric.api import run, env, task


env.use_ssh_config = True

'''
activate virtual environment
nginx.conf
pull code
install dependencies
restart app
restart nginx
'''


@task
def install_tools():
    pass


@task
def install_nginx_config():
    pass
