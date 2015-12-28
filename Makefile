.PHONY: test clean tagv pypi release docs

default:
	@echo "Pick a target (e.g., clean, test)"

clean:
	find wsgi_intercept -name "*.pyc" |xargs rm || true
	find test -name "*.pyc" |xargs rm || true
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

release: clean test tagv clean pypi

