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


def list_files_in_directory(directory_path: str, extension: str = None) -> List[str]:
    """
    List all files in a directory, optionally filtered by extension.

    Args:
        directory_path: Path to the directory to list
        extension: Optional file extension filter (e.g., '.pdf')

    Returns:
        List of file paths
    """
    try:
        if not os.path.exists(directory_path):
            logger.warning(f"Directory does not exist: {directory_path}")
            return []

        files = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if extension is None or filename.endswith(extension):
                    files.append(file_path)

        logger.debug(f"Found {len(files)} files in {directory_path}")
        return files

    except OSError as e:
        logger.error(f"Error listing files in {directory_path}: {e}")
        logger.debug(traceback.format_exc())
        return []
    except Exception as e:
        logger.error(f"Unexpected error while listing files in {directory_path}: {e}")
        logger.debug(traceback.format_exc())
        return []


def read_file_contents(file_path: str) -> Optional[str]:
    """
    Read the contents of a file as a string.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents as string, or None if error occurs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logger.debug(f"Successfully read file: {file_path}")
        return content
    except OSError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        logger.debug(traceback.format_exc())
        return None
    except Exception as e:
        logger.error(f"Unexpected error while reading file {file_path}: {e}")
        logger.debug(traceback.format_exc())
        return None


def write_file_contents(file_path: str, content: str) -> bool:
    """
    Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file

    Returns:
        True if write was successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        logger.debug(f"Successfully wrote to file: {file_path}")
        return True
    except OSError as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        logger.debug(traceback.format_exc())
        return False
    except Exception as e:
        logger.error(f"Unexpected error while writing to file {file_path}: {e}")
        logger.debug(traceback.format_exc())
        return False


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


def get_file_size(file_path: str) -> Optional[int]:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes, or None if error occurs
    """
    try:
        size: int = os.path.getsize(file_path)
        logger.debug(f"File size for {file_path}: {size} bytes")
        return size
    except OSError as e:
        logger.error(f"Error getting size of {file_path}: {e}")
        logger.debug(traceback.format_exc())
        return None


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


def get_filename_without_extension(file_path: str) -> str:
    """
    Get the filename without its extension.

    Args:
        file_path: Full path to the file

    Returns:
        Filename without extension
    """
    try:
        filename = os.path.basename(file_path)
        return os.path.splitext(filename)[0]
    except Exception as e:
        logger.error(f"Error getting filename without extension: {e}")
        logger.debug(traceback.format_exc())
        return ""


def create_backup_file(original_path: str, backup_suffix: str = ".backup") -> Optional[str]:
    """
    Create a backup copy of a file.

    Args:
        original_path: Path to the original file
        backup_suffix: Suffix to add to the backup filename

    Returns:
        Path to the backup file, or None if error occurs
    """
    try:
        backup_path = original_path + backup_suffix

        # Read original file
        content = read_file_contents(original_path)
        if content is None:
            return None

        # Write backup file
        if write_file_contents(backup_path, content):
            logger.debug(f"Backup created: {backup_path}")
            return backup_path
        else:
            return None

    except Exception as e:
        logger.error(f"Error creating backup of {original_path}: {e}")
        logger.debug(traceback.format_exc())
        return None
