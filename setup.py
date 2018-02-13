from setuptools import find_packages, setup

__author__ = 'deresmos'

setup(
    name='customlogger',
    version='0.2.8',
    description='custom logger class.',
    author='deresmos',
    author_email='deresmos@gmail.com',
    packages=find_packages(),
    include_package_data=False,
    keywords=['logging', 'Logger', 'custom'],
    license='MIT License',
    install_requires=['requests', ])
