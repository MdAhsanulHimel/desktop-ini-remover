import sys
import os
import glob
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QMessageBox

class DesktopIniRemover(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Desktop.ini Remover")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()

        self.label = QLabel("Select a folder to remove 'desktop.ini' files", self)
        layout.addWidget(self.label)

        self.btn_select_folder = QPushButton("Select Folder", self)
        self.btn_select_folder.clicked.connect(self.select_folder)
        layout.addWidget(self.btn_select_folder)

        self.btn_delete_files = QPushButton("Delete 'desktop.ini' Files", self)
        self.btn_delete_files.clicked.connect(self.delete_files)
        self.btn_delete_files.setEnabled(False)  # Disabled until folder is selected
        layout.addWidget(self.btn_delete_files)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            self.label.setText(f"Selected Folder: {folder}")
            self.btn_delete_files.setEnabled(True)  # Enable the delete button

    def delete_files(self):
        if not self.selected_folder:
            return

        # Find all 'desktop.ini' files in the selected folder and subfolders
        ini_files = glob.glob(os.path.join(self.selected_folder, "**", "desktop.ini"), recursive=True)

        if not ini_files:
            QMessageBox.information(self, "No Files Found", "No 'desktop.ini' files found in the selected folder.")
            return

        # Ask for user confirmation
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                     f"Found {len(ini_files)} 'desktop.ini' files. Do you want to delete them?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            for file in ini_files:
                try:
                    os.remove(file)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not delete {file}\nError: {e}")

            QMessageBox.information(self, "Deletion Complete", f"Deleted {len(ini_files)} 'desktop.ini' files.")
            self.label.setText("Select a folder to remove 'desktop.ini' files")
            self.btn_delete_files.setEnabled(False)  # Disable button after deletion

app = QApplication(sys.argv)
window = DesktopIniRemover()
window.show()
sys.exit(app.exec())
