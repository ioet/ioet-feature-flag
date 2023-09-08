#!/bin/bash
set -eo pipefail

function test_import() {
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    cd ../
    poetry new test-project && cd test-project
    poetry add git+https://git@github.com/ioet/ioet-feature-flag.git@$CURRENT_BRANCH
    poetry add pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    poetry run pytest
    cd ../ioet-feature-flag

}

test_import
