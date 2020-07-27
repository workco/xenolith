from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='xenolith',
    version='0.1.2',
    author='Sashary Morel',
    description='Xenolith is a command-line based tool that allows for files to be encrypted with public keys and decrypted by users who have permission',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/workco/xenolith",
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        xenolith=commands.main:command_collection
    '''
)
