from setuptools import setup
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()
setup(
    name='crypto2fiat',
    version='19.10.17',
    description='Makes converting from cryptocurrencies to fiat easy.',
    author='Raphael',
    author_email='rtnanje@gmail.com',
    packages=['crypto2fiat'],  # same as name
    install_requires=dependencies,  # external packages as dependencies
)
