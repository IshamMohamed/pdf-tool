#!/usr/bin/env python3
"""
PDF Tool - A tool for processing PDF files with different operations.
"""

import argparse
import logging
import sys
import traceback
from pathlib import Path

# Set up dedicated logger
logger = logging.getLogger("pdf_tool")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)


def get_operation_class(operation_name: str):
    """Dynamically import and return the operation class."""
    if operation_name == "squeeze":
        from pdf_tool.operations.squeeze import SqueezeOperation
        return SqueezeOperation
    else:
        raise ValueError(f"Unknown operation: {operation_name}")


def main() -> None:
    """Main entry point for the script."""
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="PDF Tool - Process PDF files with different operations"
    )
    parser.add_argument(
        "--input", "-i", default="input", 
        help="Source directory (default: input)"
    )
    parser.add_argument(
        "--output", "-o", default="output", 
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    
    # Create subparsers for operations
    subparsers = parser.add_subparsers(
        title="operations", 
        dest="operation",
        required=True,
        help="Operation to perform on PDF files"
    )
    
    # Add operations
    squeeze_parser = subparsers.add_parser(
        "squeeze", 
        help="Rasterize and compress PDF files to reduce size"
    )
    
    # Get all operation classes and add their arguments
    SqueezeOperation = get_operation_class("squeeze")
    SqueezeOperation.add_arguments(squeeze_parser)
    
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        # Create and execute the operation
        operation_class = get_operation_class(args.operation)
        operation = operation_class()
        operation.execute(args)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()