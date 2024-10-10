import sys
import os
import pandas as pd
import re
import threading
from PyQt5 import QtWidgets, QtCore
from scrapper import start_scraping, pause_scraping, current_page, total_pages, scraper_signals  # Import signal
from Algorithms import heap_sort,bubble_sort,quick_sort, merge_sort, selection_sort, insertion_sort,counting_sort,radix_sort,bucket_sort,shell_sort,tim_sort,merge_columns
import time

selectedColumns = []

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data.columns)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])  
            else:
                return str(section + 1)  

    def update_data(self, new_data):
        """ Update the model with new data. """
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class ScraperApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Website Scraper")
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #def0eb;  /* Light Brown */
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3b5446;  /* Brown color */
                color: white;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3b5446;  /* Lighter brown on hover */
            }
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
            QProgressBar {
                text-align: center;
                color: black;
                font-weight: bold;
            }
            QPushButton:enabled {
                background-color: #3b5446;
                color: white;
            }
            QPushButton:disabled {
                background-color: #6f8177;  /* Dimmed color for disabled */
            color: white;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.is_scraping = False  
        self.first_time_load = True  

        self.start_button = QtWidgets.QPushButton("Start Scraping", self)
        self.start_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.start_button)

        self.pause_button = QtWidgets.QPushButton("Pause Scraping", self)
        self.pause_button.clicked.connect(self.pause_scraping)
        self.layout.addWidget(self.pause_button)

        self.layout.addWidget(QtWidgets.QLabel("Select Columns to Sort:"))
        self.checkbox_group = CheckBoxGroup([])
        self.layout.addWidget(self.checkbox_group)

        self.algorithm_combobox = QtWidgets.QComboBox(self)
        self.algorithm_combobox.addItems(["Heap Sort", "Quick Sort", "Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort","Counting Sort","Bucket Sort","Radix Sort", "Tim Sort", "Shell Sort"])
        self.layout.addWidget(QtWidgets.QLabel("Select Sorting Algorithm:"))
        self.layout.addWidget(self.algorithm_combobox)

        self.sort_button = QtWidgets.QPushButton("Sort Data", self)
        self.sort_button.clicked.connect(self.sort_data)
        self.layout.addWidget(self.sort_button)

        self.search_input = QtWidgets.QLineEdit(self)
        self.search_input.setPlaceholderText('Format: "column name":"text here" && "another column":"another text"')
        self.layout.addWidget(QtWidgets.QLabel("Search:"))
        self.layout.addWidget(self.search_input)


        self.search_button = QtWidgets.QPushButton("Search", self)
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)

        self.reset_button = QtWidgets.QPushButton("Reset Data", self)
        self.reset_button.clicked.connect(self.reset_data)
        self.layout.addWidget(self.reset_button)

        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.table_view)

        self.setLayout(self.layout)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        header.setStretchLastSection(True)

        self.layout.setStretch(0, 0)  
        self.layout.setStretch(1, 0)  
        self.layout.setStretch(2, 0)  
        self.layout.setStretch(3, 0)  
        self.layout.setStretch(4, 0) 
        self.layout.setStretch(5, 0) 
        self.layout.setStretch(6, 1) 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)

        scraper_signals.progress_signal.connect(self.update_progress_bar)

        self.scrape_thread = None
        self.current_df = None  
        self.start_button.setEnabled(True)  # Enable Start button initially
        self.pause_button.setEnabled(False)  # Disable Pause button initially


    def start_scraping(self):
        if self.scrape_thread is None or not self.scrape_thread.is_alive():
            self.is_scraping = True  
            self.scrape_thread = threading.Thread(target=self.run_scraping)
            self.scrape_thread.start()

            # Update button states
            self.start_button.setEnabled(False)  # Disable start button during scraping
            self.pause_button.setEnabled(True)   # Enable pause button


    def run_scraping(self):
        start_scraping()

    def pause_scraping(self):
        pause_scraping()
        self.is_scraping = False  

        # Update button states
        self.start_button.setEnabled(True)  # Re-enable start button
        self.pause_button.setEnabled(False)  # Disable pause button


