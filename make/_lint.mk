.PHONY: lint
lint: $(VERSION)
	black --check -q src tests
	flake8 src tests
	mypy src tests

.PHONY: fix
fix:
	black src tests
	isort src tests
