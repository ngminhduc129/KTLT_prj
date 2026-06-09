from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QLabel,
    QMessageBox, QHeaderView, QFrame,
    QAbstractItemView
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from Services.bank_service import BankService

from UI.pages.home_page import HomePage
from UI.pages.customer_page import CustomerPage
from UI.pages.account_page import AccountPage
from UI.pages.deposit_page import DepositPage
from UI.pages.withdraw_page import WithdrawPage
from UI.pages.transfer_page import TransferPage
from UI.pages.saving_page import SavingPage
from UI.pages.interest_page import InterestPage
from UI.pages.close_saving_page import CloseSavingPage
from UI.pages.history_page import HistoryPage
from UI.pages.find_account_page import FindPageAccount
from UI.pages.find_user_page import FindPageUser
from UI.pages.update_information_page import UpdateInformationPage
from UI.pages.change_pin_password_page import ChangeSecurityPage
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bank = BankService()
        self.bank.load_all_data()
        self._setup_ui()

    def closeEvent(self, event):
        self.bank.save_all_data()
        event.accept()

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


        page_wrappers = ["Tổng quan", "Tạo khách hàng & Tài khoản",
            "Thêm tài khoản cho khách hàng",
            "Nạp tiền vào tài khoản", "Rút tiền từ tài khoản",
            "Chuyển khoản", "Tạo sổ tiết kiệm", "Rút lãi tiết kiệm",
            "Tất toán sổ tiết kiệm", "Lịch sử giao dịch", "Tra cứu thông tin khách hàng", "Tra cứu tài khoản ngân hàng" 
            "Cập nhật thông tin khách hàng", "Đổi mật khẩu và mã PIN"]

        pages = [
            HomePage(self),
            CustomerPage(self),
            AccountPage(self),
            DepositPage(self),
            WithdrawPage(self),
            TransferPage(self),
            SavingPage(self),
            InterestPage(self),
            CloseSavingPage(self),
            HistoryPage(self),
            FindPageUser(self),
            FindPageAccount(self),
            UpdateInformationPage(self),
            ChangeSecurityPage(self)
        ]

        self.menu = QTreeWidget()
        self.menu.setObjectName("menuNav")
        self.menu.setFixedWidth(300)
        self.menu.setFocusPolicy(Qt.NoFocus)
        self.menu.setHeaderHidden(True)

        # Mapping trang (leaf) -> index QStackedWidget (không dựa row index)
        self._leaf_to_page_index = {
            "Trang chủ": 0,
            "Tạo khách hàng + Tài khoản": 1,
            "Thêm tài khoản": 2,
            "Nạp tiền": 3,
            "Rút tiền": 4,
            "Chuyển khoản": 5,
            "Sổ tiết kiệm": 6,
            "Rút lãi tiết kiệm": 7,
            "Tất toán sổ tiết kiệm": 8,
            "Lịch sử giao dịch": 9,
            "Tra cứu thông tin khách hàng": 10,
            "Tra cứu tài khoản ngân hàng": 11,
            "Cập nhật thông tin": 12,
            "Đổi mật khẩu và mã PIN": 13,
        }

        # Node cha/con theo nhóm nghiệp vụ
        root_home = QTreeWidgetItem(self.menu, ["Trang chủ"])

        root_customer = QTreeWidgetItem(self.menu, ["Khách hàng"])
        QTreeWidgetItem(root_customer, ["Tạo khách hàng + Tài khoản"])
        QTreeWidgetItem(root_customer, ["Tra cứu thông tin khách hàng"])
        QTreeWidgetItem(root_customer, ["Cập nhật thông tin"])

        root_account = QTreeWidgetItem(self.menu, ["Tài khoản"])

        QTreeWidgetItem(root_account, ["Thêm tài khoản"])
        QTreeWidgetItem(root_account, ["Đổi mật khẩu và mã PIN"])
        QTreeWidgetItem(root_account, ["Tra cứu tài khoản ngân hàng"])

        root_transaction = QTreeWidgetItem(self.menu, ["Giao dịch"])
        QTreeWidgetItem(root_transaction, ["Nạp tiền"])
        QTreeWidgetItem(root_transaction, ["Rút tiền"])
        QTreeWidgetItem(root_transaction, ["Chuyển khoản"])
        QTreeWidgetItem(root_transaction, ["Lịch sử giao dịch"])

        root_saving = QTreeWidgetItem(self.menu, ["Sổ tiết kiệm"])
        QTreeWidgetItem(root_saving, ["Sổ tiết kiệm"])
        QTreeWidgetItem(root_saving, ["Rút lãi tiết kiệm"])
        QTreeWidgetItem(root_saving, ["Tất toán sổ tiết kiệm"])

        body_layout.addWidget(self.menu)

        pages_config = [
                    ("Tổng quan", HomePage(self)),
                    ("Tạo khách hàng & Tài khoản", CustomerPage(self)),
                    ("Thêm tài khoản cho khách hàng", AccountPage(self)),
                    ("Nạp tiền vào tài khoản", DepositPage(self)),
                    ("Rút tiền từ tài khoản", WithdrawPage(self)),
                    ("Chuyển khoản", TransferPage(self)),
                    ("Tạo sổ tiết kiệm", SavingPage(self)),
                    ("Rút lãi tiết kiệm", InterestPage(self)),
                    ("Tất toán sổ tiết kiệm", CloseSavingPage(self)),
                    ("Lịch sử giao dịch", HistoryPage(self)),
                    ("Tra cứu thông tin khách hàng", FindPageUser(self)),
                    ("Tra cứu tài khoản ngân hàng", FindPageAccount(self)),
                    ("Cập nhật thông tin khách hàng", UpdateInformationPage(self)),
                    ("Đổi mật khẩu và mã PIN", ChangeSecurityPage(self))
        ]
        self.pages = QStackedWidget()
        self.pages.setObjectName("contentArea")
        self.page_map = []


        for title, page_obj in pages_config:
            wrapped = self._wrap_page(title, page_obj)
            self.pages.addWidget(wrapped)
            self.page_map.append(wrapped)

        body_layout.addWidget(self.pages, 1)
        main_layout.addWidget(body, 1)

        # Kết nối menu QTreeWidget (chỉ map các leaf item)
        def on_item_clicked(item: QTreeWidgetItem, column: int):
            text = item.text(0).strip()
            if text in self._leaf_to_page_index:
                self.pages.setCurrentIndex(self._leaf_to_page_index[text])

        self.menu.itemClicked.connect(on_item_clicked)

        # Mặc định hiển thị trang 0
        self.pages.setCurrentIndex(0)



    def _create_header(self):
        header = QFrame()
        header.setObjectName("appHeader")
        header.setFixedHeight(55)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 5, 15, 5)

        title = QLabel("NGÂN HÀNG DBC")
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
            font-family: "Segoe UI", "Arial", "Microsoft Sans Serif";
        }
        QComboBox:hover {
            border: 1px solid #1976d2;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            selection-background-color: #e3f2fd;
            selection-color: black;
            font-family: "Segoe UI", "Arial", "Microsoft Sans Serif";
            font-size: 16px;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #e3f2fd;
            color: black;
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
