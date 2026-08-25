import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QSpinBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from pdf_tool.operations.squeeze import SqueezeOperation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Tool")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Input/output selectors
        io_layout = QHBoxLayout()
        layout.addLayout(io_layout)

        io_layout.addWidget(QLabel("Input Folder:"))
        self.input_edit = QLineEdit(str(Path("input").absolute()))
        io_layout.addWidget(self.input_edit)
        input_btn = QPushButton("Browse")
        input_btn.clicked.connect(self.browse_input)
        io_layout.addWidget(input_btn)

        io_layout.addWidget(QLabel("Output Folder:"))
        self.output_edit = QLineEdit(str(Path("output").absolute()))
        io_layout.addWidget(self.output_edit)
        output_btn = QPushButton("Browse")
        output_btn.clicked.connect(self.browse_output)
        io_layout.addWidget(output_btn)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tabs.addTab(self.create_squeeze_tab(), "Squeeze")

    def browse_input(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Input Folder", self.input_edit.text())
        if directory:
            self.input_edit.setText(directory)

    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_edit.text())
        if directory:
            self.output_edit.setText(directory)

    def create_squeeze_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)

        # DPI
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(1, 600)
        self.dpi_spin.setValue(56)
        dpi_layout.addWidget(self.dpi_spin)
        l.addLayout(dpi_layout)

        # Quality
        q_layout = QHBoxLayout()
        q_layout.addWidget(QLabel("Quality:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(30)
        q_layout.addWidget(self.quality_spin)
        l.addLayout(q_layout)

        # Options
        self.no_recursive_cb = QCheckBox("No Recursive")
        l.addWidget(self.no_recursive_cb)
        self.overwrite_cb = QCheckBox("Overwrite")
        l.addWidget(self.overwrite_cb)

        # Run button
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_squeeze)
        l.addWidget(run_btn, alignment=Qt.AlignRight)

        return tab

    def run_squeeze(self):
        input_dir = Path(self.input_edit.text())
        output_dir = Path(self.output_edit.text())
        dpi = self.dpi_spin.value()
        quality = self.quality_spin.value()
        recursive = not self.no_recursive_cb.isChecked()
        overwrite = self.overwrite_cb.isChecked()

        try:
            operation = SqueezeOperation()
            operation.process_directory(
                input_dir=input_dir,
                output_dir=output_dir,
                dpi=dpi,
                jpeg_quality=quality,
                recursive=recursive,
                overwrite=overwrite
            )
            QMessageBox.information(self, "Success", "Squeeze operation completed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
