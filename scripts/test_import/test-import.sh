function test_import() {
    cd ../
    poetry new test-project && cd test-project
    poetry add ../ioet-feature-flag
    poetry add pytest
    export ENVIRONMENT="test"
    cp -r ../ioet-feature-flag/scripts/test_import/* ./
    poetry run pytest
    cd ../ioet-feature-flag

}

test_import
