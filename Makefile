.PHONY: lint format typecheck test test-unit test-qgis test-edge coverage clean package help

PLUGIN_DIR = agrobr_qgis
TEST_DIR = tests

help:  ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint:  ## Roda ruff check + format check
	ruff check $(PLUGIN_DIR)/ $(TEST_DIR)/
	ruff format --check $(PLUGIN_DIR)/ $(TEST_DIR)/

format:  ## Formata com ruff
	ruff check --fix $(PLUGIN_DIR)/ $(TEST_DIR)/
	ruff format $(PLUGIN_DIR)/ $(TEST_DIR)/

typecheck:  ## Roda mypy
	mypy $(PLUGIN_DIR)/

test: test-unit test-edge  ## Roda testes unit + edge (sem QGIS)

test-unit:  ## Testes unitários
	pytest $(TEST_DIR)/unit/ -v

test-qgis:  ## Testes QGIS (requer Docker ou ambiente QGIS)
	xvfb-run pytest $(TEST_DIR)/qgis/ -v -m qgis

test-edge:  ## Testes de edge cases
	pytest $(TEST_DIR)/edge_cases/ -v

coverage:  ## Coverage report (unit + edge)
	pytest $(TEST_DIR)/unit/ $(TEST_DIR)/edge_cases/ --cov=$(PLUGIN_DIR) --cov-report=term-missing --cov-report=html

clean:  ## Remove cache e build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage build/ dist/

package:  ## Empacota plugin para distribuição
	@echo "Use: qgis-plugin-ci package <version>"
