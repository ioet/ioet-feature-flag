#!/bin/bash
set -eo pipefail

function test_import_poetry() {
    cd ../
    poetry new test-project-poetry && cd test-project-poetry
    poetry add git+https://git@github.com/ioet/ioet-feature-flag.git@$1
    poetry add pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    poetry run pytest
    cd ../ioet-feature-flag

}

function test_import_pip() {
    cd ../
    mkdir test-project-pip && cd test-project-pip
    python -m venv env && source env/bin/activate
    pip install git+https://github.com/ioet/ioet-feature-flag.git@$1
    pip install -U pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    pytest
    cd ../ioet-feature-flag
}


test_import_poetry $BRANCH_NAME
test_import_pip $BRANCH_NAME
