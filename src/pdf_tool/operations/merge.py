import logging
from argparse import Namespace
from pathlib import Path
from datetime import datetime

import pymupdf

from pdf_tool.operations.base import Operation

logger = logging.getLogger("pdf_tool")

class MergeOperation(Operation):
    """
    Operation to merge all PDF files in the input directory into a single PDF.
    """

    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add operation-specific arguments to the parser."""
        parser.add_argument(
            "--file-name", type=str, default="merged-{timestamp}.pdf",
            help="Output merged PDF file name. Use '{timestamp}' placeholder for current timestamp."
        )

    def execute(self, args: Namespace) -> None:
        """Execute the merge operation with the provided arguments."""
        input_dir = Path(args.input)
        output_dir = Path(args.output)

        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect PDF files in input directory (non-recursive)
        pdf_files = sorted(
            [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
        )
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return

        # Generate output file name with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = args.file_name.replace("{timestamp}", timestamp)
        output_path = output_dir / file_name

        logger.info(f"Merging {len(pdf_files)} files into {output_path}")

        # Create a new PDF and insert each document
        merged_doc = pymupdf.open()
        try:
            for pdf in pdf_files:
                try:
                    doc = pymupdf.open(str(pdf))
                    merged_doc.insert_pdf(doc)
                    doc.close()
                    logger.debug(f"Inserted {pdf}")
                except Exception as e:
                    logger.error(f"Failed to insert {pdf}: {e}")

            # Save merged document
            merged_doc.save(str(output_path))
            logger.info(f"Merged PDF saved to {output_path}")
        finally:
            merged_doc.close()
