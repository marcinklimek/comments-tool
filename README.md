# Comments Tool

A Python tool for processing comments in C/C++ source files, with special support for handling Japanese text. This tool helps you identify, extract, and manage Japanese comments in your C/C++ codebase.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- 🔍 Scan files for Japanese characters
- 📝 Extract and process comments from C/C++ source files
- 💬 Handle both single-line (`//`) and multi-line (`/* */`) comments
- 🧹 Remove BOM characters from files
- 🔤 Scan for non-ASCII characters
- 📚 Generate translation dictionary - for the future use
- 📊 Detailed logging and progress tracking

## Installation

### Prerequisites

- Python 3.8 or higher
- UV package manager (recommended) or pip

### Using UV (Recommended)

1. Install UV if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone <repository-url>
cd translate-jp
```

3. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
```

4. Install the package:
```bash
uv pip install -e .
```

## Usage

After installation, you can use the tool in several ways:

### Command Line Interface

```bash
# Scan files for Japanese characters
comment_tool --scan

# Scan for non-ASCII characters in a specific file
comment_tool --scan-non-ascii --file path/to/file

# Scan files for BOM characters
comment_tool --scan-bom

# Remove BOM characters from files
comment_tool --remove-bom

# Process files and extract Japanese comments
comment_tool
```

## Output

The tool generates the following files:
- `translations.json`: Contains extracted Japanese comments and their translations
- `translation.log`: Processing details and debug information

## Development

### Setting Up Development Environment

1. Clone the repository and create a virtual environment:
```bash
git clone https://github.com/marcinklimek/comments-tool.git
cd comments-tool
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
```

2. Install development dependencies:
```bash
uv pip install -e ".[dev]"
pre-commit install --install-hooks
```

### Development Tools

- **Code Formatting**: Black
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Pre-commit Hooks**: Automatically run checks before commits

### Running Tests

```bash
# Run pre-commit checks
pre-commit run --all-files

# Run type checking
mypy src/comment_tool
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to myself who have helped shape this project
- Special thanks to the open source community for their valuable tools and libraries

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/marcinklimek/comments-tool/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your problem and environment

## Roadmap

- [ ] Add support for more programming languages
- [ ] Implement machine translation integration
- [ ] Add GUI interface
- [ ] Support for batch processing
- [ ] Add more comment extraction patterns

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.
