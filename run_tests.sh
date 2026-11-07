#!/bin/bash

pytest --alluredir=allure-results
TEST_EXIT_CODE=$?

allure generate allure-results -o allure-report --clean
allure open allure-report

exit $TEST_EXIT_CODE
