.PHONY: test
test: $(VERSION)
	pytest tests
