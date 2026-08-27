from pathlib import Path
import logging
from argparse import Namespace
from PyQt5.QtCore import QThread, pyqtSignal

from pdf_tool.operations.squeeze import SqueezeOperation
from pdf_tool.operations.merge import MergeOperation


class LogEmitterHandler(logging.Handler):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        try:
            msg = self.format(record)
            self.signal.emit(msg)
        except Exception:
            pass


class SqueezeWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, input_dir: Path, output_dir: Path, dpi: int, quality: int, recursive: bool, overwrite: bool):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dpi = dpi
        self.quality = quality
        self.recursive = recursive
        self.overwrite = overwrite

    def run(self):
        logger = logging.getLogger('pdf_tool')
        handler = LogEmitterHandler(self.log_signal)
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(handler)

        try:
            operation = SqueezeOperation()
            operation.process_directory(
                input_dir=self.input_dir,
                output_dir=self.output_dir,
                dpi=self.dpi,
                jpeg_quality=self.quality,
                recursive=self.recursive,
                overwrite=self.overwrite
            )
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            logger.removeHandler(handler)


class MergeWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, input_dir: Path, output_dir: Path, file_name: str):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.file_name = file_name

    def run(self):
        logger = logging.getLogger('pdf_tool')
        handler = LogEmitterHandler(self.log_signal)
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(handler)

        try:
            args = Namespace(
                input=self.input_dir,
                output=self.output_dir,
                file_name=self.file_name
            )
            operation = MergeOperation()
            operation.execute(args)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            logger.removeHandler(handler)
