# PDF Tool

A flexible command-line tool for processing PDF files with pluggable operations. Built with the Strategy pattern, it allows you to add new PDF-processing operations easily.

## Features

- Operation-based architecture: define each PDF-processing task as an independent, reusable strategy
- Batch processing: process all PDFs in a directory (and subdirectories)
- Extensible design: add new operations with minimal code changes
- Directory structure preservation: output mirrors your input folder hierarchy
- Non-destructive: writes new files to an output directory, leaving originals untouched
- Robust logging: configurable debug output and error handling

## Installation

### Prerequisites

- Python 3.14 or higher
- pip

### Using a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -e .
```

### Direct Install

```bash
pip install .
```

## Usage

All commands share these **global options**:

| Option               | Description                        | Required | Default |
|----------------------|------------------------------------|----------|---------|
| `--operation NAME`   | Name of the operation to execute   | Yes      | —       |
| `--input, -i DIR`    | Source directory                   | No       | `input` |
| `--output, -o DIR`   | Output directory                   | No       | `output`|
| `--debug`            | Enable debug (verbose) logging     | No       | `False` |

To see available operations:

```bash
pdf-tool --help
```

### Squeeze Operation

Rasterize and compress PDF files to reduce size.

```bash
pdf-tool --operation squeeze [OPTIONS]
```

| Option               | Description                             | Default |
|----------------------|-----------------------------------------|---------|
| `--dpi DPI`          | Render density in DPI (lower=smaller)   | `56`    |
| `--quality, -q Q`    | JPEG quality (1–100, lower=smaller)     | `30`    |
| `--no-recursive`     | Disable recursion into subdirectories   | `False` |
| `--overwrite`        | Overwrite existing files in output      | `False` |

**Example**

```bash
# Compress PDFs in ./input, write to ./output with higher DPI
pdf-tool --operation squeeze --input ./input --output ./output --dpi 72 --quality 40 --debug
```

#### Tips for Squeeze Operation

- Start with defaults: `--dpi 56`, `--quality 30`.
- Higher DPI (72–150) preserves more detail but increases file size.
- Lower quality (10–30) reduces size but may introduce artifacts.
- For text-heavy PDFs, a higher DPI helps maintain readability.
- For image-heavy PDFs, you can often use lower DPI without noticeable quality loss.

#### Troubleshooting Squeeze Operation

- Permission errors: Ensure you have write access to the output directory.
- Large PDFs: Processing very large files may require more memory/time. Use `--debug` to inspect logs.
- Corrupt PDFs: Some files may fail to open or process. Check error messages in debug mode.

## Directory Structure

- Input directory:
  ```
  input/
  ├── file1.pdf
  └── subdir/
      └── file2.pdf
  ```

- Output directory (after squeeze):
  ```
  output/
  ├── file1.pdf
  └── subdir/
      └── file2.pdf
  ```

## Architecture

The Tool uses a Strategy pattern for operations:

1. **Base Operation class** defines the contract (`add_arguments`, `execute`).
2. **Concrete Operations** (e.g., `SqueezeOperation`) live in `src/pdf_tool/operations/`.
3. **CLI** in `src/pdf_tool/main.py` dynamically discovers and invokes operations.

### Adding a New Operation

1. Create `src/pdf_tool/operations/my_operation.py`:
   ```python
   from pdf_tool.operations.base import Operation

   class MyOperation(Operation):
       @classmethod
       def add_arguments(cls, parser):
           parser.add_argument('--foo', type=int, default=1, help='Example param')

       def execute(self, args):
           print(f"Running MyOperation with foo={args.foo}")
   ```
2. Register it in `get_operation_class` in `main.py`:
   ```python
   def get_operation_class(name):
       if name == 'squeeze':
           from pdf_tool.operations.squeeze import SqueezeOperation
           return SqueezeOperation
       elif name == 'myop':
           from pdf_tool.operations.my_operation import MyOperation
           return MyOperation
       else:
           raise ValueError(f"Unknown operation: {name}")
   ```

3. Run it:
   ```bash
   pdf-tool --operation myop --foo 42
   ```



## Troubleshooting

These general tips address common issues across operations:

- **Permissions**: Ensure you have write access to the output directory.
- **Large PDFs**: Processing very large files may require more memory or time. Use `--debug` to inspect logs.
- **Corrupt PDFs**: Some files may fail to open or process. Check error messages in debug mode.

## Contributing

Contributions welcome! Please fork, sign your commits, and open a PR.

## License

GPL-3.0 © Isham Mohamed