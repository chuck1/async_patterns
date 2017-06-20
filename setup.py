
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='ws_callbacks',
        version=version,
        description='pattern for registering callbacks',
        url='http://github.com/chuck1/web_sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=(
            'ws_callbacks',
            'ws_callbacks.tests'),
        zip_safe=False,
        )

