import sys
import os
import pandas as pd
import threading
from PyQt5 import QtWidgets, QtCore
from scrapper import start_scraping, pause_scraping, current_page, total_pages, scraper_signals  # Import signal

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
                return str(self._data.columns[section])  # Return column headers
            else:
                return str(section + 1)  # Optionally return row numbers (1-indexed)

    def update_data(self, new_data):
        """ Update the model with new data. """
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class ScraperApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("eBay Scraper")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.layout.addWidget(self.progress_bar)


        self.is_scraping = False  # Indicates if scraping is active
        self.first_time_load = True  # Indicates if the table has been loaded for the first time

        # Start and Pause Buttons
        self.start_button = QtWidgets.QPushButton("Start Scraping", self)
        self.start_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.start_button)

        self.pause_button = QtWidgets.QPushButton("Pause Scraping", self)
        self.pause_button.clicked.connect(self.pause_scraping)
        self.layout.addWidget(self.pause_button)

        # Column Selection ComboBox
        self.column_combobox = QtWidgets.QComboBox(self)
        self.layout.addWidget(QtWidgets.QLabel("Select Column to Sort:"))
        self.layout.addWidget(self.column_combobox)

        # Algorithm Selection ComboBox
        self.algorithm_combobox = QtWidgets.QComboBox(self)
        self.algorithm_combobox.addItems(["Heap Sort", "Quick Sort", "Bubble Sort"])  # Add more algorithms as needed
        self.layout.addWidget(QtWidgets.QLabel("Select Sorting Algorithm:"))
        self.layout.addWidget(self.algorithm_combobox)

        # Sort Button
        self.sort_button = QtWidgets.QPushButton("Sort Data", self)
        self.sort_button.clicked.connect(self.sort_data)
        self.layout.addWidget(self.sort_button)

        # Table View for displaying scraped data
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.table_view)

        # Set layout
        self.setLayout(self.layout)

        # Allow columns to be resizable
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        header.setStretchLastSection(True)

        # Set stretch factors
        self.layout.setStretch(0, 0)  # Progress Bar
        self.layout.setStretch(1, 0)  # Start Button
        self.layout.setStretch(2, 0)  # Pause Button
        self.layout.setStretch(3, 0)  # Column Selection
        self.layout.setStretch(4, 0)  # Algorithm Selection
        self.layout.setStretch(5, 0)  # Sort Button
        self.layout.setStretch(6, 1)  # Table View to take all remaining space

        # Timer to update the table
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)

        # Connect the scraper signal to the progress bar update method
        scraper_signals.progress_signal.connect(self.update_progress_bar)

        self.scrape_thread = None
        self.current_df = None  # Store the current DataFrame

    def start_scraping(self):
        if self.scrape_thread is None or not self.scrape_thread.is_alive():
            self.is_scraping = True  # Set scraping to active
            self.scrape_thread = threading.Thread(target=self.run_scraping)
            self.scrape_thread.start()
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def run_scraping(self):
        start_scraping()

    def pause_scraping(self):
        pause_scraping()
        self.is_scraping = False  # Set scraping to inactive
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def update_table(self):
        # Load the CSV file and display it in the table if conditions are met
        if os.path.exists("ebay.csv"):
            df = pd.read_csv("ebay.csv")
            if self.first_time_load:  # Load table for the first time
                self.current_df = df
                model = PandasModel(df)
                self.table_view.setModel(model)
                self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.column_combobox.clear()
                self.column_combobox.addItems(df.columns.tolist())
                self.first_time_load = False  # Set first time load to False after loading
            elif self.is_scraping:  # Update table only if scraping is active
                self.current_df = df
                model = PandasModel(df)
                self.table_view.setModel(model)
                self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def sort_data(self):
        if self.current_df is not None:
            # Get selected column name and sorting algorithm
            column_name = self.column_combobox.currentText()
            algorithm = self.algorithm_combobox.currentText().lower()  # Convert to lowercase for matching
            
            # Sort the DataFrame
            sorted_df = self.sort_dataframe(self.current_df, column_name, algorithm)
            # Update the model with sorted data
            self.table_view.setModel(PandasModel(sorted_df))
            self.current_df = sorted_df  # Update the current DataFrame to the sorted one

    def sort_dataframe(self, df, column_name, algorithm):
        if algorithm == "heap sort":
            return self.heap_sort(df, column_name)
        elif algorithm == "quick sort":
            return self.quick_sort(df, column_name)
        elif algorithm == "bubble sort":
            return self.bubble_sort(df, column_name)
        # Add other algorithms here as needed
        return df  # Return unchanged if no valid algorithm is found

    def heap_sort(self, df, column_name):
        """ Perform heap sort on the specified column of the DataFrame. """
        # Build heap
        n = len(df)
        arr = df[column_name].tolist()  # Convert the column to a list
        
        def heapify(arr, n, i):
            largest = i  # Initialize largest as root
            left = 2 * i + 1  # left = 2*i + 1
            right = 2 * i + 2  # right = 2*i + 2
            
            # See if left child of root exists and is greater than root
            if left < n and arr[left] > arr[largest]:
                largest = left
            
            # See if right child of root exists and is greater than root
            if right < n and arr[right] > arr[largest]:
                largest = right
            
            # Change root if needed
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]  # Swap
                heapify(arr, n, largest)  # Recursively heapify the affected sub-tree

        # Build heap (rearrange array)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        # One by one extract an element from heap
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # Swap
            heapify(arr, i, 0)
        
        # Create a new DataFrame to reflect the sorted order
        sorted_df = df.iloc[[df[column_name].tolist().index(x) for x in arr]].reset_index(drop=True)
        return sorted_df

    def quick_sort(self, df, column_name):
        """ Quick sort implementation. """
        arr = df[column_name].tolist()  # Convert the column to a list
        self.quick_sort_helper(arr, 0, len(arr) - 1, df)
        return df

    def quick_sort_helper(self, arr, low, high, df):
        if low < high:
            # pi is partitioning index
            pi = self.partition(arr, low, high, df)

            # Recursively sort elements before partition and after partition
            self.quick_sort_helper(arr, low, pi - 1, df)
            self.quick_sort_helper(arr, pi + 1, high, df)

    def partition(self, arr, low, high, df):
        pivot = arr[high]  # pivot
        i = low - 1  # Index of smaller element
        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1  # increment index of smaller element
                arr[i], arr[j] = arr[j], arr[i]  # swap
        arr[i + 1], arr[high] = arr[high], arr[i + 1]  # swap pivot with the element at i+1
        return i + 1

    def bubble_sort(self, df, column_name):
        """ Bubble sort implementation. """
        arr = df[column_name].tolist()  # Convert the column to a list
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                # Traverse the array from 0 to n-i-1. Swap if the element found is greater than the next element
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
        
        # Create a new DataFrame to reflect the sorted order
        sorted_df = df.iloc[[df[column_name].tolist().index(x) for x in arr]].reset_index(drop=True)
        return sorted_df

    def update_progress_bar(self, current_page):
        # Update the progress bar based on current_page and total_pages
        if total_pages > 0:
            progress = (current_page / total_pages) * 100
            self.progress_bar.setValue(int(progress))
        else:
            self.progress_bar.setValue(0)
    
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())
