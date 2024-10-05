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

        # Create login page
        self.login_page = self.create_login_page()
        self.central_widget.addWidget(self.login_page)

        # Create scraping page
        self.scraping_page = self.create_scraping_page()
        self.central_widget.addWidget(self.scraping_page)

        # Create sorting page
        self.sorting_page = self.create_sorting_page()
        self.central_widget.addWidget(self.sorting_page)

        self.central_widget.setCurrentWidget(self.login_page)  # Show login page first

        self.is_paused = False
        self.scrape_thread = None

    def create_login_page(self):
        login_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Username input
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_input = QtWidgets.QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_btn = QtWidgets.QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        login_widget.setLayout(layout)
        return login_widget

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simple login validation (for demonstration purposes)
        if username == "admin" and password == "1234":
            self.central_widget.setCurrentWidget(self.scraping_page)  # Switch to scraping page
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Incorrect username or password!")

    def create_scraping_page(self):
        scraping_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Input field for URL
        self.url_label = QtWidgets.QLabel("URL:")
        self.url_input = QtWidgets.QLineEdit()

        # Start, pause, resume buttons
        self.start_btn = QtWidgets.QPushButton("Start Scraping")
        self.start_btn.clicked.connect(self.start_scraping)

        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_scraping)

        self.resume_btn = QtWidgets.QPushButton("Resume")
        self.resume_btn.clicked.connect(self.resume_scraping)

        # Progress bar
        self.progress = QtWidgets.QProgressBar()

        # Navigation button to go to sorting page
        self.go_to_sort_btn = QtWidgets.QPushButton("Go to Sorting Page")
        self.go_to_sort_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.sorting_page))

        # Add widgets to layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.resume_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.go_to_sort_btn)

        scraping_widget.setLayout(layout)
        return scraping_widget

    def create_sorting_page(self):
        sorting_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Sorting dropdown
        self.sort_algo_combo = QtWidgets.QComboBox()
        self.sort_algo_combo.addItems(["Bubble Sort", "Quick Sort", "Merge Sort", "Selection Sort", "Heap Sort"])

        # Sort button
        self.sort_btn = QtWidgets.QPushButton("Sort")
        self.sort_btn.clicked.connect(self.sort_data)

        # Search dropdown (ComboBox)
        self.search_field = QtWidgets.QComboBox()
        self.search_field.addItems(["ID", "Name", "Category", "Price", "Stock", "Rating", "Date"])

        # Search button
        self.search_btn = QtWidgets.QPushButton("Search")
        self.search_btn.clicked.connect(self.search_data)

        # Table for displaying entities
        self.entity_table = QtWidgets.QTableWidget()
        self.entity_table.setColumnCount(7)  # Assume each entity has 7 attributes
        self.entity_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price", "Stock", "Rating", "Date"]
        )
        self.entity_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Back button to go back to scraping page
        self.back_btn = QtWidgets.QPushButton("Back to Scraping Page")
        self.back_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.scraping_page))

        # Add widgets to layout
        layout.addWidget(self.sort_algo_combo)
        layout.addWidget(self.sort_btn)
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.entity_table)
        layout.addWidget(self.back_btn)

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
        for i in range(25000):
            if self.is_paused:
                while self.is_paused:
                    time.sleep(0.1)
            time.sleep(0.01)  # Simulate scraping delay
            entity = [
                i,
                f"Entity-{i}",
                random.choice(["Category A", "Category B", "Category C"]),
                random.uniform(10, 100),
                random.randint(1, 500),
                random.uniform(1, 5),
                f"2024-10-0{random.randint(1,9)}"
            ]
            self.entities.append(entity)
            self.update_table(i)
            self.progress.setValue(int((i + 1) / 25000 * 100))
        self.scrape_thread = None

    def pause_scraping(self):
        self.is_paused = True

    def resume_scraping(self):
        self.is_paused = False

    def update_table(self, row_count):
        self.entity_table.setRowCount(row_count + 1)
        entity = self.entities[row_count]
        for col in range(7):
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
        search_column = column_map[selected_category]
        filtered_entities = sorted(self.entities, key=itemgetter(search_column))
        self.entities = filtered_entities
        self.update_full_table()

    def update_full_table(self):
        self.entity_table.setRowCount(0)
        for i, entity in enumerate(self.entities):
            self.entity_table.setRowCount(i + 1)
            for col in range(7):
                self.entity_table.setItem(i, col, QtWidgets.QTableWidgetItem(str(entity[col])))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
