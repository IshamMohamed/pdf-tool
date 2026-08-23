# This is an example of how to implement a new operation
# Copy this file and modify it for your specific operation

import logging
from argparse import Namespace

from pdf_tool.operations.base import Operation

logger = logging.getLogger("pdf_tool")

class ExampleOperation(Operation):
    """
    Example operation that demonstrates how to add a new operation.
    Replace this with your actual operation implementation.
    """
    
    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add operation-specific arguments to the parser."""
        # Add your operation's arguments here
        parser.add_argument(
            "--example-param", type=str, default="default",
            help="Example parameter for the example operation"
        )
    
    def execute(self, args: Namespace) -> None:
        """Execute the operation with the provided arguments."""
        logger.info(f"Running example operation with param: {args.example_param}")
        
        # Implement your operation's logic here
        # For example:
        # self.process_files(args.input, args.output, args.example_param)
        
        logger.info("Example operation completed.")