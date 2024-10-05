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

        # Attributes selection (CheckBoxes) and Class input
        self.attribute_label = QtWidgets.QLabel("Select 5 Attributes to Scrape and their Classes:")
        self.attribute_label.setStyleSheet("font-size: 16px; color: #8B4513;")

        self.attribute_fields = []
        for i, attr in enumerate(["Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4", "Attribute 5"]):
            attr_layout = QtWidgets.QHBoxLayout()

            checkbox = QtWidgets.QCheckBox(attr)
            checkbox.setChecked(True)  # Automatically select the attribute since we're limiting it to 5
            checkbox.setEnabled(False)  # Disable the checkbox to enforce exactly 5 attributes
            attr_layout.addWidget(checkbox)

            class_input = QtWidgets.QLineEdit()
            class_input.setPlaceholderText(f"Enter CSS class or selector for {attr.lower()}")
            class_input.setStyleSheet("padding: 5px; font-size: 14px;")
            attr_layout.addWidget(class_input)

            self.attribute_fields.append((checkbox, class_input))  # Store the checkbox and the input field

            layout.addLayout(attr_layout)

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

        for checkbox, class_input in self.attribute_fields:
            layout.addWidget(checkbox)
            layout.addWidget(class_input)

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

        # Add widgets to layout
        layout.addStretch()
        layout.addWidget(self.sort_algo_combo)
        layout.addSpacing(10)
        layout.addWidget(self.sort_btn)
        layout.addSpacing(10)
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_btn)
        layout.addSpacing(10)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_input)
        layout.addWidget(self.open_file_btn)
        layout.addSpacing(20)
        layout.addWidget(self.entity_table)
        layout.addStretch()

        sorting_widget.setLayout(layout)
        return sorting_widget

    def start_scraping(self):
        self.is_paused = False
        if self.scrape_thread is None:
            self.scrape_thread = threading.Thread(target=self.scrape_entities)
            self.scrape_thread.start()

    def pause_scraping(self):
        self.is_paused = True

    def resume_scraping(self):
        self.is_paused = False

    def scrape_entities(self):
        url = self.url_input.text()
        selected_attributes = [(field[1].text(), field[0].text()) for field in self.attribute_fields if field[0].isChecked()]

        for i in range(25000):  # Simulated scraping
            if self.is_paused:
                while self.is_paused:
                    time.sleep(0.1)
            time.sleep(0.01)  # Simulate scraping delay

            entity = {}  # Simulate an entity
            for (css_class, attr_name) in selected_attributes:
                # Simulate the fetching of an attribute using the CSS class (in a real scraper, you'd use something like BeautifulSoup)
                entity[attr_name] = f"ScrapedData-{random.randint(100, 999)}"

            filtered_entity = [entity[attr_name] for _, attr_name in selected_attributes]
            self.entities.append(filtered_entity)
            self.update_table(i, filtered_entity)
            self.progress.setValue(int((i + 1) / 25000 * 100))
        self.scrape_thread = None

    def update_table(self, row, entity):
        self.entity_table.insertRow(row)
        for col, value in enumerate(entity):
            self.entity_table.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def sort_data(self):
        selected_algorithm = self.sort_algo_combo.currentText()
        print(f"Sorting with {selected_algorithm}")

    def search_data(self):
        selected_field = self.search_field.currentText()
        print(f"Searching by {selected_field}")

    def open_file(self):
        file_name = self.file_input.text()
        print(f"Opening file: {file_name}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())
