
import click
import os
import utils
import constant as constant
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME


@click.group()
def file():
    pass


@file.command()
@click.argument('file_name')
@utils.recipients_file_exists
@utils.secret_folder_exists
def encrypt(file_name):
    """Encrypts a file assuming that at least one user exists."""
    if os.stat(SECRET_PATH + RECIPIENTS_FILE_NAME).st_size == 0:
        return click.echo(
            'To encrypt a file, at least one user\'s public key must be added using "xenolith key add"')
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'r') as recipients_list:
        format_recipients = ''
        for recipient in recipients_list:
            format_recipients = format_recipients + '-r ' + recipient.strip() + ' '
        try:
            if utils.encryption_library() == 'age':
                os.system('age ' + format_recipients + '-o ' +
                          (file_name + '.age') + ' ' + file_name)
            elif utils.encryption_library() == 'rage':
                os.system('rage ' + format_recipients + '-o ' +
                          (file_name + '.age') + ' ' + file_name)
            else:
                raise ValueError('Invalid encryption type specified in config')
            click.echo('File ' + (file_name + '.age') + ' has been encrypted')
        except Exception as e:
            click.echo(
                'There was an error encrypting the specified file.\n{}'.format(e))


@file.command()
@click.argument('key_file', type=click.Path(exists=True))
@click.argument('file_name', type=click.Path(exists=True))
@utils.secret_folder_exists
def decrypt(key_file, file_name):
    """Decrypts a file with a given key file and file name.

    key_file: Path to a file that contains an age secret key or an SSH key file
    file_name: Path to the encrypted .age file"""
    replace_age_extension = file_name.replace('.age', '')
    try:
        if utils.encryption_library() == 'age':
            os.system('age -decrypt -i ' + key_file + ' ' +
                      file_name + ' > ' + replace_age_extension)
        elif utils.encryption_library() == 'rage':
            os.system('rage --decrypt -i ' + key_file + ' ' +
                      file_name + ' > ' + replace_age_extension)
        else:
            raise ValueError('Invalid encryption type specified in config')
        click.echo('File has been decrypted')
    except Exception as e:
        click.echo(
            'There was an error decrypting the specified file\n{}'.format(e))
