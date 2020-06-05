#! /bin/bash

repo=$([ "$1" == "pypi" ] && echo "pypi"|| echo "testpypi")

echo "$repo"

pipenv run python setup.py sdist bdist_wheel

# note, you'll need to have an API key set up with pypi to use the __token__ username
# this command can be promptless when twince is set up with keyring
pipenv run twine upload --username __token__ --repository "$repo" dist/*