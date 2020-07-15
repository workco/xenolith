import click
import os

secret_path = '.secret/'
recipients_path = "recipients.txt"

@click.command()
def init():
    if os.path.exists(secret_path):
        click.echo('Project has already been initialized')
        return 
    try:
        os.mkdir(secret_path)
        recipients = open(secret_path + recipients_path, "w")
        recipients.close()
    except OSError as e:
        click.echo('There was an error creating the secret folder.\n{}'.format(e))
        return

    click.echo('.secret folder created in current directory')

@click.group()
def user():
    pass

@click.group
def file():
    pass

@add.command()
@click.argument('key')
def user(key):
    if not os.path.exists(secret_path):
        click.echo('Cannot detect a .secret folder. Run \"xenolith init\" to initialize xenolith')
        return 
    
    with open(secret_path + recipients_path, 'a') as recipients_list:
        for recipient in recipients_list:
            users_file.write('-r ' + key + '\n')

@add.command()  
@click.command()
def add():
    if not os.path.exists(secret_path):
        click.echo('Cannot detect a .secret folder. Run \"xenolith init\" to initialize xenolith')
        return
    elif os.stat(secret_path + recipients_path).st_size == 0:
        click.echo("To encrypt a file, at least one user's public key must be added using \"xenolith key add\"")
        return

    with open(secret_path + recipients_path, 'r') as recipients_list:
        format_recipients = ''
        for recipient in recipients_list:
            format_recipients = format_recipients + "-r " + recipient.strip() + " "
        os.system("age " + format_recipients + " -o .env.secret .env")
    