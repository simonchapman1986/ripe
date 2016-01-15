#!/bin/bash

set -e

cd "${SD_PACKAGE_DIRECTORY}"
echo "Running after-configure.sh at $(pwd)"

if [ "${SD_RUN_MIGRATIONS}" == "1" ]; then
    sudo -u ${SD_SERVICE_USER} sh -c "${SD_PYTHON} src/manage.py syncdb --noinput"
    sudo -u ${SD_SERVICE_USER} sd -c "${SD_PYTHON} src/manage.py migrate --noinput"
fi

sudo -u ${SD_SERVICE_USER} sh -c "${SD_PYTHON} src/manage.py collectstatic --noinput"
sudo chown -R "${SD_SERVICE_USER}" "${SD_PACKAGE_DIRECTORY}"
