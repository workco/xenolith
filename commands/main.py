import click
import os
import json
import utils
from commands import user, file
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME, CONFIG_FILE_NAME


@click.group()
def cli():
    pass


@cli.command()
@click.option('-e', '--encryption', type=click.Choice(['age', 'rage']), default='age')
def init(encryption):
    """Initializes xenolith in the current directory.

    (Optional) encryption - Specify the encryption library to use (age or rage). Defaults to age"""
    if os.path.exists(SECRET_PATH):
        return click.echo('Xenolith has already been initialized')
    try:
        os.mkdir(SECRET_PATH)
        recipients = open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'w')
        config = open(SECRET_PATH + CONFIG_FILE_NAME, 'w')
        json.dump({"encryption": encryption}, config)
        recipients.close()
        config.close()
    except OSError as e:
        return click.echo('There was an error creating the secret folder.\n{}'.format(e))

    click.echo('.secret folder created in current directory')


@cli.command()
@utils.config_file_exists
@click.argument('encryption', type=click.Choice(['age', 'rage']))
def encryption(encryption):
    """Changes the encryption library.

    encryption - Specify the encryption library to use (age or rage). Defaults to age"""
    try:
        with open(SECRET_PATH + CONFIG_FILE_NAME, 'w') as config:
            json.dump({"encryption": encryption}, config)
    except OSError as e:
        return click.echo('There was an error creating the secret folder.\n{}'.format(e))

    click.echo('Updated encryption library to ' + encryption)


command_collection = click.CommandCollection(
    sources=[cli, user.user, file.file])
