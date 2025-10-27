.PHONY: help install test quick full weather notebook clean opensource

help:
	@echo "Bitcoin Price Prediction Analysis - Available Commands"
	@echo ""
	@echo "  make install      - Install required dependencies"
	@echo "  make test         - Test modules without API key"
	@echo "  make opensource   - Run REAL analysis with open-source models (NO API KEY!) 🔥"
	@echo "  make weather      - Bitcoin weather forecast (requires API key) ☀️"
	@echo "  make quick        - Run quick analysis (requires API key)"
	@echo "  make full         - Run comprehensive analysis (requires API key)"
	@echo "  make notebook     - Start Jupyter notebook"
	@echo "  make clean        - Clean generated results"
	@echo ""
	@echo "⭐ NEW: Run 'make opensource' for REAL Bitcoin predictions without API key!"
	@echo ""
	@echo "For API-based tools, set your API key:"
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

opensource:
	@echo "Running REAL Bitcoin analysis with open-source StatsForecast..."
	@echo "NO API KEY REQUIRED - Uses AutoARIMA + AutoETS ensemble"
	@echo ""
	python main_opensources.py

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
