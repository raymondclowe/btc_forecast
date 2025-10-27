.PHONY: help install test quick full weather notebook clean

help:
	@echo "Bitcoin Price Prediction Analysis - Available Commands"
	@echo ""
	@echo "  make install    - Install required dependencies"
	@echo "  make test       - Test modules without API key"
	@echo "  make weather    - Bitcoin weather forecast (requires API key) ☀️"
	@echo "  make quick      - Run quick analysis (requires API key)"
	@echo "  make full       - Run comprehensive analysis (requires API key)"
	@echo "  make notebook   - Start Jupyter notebook"
	@echo "  make clean      - Clean generated results"
	@echo ""
	@echo "Before running analysis, set your API key:"
	@echo "  export NIXTLA_API_KEY='your-key-here'"
	@echo ""
	@echo "Get your free API key at: https://dashboard.nixtla.io"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Done!"

test:
	@echo "Running module tests..."
	python test_modules.py

weather:
	@echo "Generating Bitcoin weather forecast..."
	@echo "This will create easy-to-understand forecast charts"
	python weather_forecast.py

quick:
	@echo "Running quick analysis..."
	@echo "This will make a few API calls to TimeGPT"
	python quick_analysis.py

full:
	@echo "Running comprehensive analysis..."
	@echo "This will make multiple API calls to TimeGPT"
	python main.py

notebook:
	@echo "Starting Jupyter notebook..."
	jupyter notebook bitcoin_analysis.ipynb

clean:
	@echo "Cleaning results..."
	rm -rf results/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	@echo "Done!"
