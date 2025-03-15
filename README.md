# MCP Server - GitHub and AlphaVantage API Integration

## Overview
This MCP (Modular Conversational Platform) server provides tools to interact with the GitHub API and AlphaVantage API. The server enables fetching user and repository details from GitHub, searching repositories, and performing technical analysis on stock market data using AlphaVantage.

## Features
- Search GitHub users and repositories.
- Fetch details of a GitHub user or repository.
- Retrieve public repositories of a GitHub user.
- Perform stock market analysis using AlphaVantage, including:
  - Fetching intraday stock data.
  - Calculating moving averages.
  - Identifying bullish or bearish trends.
  - Detecting golden and death crosses.

## Installation
Ensure you have Python installed (>=3.8) and install the necessary dependencies:

install uv package manager
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
## Setup
1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```
2. install the dependencies
```sh
uv add -r 'requirements.txt'
```

3. Set up your AlphaVantage API key in the `.env` variable.
```sh
finance_server=apikey
```
4. Run the MCP server:
```sh
mcp install finance_server.py
mcp install githubMCP.py
```



## License
This project is open-source under the MIT License.

