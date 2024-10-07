# scraper_app.py
import sys
import os
import pandas as pd
import threading
from PyQt5 import QtWidgets, QtCore
from webscraper import start_scraping, pause_scraping, current_page, total_pages  # Import functions and variables from scrapper.py

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

        # Start and Pause Buttons
        self.start_button = QtWidgets.QPushButton("Start Scraping", self)
        self.start_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.start_button)

        self.pause_button = QtWidgets.QPushButton("Pause Scraping", self)
        self.pause_button.clicked.connect(self.pause_scraping)
        self.layout.addWidget(self.pause_button)

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
        self.layout.setStretch(3, 1)  # Table View to take all remaining space

        # Timer to update the table
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)

        # Timer to update the progress bar
        self.progress_timer = QtCore.QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_bar)
        self.progress_timer.start(1000)

        self.scrape_thread = None

    def start_scraping(self):
        if self.scrape_thread is None or not self.scrape_thread.is_alive():
            self.scrape_thread = threading.Thread(target=self.run_scraping)
            self.scrape_thread.start()
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def run_scraping(self):
        start_scraping()

    def pause_scraping(self):
        pause_scraping()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def update_table(self):
        # Load the CSV file and display it in the table
        if os.path.exists("ebay.csv"):
            df = pd.read_csv("ebay.csv")
            model = PandasModel(df)
            self.table_view.setModel(model)
            self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def update_progress_bar(self):
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
