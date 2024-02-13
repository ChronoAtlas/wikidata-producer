.PHONY: install
install: $(VERSION)
	pip install .

.PHONY: install-all
install-all: $(VERSION)
	pip install -e '.[all]'
