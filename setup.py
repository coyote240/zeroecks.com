from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zeroecks.com',
    version='0.1.9',
    description='zeroecks.com',
    long_description=long_description,
    author='Adam A.G. Shamblin',
    author_email='adam.shamblin@tutanota.com',
    license='MIT',
    url='https://zeroecks.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    data_files=[
        ('/zeroecks/conf/', [
            'conf/config.py',
            'conf/supervisor.conf',
            'conf/redis.conf',
            'conf/nginx.conf',
            'conf/nginx.site.conf',
            'conf/flyway.conf'
        ]),
        ('/zeroecks/sql/', [
            'sql/V1__articles.sql',
            'sql/V1_1__publish_articles.sql',
            'sql/V1_2__users_security.sql',
            'sql/V1_3__article_noncontiguous_ids.sql',
            'sql/V1_4__u2f_devices.sql'
        ])
    ],
    entry_points={
        'console_scripts': [
            'zeroecks = zeroecks.application:main',
            'zeroecks-create-user = zeroecks.models.user:create_user',
            'zeroecks-install-config = zeroecks:install_config_script'
        ]
    },
    install_requires=[
        'six==1.10.0',
        'tornado>=4',
        'tornadobase==0.1.6',
        'psycopg2==2.7.1',
        'redis==2.10.5',
        'hiredis==0.2.0',
        'Markdown==2.6.8',
        'bleach==2.0.0',
        'gnupg==2.2.0'
    ],
    tests_require=['nose'])
