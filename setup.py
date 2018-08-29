from setuptools import setup

setup(
    name='asabridge',
    packages=['asabridge'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-caching',
        'flask-socketio',
        'simplepam',
        'humanize',
        'python-dateutil',
        'redis'
    ],
)
