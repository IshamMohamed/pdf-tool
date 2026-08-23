#!/usr/bin/env python3
"""
Batch rasterize-and-compress PDFs:
- Reads all .pdf files under "Original" (recursively)
- Rasterizes pages at specified DPI, compresses as JPEG
- Reassembles into a PDF and saves into "Low" preserving directory structure
"""

import argparse
import io
import logging
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Optional, Union

import pymupdf  # PyMuPDF
import img2pdf
from PIL import Image

# Set up dedicated logger
logger = logging.getLogger("pdf_lower")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)


def compress_pdf_rasterize(
    input_path: Path,
    output_path: Path,
    dpi: int = 56,
    jpeg_quality: int = 30,
    overwrite: bool = False,
) -> bool:
    """
    Rasterize `input_path` and save compressed PDF to `output_path`.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        dpi: DPI for rasterization (lower = smaller file)
        jpeg_quality: JPEG quality (1-100, lower = smaller file)
        overwrite: Whether to overwrite existing output

    Returns:
        True on success, False on failure or skip
    """
    if output_path.exists() and not overwrite:
        logger.info(f"Skipping existing output: {output_path}")
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Processing: {input_path} -> {output_path} (dpi={dpi}, q={jpeg_quality})")

    doc: Optional[pymupdf.Document] = None
    try:
        doc = pymupdf.open(str(input_path))
    except (pymupdf.FileDataError, pymupdf.FileNotFoundError, RuntimeError) as e:
        logger.error(f"Failed to open PDF {input_path}: {e}")
        logger.debug(traceback.format_exc())
        return False

    assert doc is not None, "Document should be initialized"
    tmpdir = tempfile.mkdtemp(prefix="pdf_raster_")
    images: list[str] = []

    try:
        for pageno in range(doc.page_count):
            page = doc.load_page(pageno)
            zoom = dpi / 72.0
            matrix = pymupdf.Matrix(zoom, zoom)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            png_data = pixmap.tobytes(output="png")

            image = Image.open(io.BytesIO(png_data)).convert("RGB")
            img_path = Path(tmpdir) / f"page_{pageno+1:04d}.jpg"
            image.save(str(img_path), format="JPEG", quality=jpeg_quality, optimize=True)
            images.append(str(img_path))

            logger.debug(
                f"Rendered page {pageno+1}/{doc.page_count} -> {img_path} "
                f"({img_path.stat().st_size // 1024} KB)"
            )

        # Convert compressed JPEG images into a single PDF
        pdf_data: bytes = img2pdf.convert(images)
        if pdf_data is None:
            logger.error("Failed to convert images to PDF")
            return False

        with open(output_path, "wb") as f:
            f.write(pdf_data)

        orig_size = input_path.stat().st_size
        new_size = output_path.stat().st_size
        logger.info(
            f"Saved: {output_path} (orig {orig_size/1024/1024:.2f} MB -> "
            f"new {new_size/1024/1024:.2f} MB)"
        )
        return True

    except (RuntimeError, OSError, img2pdf.ImageOpenError) as e:
        logger.error(f"Failed processing {input_path}: {e}")
        logger.debug(traceback.format_exc())
        return False

    finally:
        # Cleanup temp images
        try:
            if 'tmpdir' in locals():
                shutil.rmtree(tmpdir)
        except OSError as cleanup_error:
            logger.debug(f"Failed to cleanup temp directory {tmpdir}: {cleanup_error}")

        if doc is not None:
            doc.close()


def process_directory(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    dpi: int = 56,
    jpeg_quality: int = 30,
    recursive: bool = True,
    overwrite: bool = False,
) -> None:
    """
    Process all PDF files in original_dir and save optimized versions to low_dir.

    Args:
        original_dir: Source directory containing PDF files
        low_dir: Output directory for optimized PDFs
        dpi: DPI for rasterization
        jpeg_quality: JPEG quality (1-100)
        recursive: Whether to process subdirectories
        overwrite: Whether to overwrite existing files
    """
    input_dir_path = Path(input_dir)
    output_dir_path = Path(output_dir)

    if not input_dir_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir_path}")
        raise FileNotFoundError(f"Original directory not found: {original_dir_path}")

    # Walk original_dir (recursively by default)
    for root, _, files in os.walk(input_dir_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(input_dir_path)
        target_root = output_dir_path / rel_path
        target_root.mkdir(parents=True, exist_ok=True)

        for filename in files:
            if not filename.lower().endswith(".pdf"):
                continue

            src = root_path / filename
            dst = target_root / filename

            try:
                _ = compress_pdf_rasterize(
                    src, dst, dpi=dpi, jpeg_quality=jpeg_quality, overwrite=overwrite
                )
            except (RuntimeError, OSError) as e:
                logger.error(f"Unhandled error while processing {src}: {e}")
                logger.debug(traceback.format_exc())

        if not recursive:
            break


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Batch rasterize+compress PDFs from 'Original' to 'Low'"
    )
    parser.add_argument(
        "--input", "-i", default="input", help="Source directory (default: input)"
    )
    parser.add_argument(
        "--output", "-o", default="output", help="Output directory (default: output)"
    )
    parser.add_argument(
        "--dpi", type=int, default=56,
        help="Render DPI (lower = smaller file, worse quality). Default 56"
    )
    parser.add_argument(
        "--quality", "-q", type=int, default=30,
        help="JPEG quality 1-100 (lower = smaller). Default 30"
    )
    parser.add_argument(
        "--no-recursive", action="store_true",
        help="Do not recurse into subdirectories"
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite existing files in output"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        process_directory(
            input_dir=args.input,
            output_dir=args.output,
            dpi=args.dpi,
            jpeg_quality=args.quality,
            recursive=not args.no_recursive,
            overwrite=args.overwrite,
        )
        logger.info("Batch processing finished.")
    except (RuntimeError, OSError, SystemExit) as e:
        logger.error(f"Fatal error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
