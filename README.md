# PDF Tool

A simple tool for batch processing PDF files to create optimized, lower-quality versions suitable for archiving or sharing.

## Features

- **Batch processing**: Convert all PDFs in a directory (and subdirectories) to optimized versions
- **Rasterization**: Converts PDF pages to images and reassembles them for consistent compression
- **Quality control**: Adjustable DPI and JPEG quality settings
- **Directory structure preservation**: Maintains the same folder structure in the output
- **Non-destructive**: Creates new files in a separate directory without modifying originals
- **Robust error handling**: Comprehensive logging and error handling for reliable operation

## Installation

### Prerequisites
- Python 3.14 or higher
- pip

### Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -e .
```

### Production Installation

#### Option 1: Direct Installation (Recommended)
```bash
pip install .
```

#### Option 2: Using requirements.txt
1. Generate pinned requirements:
```bash
pip install pip-tools
pip-compile pyproject.toml
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Run the tool:
```bash
pdf-tool [OPTIONS]
```

### Directory Structure

The tool preserves the directory structure from the input directory to the output directory.

#### Default Directories:

Before processing:
```
PDFTool/
├── input/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
```

After processing:
```
PDFTool/
├── input/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
├── output/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
```

#### Custom Directories:

You can specify custom input and output directories using the `--input` and `--output` options:
```bash
pdf-tool --input input_dir --output output_dir
```

## Usage

### Basic Usage

```bash
python pdf_tool.py
```

This will:
1. Process all PDF files in the `Original/` directory (and subdirectories)
2. Create optimized versions in the `Low/` directory with the same structure
3. Use default settings (56 DPI, JPEG quality 30)

### Advanced Options

```bash
python pdf_tool.py [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--original`, `-i` | Source directory | `Original` |
| `--low`, `-o` | Output directory | `Low` |
| `--dpi` | Render DPI (lower = smaller files) | `56` |
| `--quality`, `-q` | JPEG quality (1-100, lower = smaller) | `30` |
| `--no-recursive` | Don't process subdirectories | `False` |
| `--overwrite` | Overwrite existing output files | `False` |
| `--debug` | Enable debug logging | `False` |

**Example:**
```bash
python pdf_tool.py --dpi 72 --quality 40 --overwrite
```

### Directory Structure

Before processing:
```
PDFTool/
├── Original/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
```

After processing:
```
PDFTool/
├── Original/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
├── Low/
│   ├── document1.pdf
│   ├── subfolder/
│   │   └── document2.pdf
│   └── ...
```

## Utility Scripts

### `utils.py`

Contains helper functions for file operations with robust error handling and logging:
- Directory creation and validation
- File listing and filtering by extension
- File reading/writing with encoding support
- PDF file validation
- File size and extension utilities
- Backup creation

This module is designed to be reusable across multiple projects.

## Tips for Best Results

1. **Start with default settings** (56 DPI, quality 30) and adjust as needed
2. **Higher DPI** (72-150) preserves more detail but creates larger files
3. **Lower quality** (10-30) creates smaller files but may introduce artifacts
4. **For text-heavy PDFs**, you may need higher DPI to maintain readability
5. **For image-heavy PDFs**, you can often use lower DPI without noticeable quality loss

## Troubleshooting

- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Permission errors**: Ensure you have write access to the output directory
- **Large files**: Processing very large PDFs may require more memory
- **Corrupt PDFs**: Some PDFs may fail to process - check the error logs

## Contributing

Contributions are welcome! Please ensure your commits are signed using GPG for verification. See [GitHub's guide on commit signing](https://docs.github.com/en/authentication/managing-commit-signature-verification) for more information.

## License

This project is open source and available under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).
