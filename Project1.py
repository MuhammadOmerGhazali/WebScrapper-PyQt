import sys
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import random
from operator import itemgetter


class ScraperApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScraperApp, self).__init__()
        self.initUI()
        self.entities = []  # Will store the scraped data
    
    def initUI(self):
        self.setWindowTitle("Web Scraper App")
        self.setGeometry(100, 100, 800, 600)

        # Main Layout with stacked widget for different pages
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create welcome page
        self.welcome_page = self.create_welcome_page()
        self.central_widget.addWidget(self.welcome_page)

        # Create scraping page
        self.scraping_page = self.create_scraping_page()
        self.central_widget.addWidget(self.scraping_page)

        # Create sorting page
        self.sorting_page = self.create_sorting_page()
        self.central_widget.addWidget(self.sorting_page)

        self.central_widget.setCurrentWidget(self.welcome_page)  # Show welcome page first

        self.is_paused = False
        self.scrape_thread = None

    def create_welcome_page(self):
        welcome_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Set the background color to light brown
        welcome_widget.setStyleSheet("background-color: #F5DEB3;")  # Light brown background

        # Welcome text
        self.welcome_label = QtWidgets.QLabel("Welcome to Web Scraping App")
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #8B4513;")  # Dark brown text

        # Scraping button
        self.scraping_btn = QtWidgets.QPushButton("Start Scraping")
        self.scraping_btn.setStyleSheet("background-color: #8B4513; color: white; font-size: 18px; padding: 10px;")
        self.scraping_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.scraping_page))

        # Sorting button
        self.sorting_btn = QtWidgets.QPushButton("Start Sorting")
        self.sorting_btn.setStyleSheet("background-color: #8B4513; color: white; font-size: 18px; padding: 10px;")
        self.sorting_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.sorting_page))

        # Add some spacing between elements
        layout.addStretch()
        layout.addWidget(self.welcome_label)
        layout.addSpacing(40)
        layout.addWidget(self.scraping_btn)
        layout.addSpacing(20)
        layout.addWidget(self.sorting_btn)
        layout.addStretch()

        welcome_widget.setLayout(layout)
        return welcome_widget

    def create_scraping_page(self):
        scraping_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Set the background color to light brown and style the elements
        scraping_widget.setStyleSheet("background-color: #F5DEB3;")  # Light brown background

        # Input field for URL
        self.url_label = QtWidgets.QLabel("URL:")
        self.url_label.setStyleSheet("font-size: 16px; color: #8B4513;")
        self.url_input = QtWidgets.QLineEdit()
        self.url_input.setStyleSheet("padding: 5px; font-size: 14px;")

        # Attributes selection (CheckBoxes)
        self.attribute_label = QtWidgets.QLabel("Select Attributes to Scrape:")
        self.attribute_label.setStyleSheet("font-size: 16px; color: #8B4513;")

        self.attribute_checkboxes = []
        for attr in ["ID", "Name", "Category", "Price", "Stock", "Rating", "Date"]:
            checkbox = QtWidgets.QCheckBox(attr)
            self.attribute_checkboxes.append(checkbox)

        # Start, pause, resume buttons
        self.start_btn = QtWidgets.QPushButton("Start Scraping")
        self.start_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.start_btn.clicked.connect(self.start_scraping)

        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.pause_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.pause_btn.clicked.connect(self.pause_scraping)

        self.resume_btn = QtWidgets.QPushButton("Resume")
        self.resume_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.resume_btn.clicked.connect(self.resume_scraping)

        # Progress bar
        self.progress = QtWidgets.QProgressBar()

        # Navigation button to go to sorting page
        self.go_to_sort_btn = QtWidgets.QPushButton("Go to Sorting Page")
        self.go_to_sort_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.go_to_sort_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.sorting_page))

        # Add widgets to layout with proper spacing
        layout.addStretch()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addSpacing(10)
        layout.addWidget(self.attribute_label)

        for checkbox in self.attribute_checkboxes:
            layout.addWidget(checkbox)

        layout.addSpacing(10)
        layout.addWidget(self.start_btn)
        layout.addSpacing(10)
        layout.addWidget(self.pause_btn)
        layout.addSpacing(10)
        layout.addWidget(self.resume_btn)
        layout.addSpacing(20)
        layout.addWidget(self.progress)
        layout.addSpacing(20)
        layout.addWidget(self.go_to_sort_btn)
        layout.addStretch()

        scraping_widget.setLayout(layout)
        return scraping_widget

    def create_sorting_page(self):
        sorting_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Set the background color to light brown and style the elements
        sorting_widget.setStyleSheet("background-color: #F5DEB3;")  # Light brown background

        # Sorting dropdown
        self.sort_algo_combo = QtWidgets.QComboBox()
        self.sort_algo_combo.addItems(["Bubble Sort", "Quick Sort", "Merge Sort", "Selection Sort", "Heap Sort"])
        self.sort_algo_combo.setStyleSheet("padding: 5px; font-size: 14px;")

        # Sort button
        self.sort_btn = QtWidgets.QPushButton("Sort")
        self.sort_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.sort_btn.clicked.connect(self.sort_data)

        # Search dropdown (ComboBox)
        self.search_field = QtWidgets.QComboBox()
        self.search_field.addItems(["ID", "Name", "Category", "Price", "Stock", "Rating", "Date"])
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")

        # Search button
        self.search_btn = QtWidgets.QPushButton("Search")
        self.search_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.search_btn.clicked.connect(self.search_data)

        # File name input
        self.file_label = QtWidgets.QLabel("File Name:")
        self.file_label.setStyleSheet("font-size: 16px; color: #8B4513;")
        self.file_input = QtWidgets.QLineEdit()
        self.file_input.setStyleSheet("padding: 5px; font-size: 14px;")

        # Open file button
        self.open_file_btn = QtWidgets.QPushButton("Open File")
        self.open_file_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.open_file_btn.clicked.connect(self.open_file)

        # Table for displaying entities
        self.entity_table = QtWidgets.QTableWidget()
        self.entity_table.setColumnCount(7)  # Assume each entity has 7 attributes
        self.entity_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price", "Stock", "Rating", "Date"]
        )
        self.entity_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Back button to go back to scraping page
        self.back_btn = QtWidgets.QPushButton("Back to Scraping Page")
        self.back_btn.setStyleSheet("background-color: #8B4513; color: white; padding: 10px; font-size: 16px;")
        self.back_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.scraping_page))

        # Add widgets to layout with proper spacing
        layout.addStretch()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_input)
        layout.addSpacing(10)
        layout.addWidget(self.open_file_btn)
        layout.addSpacing(20)
        layout.addWidget(self.sort_algo_combo)
        layout.addSpacing(10)
        layout.addWidget(self.sort_btn)
        layout.addSpacing(20)
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_btn)
        layout.addSpacing(20)
        layout.addWidget(self.entity_table)
        layout.addSpacing(20)
        layout.addWidget(self.back_btn)
        layout.addStretch()

        sorting_widget.setLayout(layout)
        return sorting_widget

    # Scraping functions
    def start_scraping(self):
        self.progress.setValue(0)
        self.is_paused = False
        if not self.scrape_thread:
            self.scrape_thread = threading.Thread(target=self.scrape_entities)
            self.scrape_thread.start()

    def scrape_entities(self):
        selected_attributes = [checkbox.text() for checkbox in self.attribute_checkboxes if checkbox.isChecked()]

        for i in range(25000):
            if self.is_paused:
                while self.is_paused:
                    time.sleep(0.1)
            time.sleep(0.01)  # Simulate scraping delay
            entity = {
                "ID": i,
                "Name": f"Entity-{i}",
                "Category": random.choice(["Category A", "Category B", "Category C"]),
                "Price": random.uniform(10, 100),
                "Stock": random.randint(1, 500),
                "Rating": random.uniform(1, 5),
                "Date": f"2024-10-0{random.randint(1,9)}"
            }

            # Filter entity by selected attributes
            filtered_entity = [entity[attr] for attr in selected_attributes]
            self.entities.append(filtered_entity)
            self.update_table(i, filtered_entity)
            self.progress.setValue(int((i + 1) / 25000 * 100))
        self.scrape_thread = None

    def pause_scraping(self):
        self.is_paused = True

    def resume_scraping(self):
        self.is_paused = False

    def update_table(self, row_count, entity):
        self.entity_table.setRowCount(row_count + 1)
        for col in range(len(entity)):
            self.entity_table.setItem(row_count, col, QtWidgets.QTableWidgetItem(str(entity[col])))

    # Sorting and search functions
    def sort_data(self):
        column_index = 0  # Sort based on the first column (ID) for simplicity
        sort_algorithm = self.sort_algo_combo.currentText()
        start_time = time.time()

        if sort_algorithm == "Bubble Sort":
            self.bubble_sort(column_index)
        elif sort_algorithm == "Quick Sort":
            self.entities.sort(key=itemgetter(column_index))
        elif sort_algorithm == "Merge Sort":
            self.entities = self.merge_sort(self.entities, column_index)
        
        self.update_full_table()
        time_taken = (time.time() - start_time) * 1000  # Convert to milliseconds
        print(f"Time taken for {sort_algorithm}: {time_taken:.2f} ms")

    def bubble_sort(self, index):
        n = len(self.entities)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.entities[j][index] > self.entities[j+1][index]:
                    self.entities[j], self.entities[j+1] = self.entities[j+1], self.entities[j]

    def merge_sort(self, data, index):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.merge_sort(data[:mid], index)
        right = self.merge_sort(data[mid:], index)
        return self.merge(left, right, index)

    def merge(self, left, right, index):
        result = []
        while left and right:
            if left[0][index] <= right[0][index]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left if left else right)
        return result

    def search_data(self):
        selected_category = self.search_field.currentText()
        column_map = {
            "ID": 0,
            "Name": 1,
            "Category": 2,
            "Price": 3,
            "Stock": 4,
            "Rating": 5,
            "Date": 6
        }
        column_index = column_map[selected_category]
        search_value = QtWidgets.QInputDialog.getText(self, "Search", f"Enter {selected_category} value:")[0]

        search_results = [entity for entity in self.entities if str(entity[column_index]) == search_value]
        self.entity_table.setRowCount(0)  # Clear current table
        for i, entity in enumerate(search_results):
            self.entity_table.insertRow(i)
            for j, value in enumerate(entity):
                self.entity_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def open_file(self):
        filename = self.file_input.text()
        if filename:
            try:
                with open(filename, 'r') as file:
                    self.entities = [line.strip().split(',') for line in file]
                    self.update_full_table()
            except FileNotFoundError:
                QtWidgets.QMessageBox.warning(self, "File Not Found", f"The file {filename} was not found.")

    def update_full_table(self):
        self.entity_table.setRowCount(0)  # Clear current table
        for i, entity in enumerate(self.entities):
            self.entity_table.insertRow(i)
            for j, value in enumerate(entity):
                self.entity_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scraper_app = ScraperApp()
    scraper_app.show()
    sys.exit(app.exec_())
