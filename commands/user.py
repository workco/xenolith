import click
import os
import constant as constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def user():
    pass


@user.command()
@click.argument('recipient')
def add(recipient):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'a') as recipients_file:
        recipients_file.write(recipient + '\n')
        click.echo('Recipient has been added')


@user.command()
@click.argument('id')
def remove(id):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
