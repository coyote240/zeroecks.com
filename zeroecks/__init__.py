import os
import os.path
import pkg_resources


def install_supervisor_config():
    supervisor_conf = pkg_resources.resource_string(__name__,
                                                    'supervisor.conf')
    with cd('/etc/supervisor/conf.d/'):
        os.rename('zeroecks.conf', 'zeroecks.conf.bak')
        with open('zeroecks.conf', 'w') as config:
            config.write(supervisor_conf)


def install_config(origin, target):
    content = pkg_resources.resource_string(__name__, origin)
    path, filename = os.path.split(target)

    with cd(path):
        if os.path.isfile(filename):
            os.rename(filename, filename + '.bak')
        with open(filename, 'w') as config:
            config.write(content)


def install_config_script():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('origin')
    parser.add_argument('target')
    args = parser.parse_args()

    install_config(args.origin, args.target)


class cd(object):

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)
