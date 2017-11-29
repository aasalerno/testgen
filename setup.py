from setuptools import setup

setup(
    name='TestTeX',
    version='0.1dev',
    packages=['testtex'],
    license='MIT',
    author='Anthony Salerno',
    author_email='salerno.anthony92@gmail.com',
    install_requires=[
        'dash',
        'dash-renderer',
        'dash-html-components',
        'plotly',
        'periodictable',
        'sympy'
        ],
)