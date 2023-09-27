#!/bin/bash
set -eo pipefail

function test_import_poetry() {
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    cd ../
    poetry new test-project-poetry && cd test-project-poetry
    poetry add git+https://git@github.com/ioet/ioet-feature-flag.git@$CURRENT_BRANCH
    poetry add pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    poetry run pytest
    cd ../ioet-feature-flag

}

function test_import_pip() {
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    cd ../
    mkdir test-project-pip && cd test-project-pip
    python -m venv env && source env/bin/activate
    pip install git+https://github.com/ioet/ioet-feature-flag.git@$CURRENT_BRANCH
    pip install -U pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    pytest
    cd ../ioet-feature-flag
}

test_import_poetry
test_import_pip
