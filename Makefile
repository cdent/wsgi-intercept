.PHONY: test clean

clean:
	find wsgi_intercept -name "*.pyc" |xargs rm || true
	rm -r dist || true
	rm -r build || true
	rm -r wsgi_intercept.egg-info || true
	rm *.bundle || true
	rm -r *-bundle* || true

test:
	py.test -x test
