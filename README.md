# Xenolith

Xenolith is a command-line based tool that allows for files to be encrypted with public keys and accessed by those who have access. With the main component being FiloSottile's [age](https://github.com/FiloSottile/age) and str4d's [rage](https://github.com/str4d/rage) library for encryption, Xenolith uses `ssh-rsa`, `ssh-ed25519`, and age's `keygen` for keys.

# Installation

- Start by installing [age](https://github.com/FiloSottile/age) and [rage](https://github.com/str4d/rage)

# Usage

Xenolith uses 5 commands:

```
- xenolith
Contains a list of all the commands

- xenolith init
Initializes the project in the given directory by creating a .secret folder

- xenolith add [key]
Adds a public key (Recipient) to the list of users that can access an encrypted file.

- xenolith remove [key]
Removes a public key from the list of users. The key must match one of the keys found in .secret/recipients.txt

- xenolith encrypt [file_name]
With a given set of recipients, this encrypts a given file and appends an .age suffix at the end.

- xenolith decrypt [key_file] [file_path]
With a given key file path, this decrypts a file that have been previously encrypted.
```

# Contributing

To get started:

- Download [Python 3.8.4](https://www.python.org/downloads/release/python-384/)
- Set up [Python's Virtual Environment](https://docs.python.org/3/library/venv.html)
  ```
  python3 -m venv venv
  ```
- Download the project's requirements and run venv
  ```
  pip install -r requirements.txt
  source ./venv/bin/activate
  ```
- Install [age](https://github.com/FiloSottile/age) and [rage](https://github.com/str4d/rage)
- To test the application locally, run:
  ```
  pip install --editable .
  ```
- Tests can be run by executing `run_tests.sh` found in the `bin/` folder

# License

This project uses the [MIT](./LICENSE) license.
