from setuptools import setup

setup(
    name='zeroecks.com',
    version='0.1',
    description='zeroecks.com',
    author='Adam A.G. Shamblin',
    author_email='adam.shamblin@tutanota.com',
    license='MIT',
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
