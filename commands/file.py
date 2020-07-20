
import click
import os
import constant as constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def file():
    pass


@file.command()
@click.argument('file_name')
def encrypt(file_name):
    if not os.path.exists(SECRET_PATH):
        return click.echo(
            'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith')
    elif os.stat(SECRET_PATH + RECIPIENTS_FILE_NAME).st_size == 0:
        return click.echo(
            'To encrypt a file, at least one user\'s public key must be added using "xenolith key add"')

    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'r') as recipients_list:
        format_recipients = ''
        for recipient in recipients_list:
            format_recipients = format_recipients + '-r ' + recipient.strip() + ' '
        try:
            os.system('age ' + format_recipients + '-o ' +
                      (file_name + '.age') + ' ' + file_name)
            click.echo('File ' + (file_name + '.age') + ' has been encrypted')
        except Exception as e:
            click.echo(
                'There was an error encrypting the specified file.\n{}'.format(e))


@file.command()
@click.argument('key')
@click.argument('file_path')
def decrypt(key, file_path):
    try:
        os.system('age -decrypt -i ' + key + ' ' + file_path +
                  ' > ' + file_path.replace('.age', ''))
        click.echo('File has been decrypted')
    except Exception as e:
        click.echo(
            'There was an error decrypting the specified file.\n{}'.format(e))
