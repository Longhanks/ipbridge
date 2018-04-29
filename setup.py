from setuptools import setup

setup(
    name='asabridge',
    packages=['asabridge'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_httpauth',
        'flask-caching',
        'simplepam',
        'humanize',
        'python-dateutil',
        'redis'
    ],
)

