import shutil
import os
import pytest
import functools
from commands.file import encrypt, decrypt
from commands.main import init
from commands.user import add, remove
from click.testing import CliRunner

TEST_PUBLIC_KEY = 'age1vksv3t6antalfj3ekyr75fyuff2g2m38slpeq65v5ru82hfg2v3sngv7t6'
TEST_PRIVATE_KEY = 'AGE-SECRET-KEY-1964835NDR0GQRDY9LLDM422NWAZR9G05NFNXW6W49TURQ8PQPDGSYGJEL9'
SECRET_PATH = './.secret'


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
def init_file():
    run_init = CliRunner().invoke(init)
    return run_init


@pytest.fixture
def init_add_user(init_file):
    add_user = CliRunner().invoke(add, [TEST_PUBLIC_KEY])
    return add_user


def test_init(init_file):
    run_init_exists = CliRunner().invoke(init)
    assert 'Xenolith has already been initialized' in run_init_exists.output


def test_encrypt_no_init():
    run_encrypt = CliRunner().invoke(encrypt, ['.env'])
    assert 'Cannot detect a .secret folder. Run "xenolith init" to initialize xenolith' in run_encrypt.output


def test_encrypt_no_user(init_file):
    encrypt_file = CliRunner().invoke(encrypt, [''])
    assert 'To encrypt a file, at least one user\'s public key must be added using "xenolith key add"' in encrypt_file.output


def test_encrypt_decrypt(init_add_user, tmp_path):
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
    file_content = open(str(env), 'r').read()
    assert file_content == 'test'
    assert 'File has been decrypted' in decrypt_file.output


def test_decrypt_path_not_found():
    decrypt_file = CliRunner().invoke(
        decrypt, ["fakefile.txt", "fakefile.age"])
    assert 'Path \'fakefile.txt\' does not exist' in decrypt_file.output
