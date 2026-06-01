from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HomePage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        welcome = QLabel("CHÀO MỪNG ĐẾN VỚI NGÂN HÀNG DBC")
        welcome.setFont(QFont("Arial", 22, QFont.Bold))
        welcome.setStyleSheet("color: #1a237e;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)

        desc = QLabel("Vui lòng chọn chức năng từ menu bên trái.")
        desc.setFont(QFont("Arial", 14))
        desc.setStyleSheet("color: #757575;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        layout.addSpacing(20)

        info_box = QGroupBox("Hệ thống bao gồm")
        info_layout = QVBoxLayout(info_box)
        features = [
            "Quản lý khách hàng (User)",
            "Quản lý tài khoản ngân hàng (Account)",
            "Giao dịch: Nạp, Rút, Chuyển khoản",
            "Sổ tiết kiệm (Saving Deposit)",
            "Lịch sử giao dịch",
            "Tra cứu tài khoản",
            "Cập nhật thông tin",
            "Đổi mật khẩu và mã PIN"
        ]
        for f in features:
            lbl = QLabel(f"  {f}")
            lbl.setStyleSheet("color: #424242; padding: 3px 0;")
            info_layout.addWidget(lbl)
        layout.addWidget(info_box, 0, Qt.AlignCenter)
