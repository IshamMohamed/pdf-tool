# This file contains helper functions that can be used across the project

import os
import logging
import traceback
from typing import List, Optional, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.propagate = False  # Avoid duplicate logs if root logger is configured


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure that a directory exists, create it if it doesn't.

    Args:
        directory_path: Path to the directory to check/create

    Returns:
        True if directory exists or was created successfully, False otherwise
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.debug(f"Directory ensured: {directory_path}")
        return True
    except OSError as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        logger.debug(traceback.format_exc())
        return False
    except Exception as e:
        logger.error(f"Unexpected error while creating directory {directory_path}: {e}")
        logger.debug(traceback.format_exc())
        return False


def validate_pdf_file(file_path: str) -> bool:
    """
    Basic validation to check if a file appears to be a PDF.

    Args:
        file_path: Path to the file to validate

    Returns:
        True if file exists and has .pdf extension, False otherwise
    """
    if not os.path.exists(file_path):
        logger.warning(f"File does not exist: {file_path}")
        return False

    if get_file_extension(file_path) != '.pdf':
        logger.warning(f"File is not a PDF: {file_path}")
        return False

    # Additional validation could be added here
    # (e.g., checking magic number, file structure)

    logger.debug(f"PDF file validated: {file_path}")
    return True


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.

    Args:
        filename: The filename to extract extension from

    Returns:
        The file extension including the dot (e.g., '.pdf'),
        or empty string if no extension
    """
    try:
        _, ext = os.path.splitext(filename)
        return ext.lower()
    except Exception as e:
        logger.error(f"Error getting extension from {filename}: {e}")
        logger.debug(traceback.format_exc())
        return ""
