# Contributing to Bitcoin Prediction Analysis

Thank you for your interest in improving this Bitcoin prediction analysis toolkit!

## Ways to Contribute

### 1. Report Issues
- Found a bug? Open an issue describing the problem
- Have a suggestion? Share your ideas for improvements
- Encountered an error? Include the full traceback

### 2. Improve Documentation
- Fix typos or unclear explanations
- Add more examples or use cases
- Translate documentation

### 3. Add Features

#### Potential Enhancements

**Data Sources**
- Support for additional cryptocurrency exchanges
- Integration with on-chain metrics (transaction volume, active addresses)
- Market sentiment data (social media, news)

**Analysis Methods**
- Fine-tuning TimeGPT on Bitcoin-specific data
- Ensemble methods combining multiple models
- Regime detection for adaptive strategies

**Visualization**
- Interactive plots with Plotly
- Real-time dashboards
- Custom report templates

**Backtesting**
- Walk-forward optimization
- Monte Carlo simulations
- Scenario analysis

### 4. Optimize Performance
- Reduce API calls through batching
- Cache results for repeated analyses
- Parallel processing for multiple periods

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Nixtla/nixtla.git
cd nixtla/experiments/bitcoin-prediction
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```bash
export NIXTLA_API_KEY='your-key-here'
```

5. Run tests:
```bash
make test
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions focused and modular

Example:
```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description of what the function does.
    
    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : int
        Description of param2
        
    Returns
    -------
    bool
        Description of return value
    """
    # Implementation
    pass
```

## Testing

Before submitting changes:

1. Run module tests:
```bash
python test_modules.py
```

2. Test your changes with quick analysis:
```bash
python quick_analysis.py
```

3. Verify full analysis still works (if applicable):
```bash
python main.py
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Make your changes
4. Test thoroughly
5. Commit with clear messages:
```bash
git commit -m "Add feature: description"
```

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Open a pull request

## Pull Request Guidelines

- Describe what your PR does and why
- Reference any related issues
- Include test results
- Update documentation if needed
- Keep changes focused (one feature per PR)

## Ideas for Contributors

### Beginner-Friendly
- Add more examples to documentation
- Create additional test cases
- Improve error messages
- Add data validation checks

### Intermediate
- Implement new visualization types
- Add support for other cryptocurrencies
- Create configuration file support
- Optimize API usage

### Advanced
- Implement fine-tuning workflows
- Add real-time prediction pipeline
- Create trading strategy backtester
- Build web dashboard

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Join the Nixtla Slack community

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers
- Follow the project's code of conduct

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache 2.0).

Thank you for contributing! 🚀
