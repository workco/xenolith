# Xenolith [![Run tests](https://github.com/workco/xenolith/workflows/Run%20tests/badge.svg?branch=master)](https://github.com/workco/xenolith/actions)

Xenolith is a command-line based tool that allows for files to be encrypted with public keys and decrypted by users who have access. With the main components being FiloSottile's [age](https://github.com/FiloSottile/age) and str4d's [rage](https://github.com/str4d/rage) library for encryption, Xenolith uses `ssh-rsa`, `ssh-ed25519`, and age/rages's `keygen` as keys.

# Installation

## Requirements

- Install [age](https://github.com/FiloSottile/age) or [rage](https://github.com/str4d/rage)

- Preferably use [Python 3.8.4](https://www.python.org/downloads/release/python-384/) or higher

## Installation

Install using pip

```
pip install xenolith
```

# Usage

Xenolith uses 5 commands:

```
- xenolith
Contains a list of all the commands


- xenolith init [--encryption, -e]
Initializes the project in the given directory by creating a .secret folder. This folder contains a `recipients.txt` and `config.json` file.

Options:
-e, --encryption    Specifies an encryption library (age, rage). Defaults to age


- xenolith encryption [age/rage]
Changes the encryption library to age or rage


- xenolith add [key]
Adds a public key (Recipient) to the list of recipients that can access an encrypted file.


- xenolith remove [key]
Removes a public key from the list of recipients. The key must match one of the keys found in `.secret/recipients.txt`


- xenolith encrypt [file_name]
With a given set of recipients, encrypts the given file and appends an .age suffix at the end.


- xenolith decrypt [key_path] [file_path]
With a given key and file, decrypts a file that have been previously encrypted.
```

# Contributing

To get started:

- Download [Python 3.8.4](https://www.python.org/downloads/release/python-384/)
- Install [age](https://github.com/FiloSottile/age) and [rage](https://github.com/str4d/rage)
- Set up [Python's Virtual Environment](https://docs.python.org/3/library/venv.html)
  ```
  python3 -m venv venv
  ```
- Download the project's requirements and run venv
  ```
  pip install -r requirements.txt
  source ./venv/bin/activate
  ```
- To test the application locally, run:
  ```
  pip install --editable .
  ```
- Tests can be run by executing `run_tests.sh` found in the `bin/` folder

# License

This project uses the [MIT](./LICENSE) license.
