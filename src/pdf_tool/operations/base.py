from abc import ABC, abstractmethod
from argparse import Namespace

class Operation(ABC):
    """
    Base class for all operations in the PDF Tool.
    Each operation should implement its own parameters and execution logic.
    """
    
    @classmethod
    @abstractmethod
    def add_arguments(cls, parser) -> None:
        """
        Add operation-specific arguments to the argument parser.
        
        Args:
            parser: The argparse.ArgumentParser instance
        """
        pass
    
    @abstractmethod
    def execute(self, args: Namespace) -> None:
        """
        Execute the operation with the provided arguments.
        
        Args:
            args: Parsed command-line arguments
        """
        pass