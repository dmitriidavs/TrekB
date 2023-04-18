#!/bin/bash
# shellcheck disable=SC2164,SC2103

# vars
TARGET_FUNC="webhook"
PACKAGE_NAME="webhook"

# create src files
echo 'Creating src files.'
cd ${TARGET_FUNC}
mkdir src
pip install -r requirements.txt --target src
cp app.py src/lambda_function.py
cp -r modules src

# zip src files
echo 'Creating zip.'
cd src
zip -r ${PACKAGE_NAME}.zip .
cd ../../
mv ${TARGET_FUNC}/src/${PACKAGE_NAME}.zip .
rm -rf ${TARGET_FUNC}/src