def update_table(self):
    if os.path.exists("ebay.csv"):
        df = pd.read_csv("ebay.csv")
        if self.first_time_load:  
            self.current_df = df
            model = PandasModel(df)
            self.table_view.setModel(model)
            self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.checkbox_group = CheckBoxGroup(df.columns.tolist())  # Initialize the checkbox group
            self.layout.addWidget(self.checkbox_group)  # Add the checkbox group for the first time
            self.first_time_load = False  
        elif self.is_scraping:  
            self.current_df = df
            model = PandasModel(df)
            self.table_view.setModel(model)
            self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.checkbox_group.update_options(df.columns.tolist())  # Update options instead of recreating


    def sort_data(self):
        if self.current_df is not None:
            selected_columns = self.checkbox_group.get_selected_columns()  # Get selected columns
            if not selected_columns:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please select at least one column to sort.")
                return
            algorithm = self.algorithm_combobox.currentText().lower() 

            start_time = time.time()
        
            sorted_df = self.sort_dataframe(self.current_df, selected_columns, algorithm)  # Pass selected columns
        
            elapsed_time = time.time() - start_time
        
            self.table_view.setModel(PandasModel(sorted_df))
            self.current_df = sorted_df  
        
            QtWidgets.QMessageBox.information(self, "Sorting Complete", f"Time taken to sort: {elapsed_time:.4f} seconds")

    def sort_dataframe(self, df, columns, algorithm):
        global selectedColumns
        if len(selectedColumns) == 1:
            if algorithm == "heap sort":
                df = heap_sort(df, selectedColumns[0])
            elif algorithm == "quick sort":
                df = quick_sort(df, selectedColumns[0])
            elif algorithm == "bubble sort":
                df = bubble_sort(df, selectedColumns[0])
            elif algorithm == "selection sort":
                df = selection_sort(df, selectedColumns[0])
            elif algorithm == "merge sort":
                df = merge_sort(df, selectedColumns[0])
            elif algorithm == "insertion sort":
                df = insertion_sort(df, selectedColumns[0])
            elif algorithm == "counting sort":
                df = counting_sort(df, selectedColumns[0])
            elif algorithm == "bucket sort":
                df = bucket_sort(df, selectedColumns[0])
            elif algorithm == "radix sort":
                df = radix_sort(df, selectedColumns[0])
            elif algorithm == "shell sort":
                df = shell_sort(df, selectedColumns[0])
            elif algorithm == "tim sort":
                df = tim_sort(df, selectedColumns[0])
        elif ((len(selectedColumns) > 1) and not(selectedColumns.__contains__("Price") or selectedColumns.__contains__("Miles") or selectedColumns.__contains__("Rating") or selectedColumns.__contains__("Reviews"))):
            df = merge_columns(df,selectedColumns)
            if algorithm == "heap sort":
                df = heap_sort(df, 'merged_column')
            elif algorithm == "quick sort":
                df = quick_sort(df, 'merged_column')
            elif algorithm == "bubble sort":
                df = bubble_sort(df, 'merged_column')
            elif algorithm == "selection sort":
                df = selection_sort(df, 'merged_column')
            elif algorithm == "merge sort":
                df = merge_sort(df, 'merged_column')
            elif algorithm == "insertion sort":
                df = insertion_sort(df, 'merged_column')
            elif algorithm == "counting sort":
                df = counting_sort(df, 'merged_column')
            elif algorithm == "bucket sort":
                df = bucket_sort(df, 'merged_column')
            elif algorithm == "radix sort":
                df = radix_sort(df, 'merged_column')
            elif algorithm == "shell sort":
                df = shell_sort(df, 'merged_column')
            elif algorithm == "tim sort":
                df = tim_sort(df, 'merged_column')
            df = df.drop(columns=['merged_column'])
        elif ((len(selectedColumns) > 1)):
            df = df.sort_values(by=selectedColumns)
        else:
             QtWidgets.QMessageBox.warning(self, "Warning", "Please select a column.")
        return df



    def update_progress_bar(self, current_page):
        if total_pages > 0:
            progress = (current_page / total_pages) * 100
            self.progress_bar.setValue(int(progress))
        else:
            self.progress_bar.setValue(0)
    
    def perform_search(self):
        if self.current_df is not None:
            search_text = self.search_input.text()

            if search_text:  # Check if the search input is not empty
                try:
                    # Parse the search text for multiple column-value pairs
                    pattern = r'"([^"]+)":"([^"]+)"'
                    matches = re.findall(pattern, search_text)
                    if not matches:
                        raise ValueError("Invalid search format. Please use the format: \"column_name\":\"text\".")

                    # Filter the DataFrame based on the parsed column-value pairs
                    search_results = self.current_df
                    for column_name, value in matches:
                        if column_name in search_results.columns:
                            search_results = self.search(search_results, column_name, value)
                        else:
                            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

                    if not search_results.empty:
                        self.table_view.setModel(PandasModel(search_results))  # Update table with search results
                    else:
                        QtWidgets.QMessageBox.information(self, "No Results", "No matches found.")
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Warning", str(e))
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a search term.")

    def search(self, df, column_name, text):
        return df[df[column_name].astype(str).str.contains(text, case=False, na=False)]

    def reset_data(self):
        if os.path.exists("ebay.csv"):
            self.current_df = pd.read_csv("ebay.csv") 
            self.table_view.setModel(PandasModel(self.current_df)) 
            self.search_input.clear() 

class CheckBoxGroup(QtWidgets.QWidget):
    def __init__(self, options):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.var_list = []
        self.checkboxes = []
        self.update_options(options)  # Initialize checkboxes with options

    def update_options(self, options):
        # Clear existing checkboxes and create new ones
        for cb in self.checkboxes:
            self.layout.removeWidget(cb)
            cb.deleteLater()  # Remove and delete the old checkboxes
        
        self.checkboxes = []  # Clear the old list
        self.var_list = []  # Clear the old vars
        
        for option in options:
            var = QtCore.pyqtSignal(bool)
            cb = QtWidgets.QCheckBox(option)
            cb.setChecked(False)
            cb.stateChanged.connect(lambda state, option=option: self.update_selection(state, option))
            self.checkboxes.append(cb)
            self.layout.addWidget(cb)
            self.var_list.append(var)

    def update_selection(self, state, option):
        global selectedColumns
        if state == QtCore.Qt.Checked:
            selectedColumns.append(option)
        else:
            selectedColumns.remove(option)
        print(selectedColumns)

    def get_selected_columns(self):
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())
