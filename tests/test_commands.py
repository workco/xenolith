import shutil
import os
import pytest
import json
import functools
from constant import SECRET_PATH, RECIPIENTS_FILE_NAME, CONFIG_FILE_NAME
from commands.file import encrypt, decrypt
from commands.main import init, encryption
from commands.user import add, remove
from click.testing import CliRunner

TEST_PUBLIC_KEY = 'age1vksv3t6antalfj3ekyr75fyuff2g2m38slpeq65v5ru82hfg2v3sngv7t6'
TEST_PRIVATE_KEY = 'AGE-SECRET-KEY-1964835NDR0GQRDY9LLDM422NWAZR9G05NFNXW6W49TURQ8PQPDGSYGJEL9'


@pytest.fixture(scope="function", autouse=True)
def safe_delete(request):
    # Setup
    if os.path.exists(SECRET_PATH):
        shutil.rmtree(SECRET_PATH)
    yield
    # Teardown
    if os.path.exists(SECRET_PATH):
        shutil.rmtree(SECRET_PATH)


@pytest.fixture
def fixture_init_secret():
    run_init = CliRunner().invoke(init, ['-e', 'age'])
    #run_init = CliRunner().invoke(init, ['-e', 'rage'])
    assert ".secret folder created in current directory" in run_init.output
    return run_init


@pytest.fixture
def fixture_add_user(fixture_init_secret):
    add_user = CliRunner().invoke(add, [TEST_PUBLIC_KEY])
    assert "Recipient has been added" in add_user.output
    return add_user


def test_init(fixture_init_secret):
    run_init_exists = CliRunner().invoke(init)
    assert 'Xenolith has already been initialized' in run_init_exists.output


def test_encrypt_no_init():
    run_encrypt = CliRunner().invoke(encrypt, ['.env'])
    assert 'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith' in run_encrypt.output


def test_encrypt_no_recipients_file(fixture_init_secret):
    os.remove(SECRET_PATH + RECIPIENTS_FILE_NAME)
    encrypt_file = CliRunner().invoke(encrypt, ['.env'])

    assert 'Recipients file could not be found' in encrypt_file.output


def test_encrypt_no_recipients_added(fixture_init_secret):
    encrypt_file = CliRunner().invoke(encrypt, ['.env'])
    assert 'To encrypt a file, at least one user\'s public key must be added using "xenolith key add"' in encrypt_file.output


def test_encrypt_decrypt(fixture_add_user, tmp_path):
    env = tmp_path / '.env'
    secret_file = tmp_path / 'key.txt'
    secret_file.write_text(TEST_PRIVATE_KEY)
    env.write_text('test')

    encrypt_file = CliRunner().invoke(encrypt, [str(env)])
    assert 'File ' + str(env) + \
        '.age has been encrypted' in encrypt_file.output

    # Delete to ensure the new .env is the decrypted version
    os.remove(env)

    decrypt_file = CliRunner().invoke(
        decrypt, [str(secret_file), (str(env) + '.age')])
    file_content = open(env, 'r').read()
    assert file_content == 'test'
    assert 'File has been decrypted' in decrypt_file.output


def test_add_user(fixture_init_secret, tmp_path):
    CliRunner().invoke(add, [TEST_PUBLIC_KEY])

    with open(SECRET_PATH + RECIPIENTS_FILE_NAME) as recipient_file:
        # Last line is always an empty string
        recipient_list = recipient_file.read().split('\n')[:-1]
        assert len(recipient_list) == 1
        assert TEST_PUBLIC_KEY == recipient_list[0]


def test_remove_user(fixture_add_user, tmp_path):
    remove_user = CliRunner().invoke(remove, [TEST_PUBLIC_KEY])

    with open(SECRET_PATH + RECIPIENTS_FILE_NAME) as recipient_file:
        # Last line is always an empty string
        recipient_list = recipient_file.read().split('\n')
        assert recipient_list[0] == ''
        assert len(recipient_list) == 1

    assert "Recipient has been removed" in remove_user.output


def test_remove_nonexistant_user(fixture_add_user, tmp_path):
    remove_user = CliRunner().invoke(remove, ["AKey"])

    assert "Recipient could not be found in list of users" in remove_user.output


def test_decrypt_path_not_found():
    decrypt_file = CliRunner().invoke(
        decrypt, ["fakefile.txt", "fakefile.age"])
    assert 'Path \'fakefile.txt\' does not exist' in decrypt_file.output


def test_encryption_change(fixture_init_secret, tmp_path):
    encryption_change = CliRunner().invoke(encryption, ['rage'])
    assert "Updated encryption library to rage" in encryption_change.output

    with open(SECRET_PATH + CONFIG_FILE_NAME) as config_file:
        data = json.load(config_file)
        assert data['encryption'] == 'rage'
