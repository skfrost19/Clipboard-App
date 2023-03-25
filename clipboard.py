from PyQt5 import QtWidgets
import sys
import pickle
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QMenu,
    QAction,
    QSystemTrayIcon,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QAbstractItemView,
    QDesktopWidget,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSharedMemory, QSystemSemaphore


class ClipboardApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # style the application and set the background as transparent
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: rgba(0, 0, 0, 0);
                border: none;
            }
            QMainWindow::title {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                font-size: 50px;
            }
            QTableWidget {
                background-color: #3d3d3d;
                color: #f0f0f0;
                border: 1px solid #2d2d2d;
            }
            QTableWidget::item {
                border: 1px solid #2d2d2d;
            }
            QTableWidget::item:selected {
                background-color: #3d3d3d;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #3d3d3d;
                border: 1px solid #2d2d2d;
                height: 25px;
                font-size: 14px;
                font-family: "Segoe UI";
                font-style: normal;
            }
            QPushButton:hover {
                background-color: #5d5d5d;

            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }

        """
        )

        # remove minimise icon from the window
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # create the main window
        self.setWindowTitle("Clipboard  Manager")
        # change font size of Title Bar
        self.setWindowIcon(QIcon("icon.png"))

        # set at right upper corner
        desktop = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop.width() - 600, 0, 600, 400)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 400)

        # create the table to display copied elements
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Copied Elements", "Options"])
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setCentralWidget(self.table)
        self.add_clear_button()
        # connect to the system clipboard and add a listener for clipboard changes
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        # create the system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))

        # create the tray icon menu
        self.tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_normal)
        self.tray_menu.addAction(show_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

        # load the clipboard history
        self.load_data()
        # show the system tray icon
        self.tray_icon.show()
        self.hide()  # hide the main window on startup

        # show a message on the system tray icon
        self.tray_icon.showMessage(
            "Clipboard App",
            "The app is running in the background",
            icon=QSystemTrayIcon.Information,
            msecs=2000,
        )

        # override closeEvent to minimize to system tray and if the user closes the window from the system tray, exit the application
        self.closeEvent = self.on_close
        self.set_tooltip()

    def set_tooltip(self):
        for row in range(self.table.rowCount()):  # iterate through the rows
            item = self.table.item(row, 0)  # get the item in the first column
            item.setToolTip(
                item.text()[:100]
            )  # set the tooltip to the first 100 characters of the text

    def add_clear_button(self):
        # add a button to clear the clipboard at the bottom of the window
        self.clear_button = QPushButton("Clear Clipboard", self)
        self.clear_button.setIcon(QIcon("clear.png"))
        self.clear_button.clicked.connect(self.clear_clipboard)
        # flex the button to the bottom of the window and center it
        # resize according to the window size
        self.clear_button.resize(600, 30)
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3d3d3d;  
                color: red;
                border: 1px solid #2d2d2d;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
        """
        )
        self.clear_button.move(0, 370)

    def clear_clipboard(self):
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        # clear the clipboard history
        self.clipboard_data.clear()
        # clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

    def show_normal(self):
        self.show()
        self.activateWindow()

    def load_data(self):
        # load the clipboard history
        try:
            with open("clipboard_history.pkl", "rb") as f:
                self.clipboard_data = pickle.load(f)
            f.close()
        except:
            print("No clipboard history found")
            self.clipboard_data = []

        # add the clipboard history to the table
        for text in self.clipboard_data[::-1]:
            self.add_row(text)

    def on_close(self, event):
        if self.isVisible():
            self.hide()
            event.ignore()
        else:
            self.save_data()
            event.accept()

    def save_data(self):
        # save the clipboard history
        with open("clipboard_history.pkl", "wb") as f:
            pickle.dump(self.clipboard_data, f)
        f.close()

    def on_clipboard_change(self):
        # get the current clipboard text
        text = self.clipboard.text()

        # check if the text is already in the table
        if text in self.clipboard_data:
            return
        if text != "":
            self.add_row(text)
            self.clipboard_data.insert(0, text)
            self.set_tooltip()
            self.save_data()
        else:
            return

    def add_row(self, text):
        if text != "":
            self.table.insertRow(0)
            # set as not editable
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # set the text
            self.table.setItem(0, 0, QTableWidgetItem(text))

            # add the options to the table
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete_row)
            delete_button.setFixedHeight(20)
            # font color to red
            delete_button.setStyleSheet("color: red")
            # change y padding to 0
            delete_button.setContentsMargins(0, 0, 0, 0)
            copy_button = QPushButton("Copy")
            copy_button.clicked.connect(self.copy_row)
            copy_button.setFixedHeight(20)
            # font color to green
            copy_button.setStyleSheet("color: green")
            # change y padding to 0
            copy_button.setContentsMargins(0, 0, 0, 0)
            option_widget = QWidget()
            layout = QHBoxLayout(option_widget)
            layout.addWidget(delete_button)
            layout.addWidget(copy_button)
            layout.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(0, 1, option_widget)
        else:
            pass

    def copy_row(self):
        button = self.sender()
        if button:
            # get the row of the button's parent widget
            row = self.table.indexAt(button.parent().pos()).row()
            row_text = self.table.item(row, 0).text()
            self.clipboard.setText(row_text)
            # show a message
            QtWidgets.QMessageBox.information(self, "Copied", f"{row_text[:200]}")

    def delete_row(self):
        button = self.sender()
        if button:
            # get the row of the button's parent widget
            row = self.table.indexAt(button.parent().pos()).row()
            self.table.removeRow(row)
            self.clipboard_data.pop(row)
            self.save_data()


def launch():
    app = QtWidgets.QApplication(
        sys.argv
    )  # create app instance at top, to able to show QMessageBox is required
    window_id = "pingidapplication"
    shared_mem_id = "pingidsharedmem"
    semaphore = QSystemSemaphore(window_id, 1)
    semaphore.acquire()  # Raise the semaphore, barring other instances to work with shared memory

    if sys.platform != "win32":
        # in linux / unix shared memory is not freed when the application terminates abnormally,
        # so you need to get rid of the garbage
        nix_fix_shared_mem = QSharedMemory(shared_mem_id)
        if nix_fix_shared_mem.attach():
            nix_fix_shared_mem.detach()

    shared_memory = QSharedMemory(shared_mem_id)

    if (
        shared_memory.attach()
    ):  # attach a copy of the shared memory, if successful, the application is already running
        is_running = True
    else:
        shared_memory.create(1)  # allocate a shared memory block of 1 byte
        is_running = False

    semaphore.release()

    if is_running:  # if the application is already running, show the warning message
        QtWidgets.QMessageBox.warning(
            None,
            "Application already running",
            "One instance of the application is already running.",
        )
        return

    # normal process of creating & launching MainWindow
    window = ClipboardApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch()