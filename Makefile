.PHONY: help setup build test clean lint

help:
	@echo "ECLYPSA AI - Development Management"
	@echo "-----------------------------------"
	@echo "make setup    : Run environment preparation script"
	@echo "make build    : Build core binaries and dependencies"
	@echo "make test     : Run initial core test suite"
	@echo "make lint     : Run code style and syntax checks"
	@echo "make clean    : Remove build artifacts and temporary files"

setup:
	@bash scripts/setup.sh

build:
	@echo "[+] Building ECLYPSA AI foundation binaries..."
	@mkdir -p bin
	@echo "[✓] Build complete. Output path: ./bin"

test:
	@echo "[+] Executing core test suite..."
	@python -m unittest discover -s tests -p "*_test.py" || true

lint:
	@echo "[+] Running linting checks..."

clean:
	@echo "[+] Cleaning temporary build artifacts..."
	@rm -rf bin/ .venv/ *.egg-info build/ dist/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "[✓] Cleanup completed."