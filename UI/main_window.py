from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QStackedWidget, QLabel,
    QMessageBox, QHeaderView, QFrame,
    QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from Services.bank_service import BankService

from UI.pages.home_page import HomePage
from UI.pages.customer_page import CustomerPage
from UI.pages.deposit_page import DepositPage
from UI.pages.withdraw_page import WithdrawPage
from UI.pages.transfer_page import TransferPage
from UI.pages.saving_page import SavingPage
from UI.pages.interest_page import InterestPage
from UI.pages.close_saving_page import CloseSavingPage
from UI.pages.history_page import HistoryPage
from UI.pages.find_page import FindPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bank = BankService()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("NGAN HANG DBC - He Thong Quan Ly Tai Khoan")
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        self.setStyleSheet(self._get_global_style())

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._create_header())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        menu_labels = [
            "Trang chủ", "Tạo khách hàng + Tài khoản", "Nạp tiền",
            "Rút tiền", "Chuyển khoản", "Sổ tiết kiệm",
            "Rút lãi tiết kiệm", "Tất toán sổ tiết kiệm",
            "Lịch sử giao dịch", "Tra cứu"
        ]
        page_wrappers = ["Tổng quan", "Tạo khách hàng & Tài khoản",
            "Nạp tiền vào tài khoản", "Rút tiền từ tài khoản",
            "Chuyển khoản", "Tạo sổ tiết kiệm", "Rút lãi tiết kiệm",
            "Tất toán sổ tiết kiệm", "Lịch sử giao dịch", "Tra cứu thông tin"]

        pages = [
            HomePage(self), CustomerPage(self), DepositPage(self),
            WithdrawPage(self), TransferPage(self), SavingPage(self),
            InterestPage(self), CloseSavingPage(self), HistoryPage(self),
            FindPage(self)
        ]

        self.menu = QListWidget()
        self.menu.setObjectName("menuNav")
        self.menu.setFixedWidth(300)
        self.menu.setFocusPolicy(Qt.NoFocus)
        for text in menu_labels:
            self.menu.addItem(text)
        body_layout.addWidget(self.menu)

        self.pages = QStackedWidget()
        self.pages.setObjectName("contentArea")
        self.page_map = []
        for i, page in enumerate(pages):
            wrapped = self._wrap_page(page_wrappers[i], page)
            self.pages.addWidget(wrapped)
            self.page_map.append(wrapped)

        body_layout.addWidget(self.pages, 1)
        main_layout.addWidget(body, 1)

        self.menu.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.menu.setCurrentRow(0)

    def _create_header(self):
        header = QFrame()
        header.setObjectName("appHeader")
        header.setFixedHeight(55)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 5, 15, 5)

        title = QLabel("NGÂN HÀNG ABC")
        title.setObjectName("headerTitle")
        layout.addWidget(title)

        subtitle = QLabel("Hệ Thống Quản Lý Tài Khoản")
        subtitle.setObjectName("headerSubtitle")
        layout.addWidget(subtitle)

        layout.addStretch()
        return header

    def _get_global_style(self):
        return """
        QMainWindow { background-color: #f0f2f5; }
        QWidget { font-family: Segoe UI, Arial; font-size: 16px; }
        #appHeader {
            background-color: #1a237e;
            color: white;
            border-bottom: 3px solid #ff6f00;
        }
        #headerTitle { color: white; font-weight: bold; }
        #headerSubtitle { color: #b0bec5; padding-top: 6px; }
        #menuNav {
            background-color: #263238;
            color: #eceff1;
            border: none;
            font-size: 16px;
            padding: 5px;
            outline: none;
        }
        #menuNav::item {
            padding: 16px 20px;
            border-bottom: 1px solid #37474f;
        }
        #menuNav::item:selected {
            background-color: #ff6f00;
            color: white;
        }
        #menuNav::item:hover:!selected {
            background-color: #37474f;
        }
        #contentArea {
            background-color: #ffffff;
            border: none;
            padding: 20px;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            margin-top: 12px;
            padding: 15px 10px 10px 10px;
            background-color: #fafafa;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
            color: #1a237e;
        }
        QLineEdit {
            border: 1px solid #bdbdbd;
            border-radius: 4px;
            padding: 12px 14px;
            background-color: white;
            min-width: 250px;
            font-size: 16px;
        }
        QLineEdit:focus { border-color: #ff6f00; }
        QPushButton {
            border-radius: 4px;
            padding: 12px 28px;
            font-weight: bold;
            min-width: 120px;
            font-size: 15px;
        }
        QPushButton#btnPrimary {
            background-color: #1a237e;
            color: white;
            border: none;
        }
        QPushButton#btnPrimary:hover { background-color: #283593; }
        QPushButton#btnDanger {
            background-color: #c62828;
            color: white;
            border: none;
        }
        QPushButton#btnDanger:hover { background-color: #d32f2f; }
        QPushButton#btnSuccess {
            background-color: #2e7d32;
            color: white;
            border: none;
        }
        QPushButton#btnSuccess:hover { background-color: #388e3c; }
        QPushButton#btnNormal {
            background-color: #f5f5f5;
            border: 1px solid #bdbdbd;
        }
        QPushButton#btnNormal:hover { background-color: #eeeeee; }
        QTableWidget {
            border: 1px solid #e0e0e0;
            gridline-color: #e0e0e0;
            selection-background-color: #e3f2fd;
            font-size: 15px;
        }
        QTableWidget::item { padding: 10px; }
        QHeaderView::section {
            background-color: #37474f;
            color: white;
            font-weight: bold;
            padding: 12px;
            border: none;
            font-size: 15px;
        }
        QComboBox {
            border: 1px solid #bdbdbd;
            border-radius: 4px;
            padding: 12px 14px;
            background-color: white;
            min-width: 250px;
            font-size: 16px;
        }
        """

    def _show_error(self, message):
        QMessageBox.warning(self, "Lỗi", str(message))

    def _show_success(self, message):
        QMessageBox.information(self, "Thành công", message)

    def _wrap_page(self, title, widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 19px; font-weight: bold; color: #1a237e; padding-bottom: 5px;")
        layout.addWidget(title_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #ff6f00; max-height: 2px;")
        layout.addWidget(sep)
        layout.addSpacing(10)
        layout.addWidget(widget, 1)
        return container
