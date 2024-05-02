import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QTableWidget, QTableWidgetItem
import pandas as pd
from pathlib import Path
from PyQt5.QtGui import QPixmap, QPainter

# Get Segregared CSV records
def parse_csv_records():
    master_csv_path = 'master_file.csv'  # Replace with your master CSV file path
    master_df = pd.read_csv(master_csv_path)

    # Ensure the SensorID column exists
    if 'SensorID' not in master_df.columns:
        raise ValueError("The master CSV does not have a 'SensorID' column.")

    # Create a directory for the output CSV files if it doesn't exist
    output_dir = Path('sensor_records')
    output_dir.mkdir(exist_ok=True)

    # Group the dataframe by SensorID and write separate CSVs
    for SensorID, group_df in master_df.groupby('SensorID'):
        output_file_path = output_dir / f'sensorID_{SensorID}.csv'
        group_df.to_csv(output_file_path, index=False)

    print("CSV files have been created for each SensorID.")

# Get available Sensor IDs
def detect_disctint_sensors():
    master_csv = 'master_file.csv'
    df = pd.read_csv(master_csv)
    search_field = 'SensorID'
    distinct_values = df[search_field].unique()
    print("Type of data",type(distinct_values))
    print("IDs:", list(distinct_values))
    sensorID_list = list(map(str,distinct_values))
    return sensorID_list

# Additional window for displaying records in a table
class RecordsWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sensor Data Table')
        #setGeometry(xpos, ypos, width, height)
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setRowCount(len(self.data.index))
        table.setColumnCount(len(self.data.columns))
        table.setHorizontalHeaderLabels(self.data.columns)

        for i in range(len(self.data.index)):
            for j in range(len(self.data.columns)):
                table.setItem(i, j, QTableWidgetItem(str(self.data.iloc[i, j])))

        # Enable sorting
        table.setSortingEnabled(True)

        layout.addWidget(table)
        self.setLayout(layout)
        self.show()

# Placeholder window
class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Graphical View')
        #self.setGeometry(200, 200, 200, 200)
        self.show()

# Main application window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sensor Data GUI'
        self.left = 400
        self.top = 200
        self.width = 500
        self.height = 400
        # self.sensor_ids = ['Sensor1', 'Sensor2', 'Sensor3']  # Replace with actual sensor IDs
        self.sensor_ids = sensor_list
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Main layout
        layout = QVBoxLayout()
        # label = QLabel('Sensor ID', self)

        # Dropdown for sensorID
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(self.sensor_ids)
        #layout.addWidget(label)
        layout.addWidget(self.comboBox)
        self.comboBox.setStyleSheet("""
                                    QComboBox {
                                        /*background-color: lightblue;*/
                                        border: 1px solid gray;
                                        position: absolute;
                                        padding: 1px 18px 1px 3px;
                                        /*min-width: 160px;*/
                                        width: 50px;
                                        height: 18px;
                                        padding: 12px 16px;
                                        font-size: 16px;
                                        text-align: center;
                                    }
                                """)

        # Button to show records
        self.btn_show_records = QPushButton('Sensor Data', self)
        self.btn_show_records.clicked.connect(self.show_records)
        # self.btn_show_records.resize(180, 40)
        self.btn_show_records.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAF50; /* Green */
                                                /*width: 100px;
                                                height: 50px;*/
                                                /*border: none; */
                                                border :2px solid white;
                                                color: white;
                                                padding: 15px 32px;
                                                text-align: center;
                                                text-decoration: none;
                                                /*display: inline-block;*/
                                                font-size: 16px;
                                                margin: 4px 2px;
                                                /*cursor: pointer;*/
                                                border-radius: 8px;
                                            }
                                            QPushButton:hover {
                                                background-color: #45a049;
                                            }
                                        """)
        layout.addWidget(self.btn_show_records)

        # Button to launch placeholder window
        self.btn_placeholder = QPushButton('Graphical View', self)
        self.btn_placeholder.clicked.connect(self.show_graphs)
        self.btn_placeholder.setStyleSheet("""
                                        QPushButton {
                                            background-color: #008CBA; /* Blue */
                                            border :2px solid white;
                                            color: white;
                                            padding: 15px 32px;
                                            text-align: center;
                                            text-decoration: none;
                                            /*display: inline-block;*/
                                            font-size: 16px;
                                            margin: 4px 2px;
                                            /*cursor: pointer;*/
                                            border-radius: 8px;
                                        }
                                        QPushButton:hover {
                                            background-color: #007bb5;
                                        }
                                    """)
        layout.addWidget(self.btn_placeholder)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()

        # Add a background image to the  GUI
        self.background = QPixmap('background.png') 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def show_records(self):
        # Read data from CSV
        selected_id = self.comboBox.currentText()
        file_name = "sensorID_"+ selected_id + ".csv"
        data = pd.read_csv(file_name)
        # Open the records window
        self.records_window = RecordsWindow(data)

    def show_graphs(self):
        selected_id = self.comboBox.currentText()
        file_name = "sensorID_"+ selected_id + ".csv"
        self.placeholder_window = GraphWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parse_csv_records()
    sensor_list = detect_disctint_sensors()
    ex = App()
    sys.exit(app.exec_())
