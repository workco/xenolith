import click
import os
import constant as constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def user():
    pass


@user.command()
@click.option('--type', default='key', help='The user identification that will be added. Defaults to a public key.', type=click.Choice(['key', 'github'], case_sensitive=False))
@click.argument('key')
def add(type, key):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'a') as recipients_file:
        recipients_file.write(key + '\n')
        click.echo('User has been added')


@user.command()
@click.argument('id')
def remove(id):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
