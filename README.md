# PDF Tool

A simple tool for batch processing PDF files to create optimized, lower-quality versions suitable for archiving or sharing.

## Features

- **Batch processing**: Convert all PDFs in a directory (and subdirectories) to optimized versions
- **Rasterization**: Converts PDF pages to images and reassembles them for consistent compression
- **Quality control**: Adjustable DPI and JPEG quality settings
- **Directory structure preservation**: Maintains the same folder structure in the output
- **Non-destructive**: Creates new files in a separate directory without modifying originals

## Requirements

- Python 3.7+
- Dependencies (listed in `requirements.txt`):
  - `pymupdf` (PyMuPDF)
  - `Pillow` (PIL)
  - `img2pdf`

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone this repository or download the files
2. Install dependencies as shown above
3. Create two directories:
   - `Original/` - Place your original PDF files here
   - `Low/` - Optimized PDFs will be saved here

## Usage

### Basic Usage

```bash
python pdf_lower.py
```

This will:
1. Process all PDF files in the `Original/` directory (and subdirectories)
2. Create optimized versions in the `Low/` directory with the same structure
3. Use default settings (56 DPI, JPEG quality 30)

### Advanced Options

```bash
python pdf_lower.py [OPTIONS]
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
python pdf_lower.py --dpi 72 --quality 40 --overwrite
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

Contains helper functions for file operations:
- Directory creation and validation
- File listing and filtering
- File reading/writing
- PDF file validation
- Backup creation

### `print_foo.py`

A simple example script that prints "foo" to the console.

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

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
