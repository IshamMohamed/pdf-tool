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
from pathlib import Path
from typing import Optional, Union

import fitz  # PyMuPDF
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

    doc: Optional[fitz.Document] = None
    try:
        doc = fitz.open(str(input_path))
    except (fitz.FileDataError, fitz.FileNotFoundError, RuntimeError) as e:
        logger.exception(f"Failed to open PDF {input_path}: {e}")
        return False

    assert doc is not None, "Document should be initialized"
    tmpdir = tempfile.mkdtemp(prefix="pdf_raster_")
    images: list[str] = []

    try:
        for pageno in range(doc.page_count):
            page = doc.load_page(pageno)
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            png_bytes = pix.tobytes(output="png")

            im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
            img_path = Path(tmpdir) / f"page_{pageno+1:04d}.jpg"
            im.save(str(img_path), format="JPEG", quality=jpeg_quality, optimize=True)
            images.append(str(img_path))

            logger.debug(
                f"Rendered page {pageno+1}/{doc.page_count} -> {img_path} "
                f"({img_path.stat().st_size // 1024} KB)"
            )

        # Convert compressed JPEG images into a single PDF
        pdf_bytes = img2pdf.convert(images)
        if pdf_bytes is None:
            logger.error("Failed to convert images to PDF")
            return False

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        orig_size = input_path.stat().st_size
        new_size = output_path.stat().st_size
        logger.info(
            f"Saved: {output_path} (orig {orig_size/1024/1024:.2f} MB -> "
            f"new {new_size/1024/1024:.2f} MB)"
        )
        return True

    except (RuntimeError, OSError, img2pdf.ImageOpenError) as e:
        logger.exception(f"Failed processing {input_path}: {e}")
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
    original_dir: Union[str, Path],
    low_dir: Union[str, Path],
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
    original_dir_path = Path(original_dir)
    low_dir_path = Path(low_dir)

    if not original_dir_path.exists():
        raise FileNotFoundError(f"Original directory not found: {original_dir_path}")

    # Walk original_dir (recursively by default)
    for root, _, files in os.walk(original_dir_path):
        root_path = Path(root)
        rel_path = root_path.relative_to(original_dir_path)
        target_root = low_dir_path / rel_path
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
                logger.exception(f"Unhandled error while processing {src}: {e}")

        if not recursive:
            break


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Batch rasterize+compress PDFs from 'Original' to 'Low'"
    )
    parser.add_argument(
        "--original", "-i", default="Original", help="Source directory (default: Original)"
    )
    parser.add_argument(
        "--low", "-o", default="Low", help="Output directory (default: Low)"
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
            original_dir=args.original,
            low_dir=args.low,
            dpi=args.dpi,
            jpeg_quality=args.quality,
            recursive=not args.no_recursive,
            overwrite=args.overwrite,
        )
        logger.info("Batch processing finished.")
    except (RuntimeError, OSError, SystemExit) as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
