
import click
import os
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME

@click.group()
def file():
    pass

@file.command()  
def add():
    if not os.path.exists(SECRET_PATH):
        click.echo('Cannot detect a .secret folder. Run \"xenolith init\" to initialize xenolith')
        return
    elif os.stat(SECRET_PATH + RECIPIENTS_FILE_NAME).st_size == 0:
        click.echo("To encrypt a file, at least one user's public key must be added using \"xenolith key add\"")
        return
        
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'r') as recipients_list:
        format_recipients = ''
        for recipient in recipients_list:
            format_recipients = format_recipients + "-r " + recipient.strip() + " "
        os.system("age " + format_recipients + " -o .env.secret .env")
    