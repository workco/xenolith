
import click
import os
import subprocess
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
    with open(SECRET_PATH + RECIPIENTS_FILE_NAME, 'r') as recipient_file:
        recipients_list = recipient_file.read().splitlines()
        format_recipients = ''
        format_file_name_encrypted = file_name + '.age'
        for recipient in recipients_list:
            format_recipients = format_recipients + '-r ' + recipient + ' '
        # Remove last space from the format
        format_recipients = format_recipients[:-1]
        try:
            if utils.encryption_library().lower() == 'invalid':
                raise ValueError('Invalid encryption type specified in config')
            format_command = '{} {} -o {} {}'.format(
                utils.encryption_library(), format_recipients, format_file_name_encrypted, file_name)
            pipe = subprocess.Popen(format_command, shell=True)
            pipe.wait(timeout=5)
            if int(pipe.returncode) != 0:
                output, error = pipe.communicate()
                raise Exception(
                    'Decryption failed - {}'.format(error.decode('utf-8')))
            click.echo('File ' + format_file_name_encrypted +
                       ' has been encrypted')
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
        if utils.encryption_library().lower() == 'invalid':
            raise ValueError('Invalid encryption type specified in config')
        format_command = '{} -d -i {} {} > {}'.format(
            utils.encryption_library(), key_file, file_name, replace_age_extension)
        pipe = subprocess.Popen(
            format_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pipe.wait(timeout=5)
        if int(pipe.returncode) != 0:
            output, error = pipe.communicate()
            raise Exception(
                'Decryption failed - {}'.format(error.decode('utf-8')))
        click.echo('File has been decrypted')
    except Exception as e:
        click.echo(
            'There was an error decrypting the specified file\n{}'.format(e))
