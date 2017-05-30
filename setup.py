from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zeroecks.com',
    version='0.1',
    description='zeroecks.com',
    long_description=long_description,
    author='Adam A.G. Shamblin',
    author_email='adam.shamblin@tutanota.com',
    license='MIT',
    url='https://zeroecks.com',
    packages=find_packages(exclude=['tests']),
    data_files=[
        ('/etc/nginx', ['conf/nginx.conf']),
        ('/etc/nginx/sites-available', ['conf/nginx.site.conf']),
        ('/etc/redis', ['conf/redis.conf'])
    ],
    entry_points={
        'console_scripts': [
            'startserver = zeroecks.application:main'
        ]
    },
    install_requires=[
        'tornado>=4',
        'tornadobase==0.1.2',
        'psycopg2==2.7.1',
        'redis==2.10.5',
        'hiredis==0.2.0',
        'Markdown==2.6.8',
        'bleach==2.0.0'
    ],
    tests_require=['nose'])
