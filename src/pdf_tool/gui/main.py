import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QFormLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
    QTabWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QCheckBox,
    QTextEdit, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from .worker import SqueezeWorker, MergeWorker


class MainWindow(QMainWindow):
    """
    PDF Tool GUI: select folders, configure operations, and view logs.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Tool GUI")
        self.resize(800, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Input/output selectors
        form = QFormLayout()
        main_layout.addLayout(form)
        self.input_edit = QLineEdit(str(Path("input").absolute()))
        form.addRow(QLabel("Input Folder:"), self._folder_selector(self.input_edit, self.browse_input))
        self.output_edit = QLineEdit(str(Path("output").absolute()))
        form.addRow(QLabel("Output Folder:"), self._folder_selector(self.output_edit, self.browse_output))

        # Tabs for operations
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.tabs.addTab(self._create_squeeze_tab(), "Squeeze")
        self.tabs.addTab(self._create_merge_tab(), "Merge")

        # Progress and log
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Operation logs...")
        self.log_view.setVisible(False)
        main_layout.addWidget(self.log_view)

        # Thread worker reference
        self.worker = None

    def _folder_selector(self, line_edit: QLineEdit, callback) -> QWidget:
        widget = QWidget()
        h = QHBoxLayout(widget)
        h.setContentsMargins(0, 0, 0, 0)
        line_edit.setMinimumWidth(400)
        h.addWidget(line_edit)
        btn = QPushButton("Browse")
        btn.setFixedWidth(80)
        btn.clicked.connect(callback)
        h.addWidget(btn)
        return widget

    def browse_input(self):
        path = QFileDialog.getExistingDirectory(self, "Select Input Folder", self.input_edit.text())
        if path:
            self.input_edit.setText(path)

    def browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_edit.text())
        if path:
            self.output_edit.setText(path)

    def _create_squeeze_tab(self) -> QWidget:
        tab = QWidget()
        v = QVBoxLayout(tab)

        # DPI
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(10, 300)
        self.dpi_spin.setValue(56)
        h1.addWidget(self.dpi_spin)
        v.addLayout(h1)

        # Quality
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("JPEG Quality:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(30)
        h2.addWidget(self.quality_spin)
        v.addLayout(h2)

        # Options
        self.no_recursive_cb = QCheckBox("No Recursive")
        v.addWidget(self.no_recursive_cb)
        self.overwrite_cb = QCheckBox("Overwrite Existing")
        v.addWidget(self.overwrite_cb)

        # Spacer
        v.addStretch()

        # Run
        btn_h = QHBoxLayout()
        btn_h.addStretch()
        self.run_btn = QPushButton("Run Squeeze")
        self.run_btn.clicked.connect(self.run_squeeze)
        btn_h.addWidget(self.run_btn)
        v.addLayout(btn_h)

        return tab

    def run_squeeze(self):
        # Prepare UI
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)
        self.log_view.clear()
        self.log_view.setVisible(True)
        self.run_btn.setEnabled(False)

        # Collect parameters
        inp = Path(self.input_edit.text())
        out = Path(self.output_edit.text())
        dpi = self.dpi_spin.value()
        quality = self.quality_spin.value()
        recursive = not self.no_recursive_cb.isChecked()
        overwrite = self.overwrite_cb.isChecked()

        # Start worker
        self.worker = SqueezeWorker(inp, out, dpi, quality, recursive, overwrite)
        self.worker.log_signal.connect(self.log_view.append)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.error_signal.connect(self._on_error)
        self.worker.start()

    def _on_finished(self):
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        QMessageBox.information(self, "Done", "Squeeze operation completed.")

    def _on_error(self, message):
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Operation failed:\n{message}")

    def _create_merge_tab(self) -> QWidget:
        tab = QWidget()
        v = QVBoxLayout(tab)

        # Output file name
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Output File Name:"))
        self.merge_filename_edit = QLineEdit("merged-{timestamp}.pdf")
        h1.addWidget(self.merge_filename_edit)
        v.addLayout(h1)

        # Spacer
        v.addStretch()

        # Run button
        btn_h = QHBoxLayout()
        btn_h.addStretch()
        self.run_merge_btn = QPushButton("Run Merge")
        self.run_merge_btn.clicked.connect(self.run_merge)
        btn_h.addWidget(self.run_merge_btn)
        v.addLayout(btn_h)

        return tab

    def run_merge(self):
        # Prepare UI
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(True)
        self.log_view.clear()
        self.log_view.setVisible(True)
        self.run_merge_btn.setEnabled(False)

        # Collect parameters
        inp = Path(self.input_edit.text())
        out = Path(self.output_edit.text())
        filename = self.merge_filename_edit.text()

        # Start worker
        self.worker = MergeWorker(inp, out, filename)
        self.worker.log_signal.connect(self.log_view.append)
        self.worker.finished_signal.connect(self._on_merge_finished)
        self.worker.error_signal.connect(self._on_merge_error)
        self.worker.start()

    def _on_merge_finished(self):
        self.progress_bar.setVisible(False)
        self.run_merge_btn.setEnabled(True)
        QMessageBox.information(self, "Done", "Merge operation completed.")

    def _on_merge_error(self, message):
        self.progress_bar.setVisible(False)
        self.run_merge_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Operation failed:\n{message}")


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
