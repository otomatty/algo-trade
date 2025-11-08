# Python Backend

This directory contains the Python backend code for the algo-trade application.

## Structure

```
src-python/
├── scripts/              # Executable scripts called from Rust commands
├── modules/              # Feature modules
│   ├── data_collection/  # Data collection from APIs/CSV
│   ├── data_analysis/    # Technical analysis and indicators
│   ├── llm_integration/  # LLM API clients
│   ├── news_collection/ # News collection and sentiment analysis
│   └── backtest/         # Backtest engine
├── database/             # Database management and migrations
├── utils/                # Shared utilities
└── requirements.txt      # Python dependencies
```

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install TA-Lib (required for technical analysis):
   - macOS: `brew install ta-lib`
   - Linux: Follow [TA-Lib installation guide](https://ta-lib.org/install/)
   - Windows: Download from [TA-Lib website](https://ta-lib.org/install/)

## Communication with Rust

Python scripts are called from Rust Tauri commands via subprocess execution.
Communication is done via JSON over stdout/stdin.

## Environment Variables

Create a `.env` file in the project root for API keys:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

