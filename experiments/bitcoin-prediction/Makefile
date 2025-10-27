.PHONY: help install forecast backtest clean

help:
	@echo "Bitcoin Price Prediction - Open Source Toolkit"
	@echo "NO API KEY REQUIRED - 100% Free and Local"
	@echo ""
	@echo "Available Commands:"
	@echo ""
	@echo "  make install      - Install required dependencies"
	@echo "  make forecast     - Generate actionable trading forecast (7 days) 🔥"
	@echo "  make backtest     - Run comprehensive backtest analysis"
	@echo "  make clean        - Clean generated results"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make install"
	@echo "  2. make forecast"
	@echo ""
	@echo "The forecast tool provides clear trading signals with confidence levels"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Installation complete!"

forecast:
	@echo "Generating actionable Bitcoin trading forecast..."
	@echo "Using open-source StatsForecast (AutoARIMA + AutoETS)"
	@echo ""
	python trading_forecast.py

backtest:
	@echo "Running comprehensive backtest analysis..."
	@echo "This will test prediction accuracy on historical data"
	@echo ""
	python main.py

clean:
	@echo "Cleaning results..."
	rm -rf results/
	rm -f trading_forecast.csv
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	@echo "✓ Cleanup complete!"
