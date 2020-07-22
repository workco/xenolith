import os
import click
import functools
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


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
            return click.echo(
                'Recipients file could not be found.')
        else:
            func(*args, **kwargs)
    return check
