.ONESHELL:
SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

include $(SELF_DIR)/_install.mk
include $(SELF_DIR)/_lint.mk
include $(SELF_DIR)/_test.mk

.PHONY: $(VERSION)
$(VERSION):
	git describe --tag --always \
		| grep -oE '[0-9]+\.[0-9]+\.[0-9]+' \
		|| echo "0.0.0" \
		>$@
	printf '__version__ = "%s"\n' "$$(cat $@)" >$@
