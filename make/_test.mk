.PHONY: test
test: unit-test integration-test

.PHONY: unit-test
unit-test: $(VERSION)
	-pytest tests/unit_tests
	ret=$$?
	test "$$ret" = 5 && ret=0
	exit $$ret

.PHONY: integration-test
integration-test: $(VERSION)
	docker-compose up -d
	-pytest tests/integration_tests
	ret=$$?
	docker-compose down
	test "$$ret" = 5 && ret=0
	exit $$ret
