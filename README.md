# PDF Tool

A flexible tool for processing PDF files with different operations. Currently supports:
- **Squeeze**: Rasterize and compress PDF files to reduce size

The tool is designed with extensibility in mind, making it easy to add new operations in the future.

## Features

- **Operation-based architecture**: Use different operations for different PDF processing tasks
- **Batch processing**: Process all PDFs in a directory (and subdirectories)
- **Extensible design**: Easy to add new operations with their own parameters
- **Directory structure preservation**: Maintains the same folder structure in the output
- **Non-destructive**: Creates new files in a separate directory without modifying originals
- **Robust error handling**: Comprehensive logging and error handling for reliable operation

### Current Operations

1. **Squeeze**: Rasterize and compress PDF files to reduce size
   - Adjustable DPI for rasterization
   - Adjustable JPEG quality
   - Recursive directory processing
   - Overwrite control

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

2. Run the tool with required operation and optional parameters:
```bash
pdf-tool --operation OPERATION_NAME [GLOBAL_OPTIONS] [OPERATION_OPTIONS]
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

### Available Operations

#### Squeeze Operation

Rasterize and compress PDF files to reduce size.

```bash
pdf-tool squeeze [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--input`, `-i` | Source directory | `input` |
| `--output`, `-o` | Output directory | `output` |
| `--dpi` | Render DPI (lower = smaller files) | `56` |
| `--quality`, `-q` | JPEG quality (1-100, lower = smaller) | `30` |
| `--no-recursive` | Don't process subdirectories | `False` |
| `--overwrite` | Overwrite existing output files | `False` |
| `--debug` | Enable debug logging | `False` |

**Example:**
```bash
pdf-tool squeeze --dpi 72 --quality 40 --overwrite
```

### Global Options

These options apply to all commands:

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `--operation` | Operation to perform on PDF files | Yes | - |
| `--input`, `-i` | Source directory | No | `input` |
| `--output`, `-o` | Output directory | No | `output` |
| `--debug` | Enable debug logging | No | `False` |

**Example:**
```bash
pdf-tool --operation squeeze --input my_input --output my_output --dpi 72 --quality 40
```

**Example:**
```bash
python pdf_tool.py --dpi 72 --quality 40 --overwrite
```

### Directory Structure

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

## Architecture

The PDF Tool uses a Strategy pattern to implement different operations:

1. **Base Operation Class**: Defines the interface for all operations
2. **Operation Implementations**: Each operation is a separate class with its own parameters and logic
3. **CLI Integration**: The command-line interface dynamically loads and executes operations

This design makes it easy to add new operations by:
1. Creating a new operation class that inherits from the base `Operation` class
2. Implementing the required methods (`add_arguments` and `execute`)
3. Registering the operation in the CLI

## Adding New Operations

To add a new operation:

1. Create a new file in `src/pdf_tool/operations/` (e.g., `my_operation.py`)
2. Implement a class that inherits from `Operation`:
   ```python
   from pdf_tool.operations.base import Operation
   
   class MyOperation(Operation):
       @classmethod
       def add_arguments(cls, parser):
           # Add operation-specific arguments
           parser.add_argument('--my-param', type=int, default=10, help='My parameter')
       
       def execute(self, args):
           # Implement operation logic
           print(f"Running MyOperation with param: {args.my_param}")
   ```
3. Update the `get_operation_class` function in `main.py` to recognize the new operation
4. The new operation will automatically be available in the CLI

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
