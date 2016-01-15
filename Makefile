clean:
	pip freeze > .pip.freeze
	pip uninstall -r .pip.freeze

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} \;

cleandb:
	echo "drop database if exists ripe; create database ripe;" | mysql -uroot
	./src/manage.py syncdb --noinput
	./src/manage.py migrate --noinput
	./src/manage.py loaddata dim_utc_date

install:

	mkdir -p /tmp/pypi
	pip install --download /tmp/pypi --no-deps -r requirements.txt
	pip install --download /tmp/pypi --no-deps -r requirements-dev.txt
	pip install --download /tmp/pypi --no-deps -r requirements-sc.txt -i https://cheeseshop:password@cheeseshop.local/simple
	pip install --no-index --find-links=/tmp/pypi --no-deps -r requirements.txt
	pip install --no-index --find-links=/tmp/pypi --no-deps -r requirements-dev.txt
	pip install --no-index --find-links=/tmp/pypi --no-deps -r requirements-sd.txt

unit:
	src/manage.py test reporting

pep8:
	-git status | grep 'modified:.*py' | cut -f 2 -d: | xargs -n 1 -t pep8 --max-line-length 120

pylint:
	-PYTHONPATH=$$(pwd)/src:$${PYTHONPATH} &&\
	git status | grep 'modified:.*py' | cut -f 2 -d: | xargs -n 1 -t pylint --rcfile pylint.rc -f colorized -r n
