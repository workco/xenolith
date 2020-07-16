import click
import os
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def user():
    pass


@user.command()
@click.option('--format', default='key', help='The user identification that will be added. Defaults to a public key.', type=click.Choice(['key', 'github'], case_sensitive=False))
@click.argument('key')
def add(format, key):
    if not os.path.exists(SECRET_PATH):
        click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
        return
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'a') as recipients_file:
        recipients_file.write(key + '\n')


@user.command()
@click.argument('id')
def remove(id):
    if not os.path.exists(SECRET_PATH):
        click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
        return
