.PHONY: test clean tagv pypi release

default:
	@echo "Pick a target (e.g., clean, test)"

clean:
	find wsgi_intercept -name "*.pyc" |xargs rm || true
	rm -r dist || true
	rm -r build || true
	rm -r wsgi_intercept.egg-info || true
	rm *.bundle || true
	rm -r *-bundle* || true

test:
	py.test --tb=short -x test

tagv:
	git tag -a \
		-m v`python setup.py --version` \
		v`python setup.py --version`
	git push origin master --tags

pypi:
	python setup.py sdist upload

release: clean test tagv pypi

