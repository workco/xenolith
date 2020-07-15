import click
import os

secret_path = '.secret/'
recipients_path = "recipients.txt"

@click.group()
def user():
    pass

@click.option('--format', default='key', help='The user identification that will be added. Defaults to a public key.', type=click.Choice(['key', 'github'], case_sensitive=False) )
@click.argument('key')
@user.command()
def add(format, key):
    if not os.path.exists(secret_path):
        click.echo('Cannot detect a .secret folder. Run \"xenolith init\" to initialize xenolith')
        return 
    with open(secret_path + recipients_path, 'a') as recipients_list:
        for recipient in recipients_list:
            users_file.write(key + '\n')

@click.argument('id')
@user.command()
def remove(id):
    if not os.path.exists(secret_path):
        click.echo('Cannot detect a .secret folder. Run \"xenolith init\" to initialize xenolith')
        return 
