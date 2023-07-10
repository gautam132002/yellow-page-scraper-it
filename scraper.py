import csv
import requests
import json
from tqdm import tqdm
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QProgressBar, QLabel, QFileDialog
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()

    def remove_duplicates(self):
        inp = self.file_path.replace(".csv", "_result.csv")

        with open(inp, 'r',encoding='ISO-8859-1', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
        unique_rows = [rows[0]]  

        for row in rows[1:]:
            if row not in unique_rows:
                unique_rows.append(row)

      
        output_file = inp

        with open(output_file, 'w', encoding='ISO-8859-1', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(unique_rows)

        print(f"Redundancies removed. Cleaned data saved to {output_file}")
        

    def run(self):

        save_path = self.file_path.replace(".csv", "_result.csv")

        f = open(save_path, "w", encoding="utf-8", newline="")
        writer = csv.writer(f,delimiter=';')
        writer.writerow(["RAGIONE SOCIALE"," INDIRIZZO","PROVINCIA","COMUNE","CAP","TELEFONO", "WHATSAPP", "EMAIL", "SITO INTERNET","DETAILS LINK"])

        with open(self.file_path, 'r', encoding='ISO-8859-1') as csvfile:
            # Create a CSV reader object with semicolon delimiter
            csvreader = csv.reader(csvfile, delimiter=';')

            # Skip the header row
            next(csvreader)

            # Get the total number of rows in the CSV file
            num_rows = sum(1 for _ in csvfile)

            # Reset the file pointer to the beginning of the file
            csvfile.seek(0)
            next(csvreader)  # Skip the header row again

            # Initialize the tqdm loader
            progress_bar = tqdm(csvreader, total=num_rows, desc="Processing Rows")

            # Create a list to store the existing data
            existing_data = []

            
            # Iterate over each row in the CSV file
            for i, row in enumerate(progress_bar):
                # Get the values from each column
                column_1 = row[0]
                column_2 = row[1]

                page_number = 1

                while True:
                    try:
                        # Construct the API URL
                        url = f"https://www.paginegialle.it/ricerca/{column_1}/{column_2}/p-{page_number}?output=json"
                        print(url)

                        # Make the API request
                        response = requests.get(url)

                        # Get the JSON response as a dictionary
                        json_data = response.json()

                        # Check if the data exists
                        if 'list' in json_data and 'out' in json_data['list'] and 'base' in json_data['list']['out']:
                            json_info = json_data['list']['out']['base']['results']
                            for k in json_info:
                                ds_ragsoc = ""
                                addr = ""
                                prov = ""
                                loc = ""
                                codloc = ""
                                ds_ls_telefoni = []
                                site_link = ""
                                email = ""
                                whatsapp = ""
                                p_link = ""

                                try:
                                    ds_ragsoc = str(k["ds_ragsoc"])
                                except KeyError:
                                    pass

                                try:
                                    addr = str(k["addr"])
                                except KeyError:
                                    pass

                                try:
                                    prov = str(k["prov"])
                                except KeyError:
                                    pass

                                try:
                                    loc = str(k["loc"])
                                except KeyError:
                                    pass

                                try:
                                    codloc = str(k["codloc"])
                                except KeyError:
                                    pass

                                try:
                                    ds_ls = k.get("ds_ls_telefoni", [])
                                    ds_ls_telefoni = ", " .join(ds_ls)
                                    
                        
                                except KeyError:
                                    pass

                                try:
                                    site_link = k["extra"]["site_link"]["url"]
                                    

                                except:
                                    site_link = ""

                                try:
                                    p_link = k["extra"]["urlms"]
                                except:
                                    p_link = ""

                                try:
                                    mail = k["ds_ls_email"]
                                    email = ", ".join(mail)
                                except:
                                    email = ""

                                try:
                                    wa = k["ds_ls_telefoni_whatsapp"]
                                    whatsapp = ", ".join(wa)
                                except:
                                    whatsapp = ""

                                # Check if the data already exists
                                data = [ds_ragsoc, addr, prov, loc, codloc, ds_ls_telefoni,whatsapp, email, site_link, p_link]
                                existing_data.append(data)
                                
                                writer.writerow(data)
                                

                        page_number += 1

                    except Exception as e:
                        # print(e)
                        break

                progress_percentage = int((i + 1) / num_rows * 100)
                self.progress_update.emit(progress_percentage)
        
        f.close()       
        self.finished.emit()

        # Eleminating redundancy

        self.remove_duplicates()





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Processing")
        self.resize(400, 200)

        self.setStyleSheet("background-color: #333333; color: #ffffff;")

        self.progress_label = QLabel("Select CSV file", self)
        self.progress_label.setGeometry(100, 80, 200, 20)
        self.progress_label.setFont(QFont("Arial", 12))

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 120, 200, 20)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #555555; color: #ffffff; }")

        self.select_file_button = QPushButton("Select File", self)
        self.select_file_button.clicked.connect(self.select_file)
        self.select_file_button.setGeometry(100, 120, 200, 50)
        self.select_file_button.setStyleSheet("background-color: #777777; color: #ffffff;")

        self.worker_thread = WorkerThread()
        self.worker_thread.progress_update.connect(self.update_progress)
        self.worker_thread.finished.connect(self.processing_finished)

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.worker_thread.file_path = file_path
                self.worker_thread.start()
                self.select_file_button.setVisible(False)
                self.progress_bar.setVisible(True)

    def update_progress(self, percentage):
        self.progress_bar.setValue(percentage)
        self.progress_label.setText(f"<font color='#90caf9'>Progress: {percentage}%</font>")
        self.progress_label.adjustSize()

    def processing_finished(self):
        QMessageBox.information(self, "Information", "Processing finished.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Set the dark theme style sheet
    style_sheet = """
        QMainWindow {
            background-color: #333333;
            color: #ffffff;
        }

        QLabel {
            color: #ffffff;
        }

        QProgressBar {
            background-color: #555555;
            color: #ffffff;
        }

        QPushButton {
            background-color: #000301;
            color: #ffffff;

        }
    """

    app.setStyleSheet(style_sheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
