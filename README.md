# Cursor Template

A powerful template project for AI-assisted development in Cursor IDE, featuring OpenAI integration, web scraping, and search capabilities.

## Features

- **OpenAI Integration**: Seamless integration with OpenAI's GPT models for text and image processing
- **Web Scraping**: Built-in web scraping capabilities using Playwright
- **Search Engine**: Integration with DuckDuckGo for web searches
- **Screenshot Verification**: Tools for capturing and verifying web page screenshots
- **Environment Management**: Flexible environment configuration with support for multiple .env files

## Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cursor-template.git
   cd cursor-template
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   python -m playwright install
   ```

5. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Project Structure

```
cursor-template/
├── tools/                  # Core utility tools
│   ├── llm_api.py         # OpenAI integration
│   ├── web_scraper.py     # Web scraping utilities
│   ├── screenshot_utils.py # Screenshot capture and verification
│   └── search_engine.py   # Search engine integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
└── .cursorrules           # Cursor IDE configuration
```

## Usage

### OpenAI Integration

```python
from tools.llm_api import query_llm

# Text query
response = query_llm("What is the capital of France?")

# Image query
response = query_llm(
    "What's in this image?",
    image_path="path/to/image.png"
)
```

### Web Scraping

```python
from tools.web_scraper import scrape_urls

# Scrape multiple URLs concurrently
results = scrape_urls(["https://example.com", "https://example.org"])
```

### Search Engine

```python
from tools.search_engine import search

# Perform a web search
results = search("your search query")
```

### Screenshot Verification

```python
from tools.screenshot_utils import take_screenshot_sync
from tools.llm_api import query_llm

# Take a screenshot
screenshot_path = take_screenshot_sync('https://example.com')

# Verify with OpenAI
response = query_llm(
    "What is the background color and title of this webpage?",
    image_path=screenshot_path
)
```

## Environment Configuration

The project supports multiple environment files in order of precedence:
1. `.env.local` (user-specific overrides)
2. `.env` (project defaults)
3. `.env.example` (example configuration)

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.