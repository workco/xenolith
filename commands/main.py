import click
import os
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME

@click.command()
def init():
    if os.path.exists(SECRET_PATH):
        click.echo('Project has already been initialized')
        return 
    try:
        os.mkdir(SECRET_PATH)
        recipients = open(SECRET_PATH + RECIPIENTS_FILE_NAME, "w")
        recipients.close()
    except OSError as e:
        click.echo('There was an error creating the secret folder.\n{}'.format(e))
        return
    click.echo('.secret folder created in current directory')