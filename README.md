# EPUB to Markdown Chapter Extractor

A fast and reliable Python tool that converts EPUB files into individual chapter-wise Markdown files. Built with modern Python packaging using [uv](https://docs.astral.sh/uv/) - an extremely fast Python package and project manager written in Rust.

## Features

- 📚 **Smart Chapter Detection**: Automatically identifies and extracts chapters from EPUB structure
- 🔄 **Clean Conversion**: Converts HTML content to clean, readable Markdown
- 📝 **Intelligent Naming**: Creates meaningful filenames from chapter titles
- 📋 **Index Generation**: Automatically creates a table of contents with links
- 🚀 **Fast Processing**: Leverages uv's speed for dependency management and execution
- 🛡️ **Robust Parsing**: Handles various EPUB formats and edge cases
- 📖 **Metadata Extraction**: Preserves book information (title, author, language)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone or download this project**:
   ```bash
   git clone <repository-url>
   cd epub-to-markdown
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

### Usage

Convert an EPUB file to chapter-wise Markdown:

```bash
uv run main.py path/to/your/book.epub
```

**Example:**
```bash
uv run main.py "The Great Gatsby.epub"
```

This will create a folder named `The_Great_Gatsby_chapters/` containing:
- Individual `.md` files for each chapter (numbered and titled)
- `README.md` with book metadata and table of contents

### Advanced Usage

**Custom output directory:**
```bash
uv run main.py book.epub -o ./custom-output-folder
```

**Help and options:**
```bash
uv run main.py --help
```

## Project Structure

This project uses uv's modern Python project management:

```
epub-to-markdown/
├── .venv/              # Virtual environment (auto-created)
├── .python-version     # Python version specification
├── main.py            # Main application script
├── pyproject.toml     # Project configuration and dependencies
├── uv.lock           # Dependency lockfile
└── README.md         # This file
```

## Dependencies

The project uses these high-quality Python packages:

- **[ebooklib](https://pypi.org/project/EbookLib/)**: EPUB file parsing and manipulation
- **[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)**: HTML parsing and processing
- **[markdownify](https://pypi.org/project/markdownify/)**: HTML to Markdown conversion

All dependencies are managed through uv for fast, reliable installation.

## How It Works

1. **EPUB Parsing**: Uses `ebooklib` to parse the EPUB structure and reading order
2. **Content Extraction**: Extracts HTML content from each chapter document
3. **Title Detection**: Intelligently detects chapter titles from HTML headers
4. **HTML Processing**: Cleans and processes HTML using BeautifulSoup
5. **Markdown Conversion**: Converts cleaned HTML to Markdown format
6. **File Generation**: Creates numbered chapter files with clean names
7. **Index Creation**: Generates a comprehensive table of contents

## Output Format

### Chapter Files
Each chapter is saved as a separate Markdown file:
```
01_Chapter_1_Introduction.md
02_The_Great_Adventure_Begins.md
03_Meeting_the_Characters.md
...
```

### Index File
A `README.md` file is created with:
- Book metadata (title, author, language)
- Complete table of contents with links
- Chapter count and overview

## Development

### Project Setup with uv

This project demonstrates modern Python development with uv:

```bash
# Initialize new project
uv init epub-to-markdown

# Add dependencies
uv add ebooklib beautifulsoup4 markdownify

# Run the application
uv run main.py example.epub

# Add development dependencies (if needed)
uv add --dev pytest black ruff
```

### Why uv?

This project uses [uv](https://docs.astral.sh/uv/) instead of traditional pip/virtualenv because:

- ⚡ **10-100x faster** than pip for package installation
- 🔒 **Reliable dependency resolution** with lockfiles
- 🔄 **Unified tooling** - replaces pip, pip-tools, virtualenv
- 🦀 **Written in Rust** for maximum performance
- 🎯 **Modern Python packaging** standards
- 🔧 **Zero configuration** required

### Configuration

The `pyproject.toml` file contains all project metadata and dependencies:

```toml
[project]
name = "epub-to-md"
version = "0.1.0"
description = "A fast and reliable Python tool that converts EPUB files into individual chapter-wise Markdown files. "
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "beautifulsoup4>=4.13.4",
    "ebooklib>=0.19",
    "markdownify>=1.1.0",
]
```

## Troubleshooting

### Common Issues

**"No chapters found"**: 
- Some EPUB files have unusual structures. Try the alternative simple approach in the code comments.

**"Permission denied"**:
- Ensure you have write permissions in the output directory.

**"UnicodeDecodeError"**:
- The EPUB file might have encoding issues. The script handles most cases automatically.

### Getting Help

1. Check the console output for detailed error messages
2. Ensure your EPUB file is valid and not corrupted
3. Try with a different EPUB file to isolate the issue

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `uv run main.py test-file.epub`
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.

## Related Tools

- [uv Documentation](https://docs.astral.sh/uv/) - Learn more about the uv package manager
- [ebooklib Documentation](https://github.com/aerkalov/ebooklib) - EPUB processing library
- [Calibre](https://calibre-ebook.com/) - Comprehensive ebook management
