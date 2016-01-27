.PHONY: test clean reclean tagv pypi release docs

default:
	@echo "Pick a target (e.g., clean, test)"

clean:
	find wsgi_intercept test -name "*.py[co]" |xargs rm || true
	find wsgi_intercept test -type d -name "__pycache__" |xargs rmdir || true
	rm -r dist || true
	rm -r build || true
	rm -r wsgi_intercept.egg-info || true
	rm *.bundle || true
	rm -r *-bundle* || true
	cd docs && make clean

reclean:
	find wsgi_intercept test -name "*.py[co]" |xargs rm || true
	find wsgi_intercept test -type d -name "__pycache__" |xargs rmdir || true
	rm -r dist || true
	rm -r build || true
	rm -r wsgi_intercept.egg-info || true
	rm *.bundle || true
	rm -r *-bundle* || true
	cd docs && make clean

test:
	py.test --tb=short -x test

doctest:
	cd docs && make doctest

tagv:
	git tag -a \
		-m v`python setup.py --version` \
		v`python setup.py --version`
	git push origin master --tags

pypi:
	python setup.py sdist upload

docs:
	cd docs && $(MAKE) html

release: clean test tagv reclean pypi
