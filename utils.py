import os
import click
import functools
import json
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME, CONFIG_FILE_NAME


def secret_folder_exists(func):
    @functools.wraps(func)
    def check(*args, **kwargs):
        if not os.path.exists(SECRET_PATH):
            return click.echo(
                'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
        else:
            func(*args, **kwargs)
    return check


def recipients_file_exists(func):
    @functools.wraps(func)
    @secret_folder_exists
    def check(*args, **kwargs):
        if not os.path.isfile(SECRET_PATH + RECIPIENTS_FILE_NAME):
            # TODO: If the file is missing, give option to create
            return click.echo(
                'Recipients file could not be found. Delete the .secret folder and reinitialize xenolith')
        else:
            func(*args, **kwargs)
    return check


def config_file_exists(func):
    @functools.wraps(func)
    @secret_folder_exists
    def check(*args, **kwargs):
        if not os.path.isfile(SECRET_PATH + CONFIG_FILE_NAME):
            # TODO: If the file is missing, give option to create
            return click.echo(
                'Config file could not be found. Delete the .secret folder and reinitialize xenolith')
        else:
            func(*args, **kwargs)
    return check


def encryption_library():
    config = open(SECRET_PATH + CONFIG_FILE_NAME, 'r')
    encryption = json.load(config)['encryption']
    config.close()
    return encryption
