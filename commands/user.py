import click
import os
import utils
import constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def user():
    pass


@user.command()
@utils.secret_folder_exists
@click.argument('recipient')
def add(recipient):
    """Adds a recipient that can unencrypt files.

    recpient - Public key of the recipient"""
    # TODO: Allow multiple recipients
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'a') as recipients_file:
        recipients_file.write(recipient)
        recipients_file.write('\n')
        click.echo('Recipient has been added')


@user.command()
@click.argument('recipient')
@utils.recipients_file_exists
def remove(recipient):
    """Removes a recipient that can unencrypt files.

    recpient - Public key of the recipient"""
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'r+') as recipients_file:
        recipients_list = recipients_file.read().splitlines()
        if(recipient in recipients_list):
            recipients_list.remove(recipient)
            click.echo("Recipient has been removed")
        else:
            click.echo("Recipient could not be found in list of users")
        recipients_file.seek(0)
        recipients_file.truncate()
        recipients_file.write('\n'.join(recipients_list))
