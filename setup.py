from setuptools import setup, find_packages

setup(
    name='Xenolith',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        xenolith=xenolith:init
    ''',
)