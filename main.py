# This Python file uses the following encoding: utf-8
import sys
import os
import glob
import pandas as pd


from PySide2.QtWidgets import QTabWidget, QPlainTextEdit, QMainWindow ,QApplication, QWidget, QLineEdit, QPushButton, QFileDialog, QMessageBox, QAction
from PySide2.QtCore import QFile, QFileInfo
from PySide2.QtUiTools import QUiLoader

class readme(QWidget):
    def __init__(self, parent=None):
        super(readme, self).__init__(parent)
        ui_file = QFile('readme.ui')
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.text = open('Readme.txt').read()
        self.readM = self.window.findChild(QPlainTextEdit, 'readM')
        self.readM.setPlainText(self.text)

        self.window.show()

class PyCSV(QMainWindow):
    def __init__(self, ui_file, parent=None):
        # Load ui file into program to display
        super(PyCSV, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.fileSelectCombine()
        self.fileSelectConvert()
        self.Readme()

        self.window.show()

    def uiconnect(self):
        self.inputPB = self.window.findChild(QPushButton, 'inputPB')
        self.inputLE = self.window.findChild(QLineEdit, 'inputLE')
        self.outputPB = self.window.findChild(QPushButton, 'outputPB')
        self.outputLE = self.window.findChild(QLineEdit, 'outputLE')
        self.nameLE = self.window.findChild(QLineEdit, 'nameLE')
        self.combinePB = self.window.findChild(QPushButton, 'combinePB')
        self.Help = self.window.findChild(QAction, 'actionHelp')
        self.inputPB_2 = self.window.findChild(QPushButton, 'inputPB_2')
        self.inputLE_2 = self.window.findChild(QLineEdit, 'inputLE_2')
        self.outputPB_2 = self.window.findChild(QPushButton, 'outputPB_2')
        self.outputLE_2 = self.window.findChild(QLineEdit, 'outputLE_2')
        self.nameLE_2 = self.window.findChild(QLineEdit, 'nameLE_2')
        self.combinePB_2 = self.window.findChild(QPushButton, 'combinePB_2')

    def fileSelectCombine(self):
        self.uiconnect()
        self.inputPB.clicked.connect(self.getFolderIn)
        self.outputPB.clicked.connect(self.getFolderOut)
        self.combinePB.clicked.connect(self.Combine)

    def getFolderIn(self):
        folder = QFileDialog.getExistingDirectory()
        self.inputLE.setText(folder)

    def getFolderOut(self):
        folder = QFileDialog.getExistingDirectory()
        self.outputLE.setText(folder)

    def Combine(self):
        print(self.inputLE.text())
        print(self.outputLE.text())
        if self.inputLE.text() == "" and self.outputLE.text() == "":
            QMessageBox.critical(
                None,
                "Error - Blank Fields",
                '''Your "Input Folder" and "Output Folder" fields were left blank,
fill in all fields and try again.''')
            return

        try:
            os.chdir(self.inputLE.text())
        except:
            QMessageBox.critical(
                None,
                "Error - Set Input Failed",
                '''Failed to set the input folder,
verify that you have selected a valid folder and try again.''')
            return

        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        #combine all files in the list
        try:
            combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        except:
            QMessageBox.critical(
                None,
                "Error - File Combine Failed",
                '''Failed to select and combine the input files,
verify that you have selected a valid folder and try again.''')
            return

        try:
            os.chdir(self.outputLE.text())
        except:
            QMessageBox.critical(
                None,
                "Error - Set Output Failed",
                '''Failed to set the output folder,
verify that you have selected a valid folder and try again.'''
                )

        Name = self.nameLE.text()

        def get_nonexistant_path(Name):

            if not os.path.exists(Name):
                return Name
            filename, file_extension = os.path.splitext(Name)
            i = 1
            new_fname = "{}-{}{}".format(filename, i, file_extension)
            while os.path.exists(new_fname):
                i += 1
                new_fname = "{}-{}{}".format(filename, i, file_extension)
            return new_fname

        fName = get_nonexistant_path(Name+".csv")

        combined_csv.to_csv( fName, index=False, encoding='utf-8-sig')

        QMessageBox.information(
            None,
            "Success",
            "Your files have been combined successfully!")
        self.clear()

    def clear(self):
        self.inputLE.clear()
        self.outputLE.clear()
        self.nameLE.clear()

    def Readme(self):
        self.Help.triggered.connect(self.fileOpen)

    def fileOpen(self):
        try:
            readme(self)
        except:
            print("load readme failed")

    def fileSelectConvert(self):
        self.uiconnect()
        self.inputPB_2.clicked.connect(self.getFileIn)
        self.outputPB_2.clicked.connect(self.getFileOut)
        self.combinePB_2.clicked.connect(self.Convert)

    def getFileIn(self):
        file = str(QFileDialog.getOpenFileName())
        self.inputLE_2.setText(file[2:-19])

        oName = QFileInfo(self.inputLE_2.text()).fileName()
        self.nameLE_2.setText(oName[:-5])

    def getFileOut(self):
        file = QFileDialog.getExistingDirectory()
        self.outputLE_2.setText(file)

    def Convert(self):
        print(self.inputLE_2.text())
        print(self.outputLE_2.text())
        if self.inputLE_2.text() == "" and self.outputLE_2.text() == "":
            QMessageBox.critical(
                None,
                "Error - Blank Fields",
                '''Your "Input File" and "Output Folder" fields were left blank,
fill in all fields and try again.''')
            return

        import_file_path = self.inputLE_2.text()
        try:
            print(import_file_path)
            read_file = pd.read_excel(import_file_path)
        except:
            QMessageBox.critical(
                None,
                "Error - File Read Failed",
                '''Failed to read the input file,
verify that it is a working excel file and try again.''')
            return

        try:
            os.chdir(self.outputLE_2.text())
        except:
            QMessageBox.critical(
                None,
                "Error - Set Output Failed",
                '''Failed to set the output folder,
verify that you have selected a valid folder and try again.'''
                )
            return

        Name = self.nameLE_2.text()

        def get_nonexistant_path(Name):

            if not os.path.exists(Name):
                return Name
            filename, file_extension = os.path.splitext(Name)
            i = 1
            new_fname = "{}-{}{}".format(filename, i, file_extension)
            while os.path.exists(new_fname):
                i += 1
                new_fname = "{}-{}{}".format(filename, i, file_extension)
            return new_fname

        fName = get_nonexistant_path(Name+".csv")

        read_file.to_csv(fName, index = None, encoding='utf-8-sig')

        QMessageBox.information(
            None,
            "Success",
            "Your files have been combined successfully!")
        self.inputLE_2.clear()
        self.nameLE_2.clear()


if __name__ == "__main__":
    app = QApplication([])
    widget = PyCSV('form.ui')
    sys.exit(app.exec_())
