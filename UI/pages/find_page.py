from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTextEdit, QGroupBox
)


class FindPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        tab = QWidget()
        tab_layout = QHBoxLayout(tab)

        user_box = QGroupBox("Tra cứu khách hàng")
        user_layout = QVBoxLayout(user_box)
        self.mw.find_user_id = QLineEdit()
        self.mw.find_user_id.setPlaceholderText("Nhập User ID")
        btn_find_user = QPushButton("Tìm khách hàng")
        btn_find_user.setObjectName("btnPrimary")
        btn_find_user.clicked.connect(self._on_find_user)
        user_layout.addWidget(QLabel("User ID:"))
        user_layout.addWidget(self.mw.find_user_id)
        user_layout.addWidget(btn_find_user)
        self.mw.find_user_result = QTextEdit()
        self.mw.find_user_result.setReadOnly(True)
        self.mw.find_user_result.setMaximumHeight(200)
        user_layout.addWidget(self.mw.find_user_result)

        acc_box = QGroupBox("Tra cứu tài khoản")
        acc_layout = QVBoxLayout(acc_box)
        self.mw.find_account_id = QLineEdit()
        self.mw.find_account_id.setPlaceholderText("Nhập số tài khoản")
        btn_find_acc = QPushButton("Tìm tài khoản")
        btn_find_acc.setObjectName("btnPrimary")
        btn_find_acc.clicked.connect(self._on_find_account)
        acc_layout.addWidget(QLabel("Số tài khoản:"))
        acc_layout.addWidget(self.mw.find_account_id)
        acc_layout.addWidget(btn_find_acc)
        self.mw.find_account_result = QTextEdit()
        self.mw.find_account_result.setReadOnly(True)
        self.mw.find_account_result.setMaximumHeight(200)
        acc_layout.addWidget(self.mw.find_account_result)

        tab_layout.addWidget(user_box)
        tab_layout.addWidget(acc_box)
        layout.addWidget(tab)
        layout.addStretch()

    def _on_find_user(self):
        mw = self.mw
        user_id = mw.find_user_id.text().strip()
        if not user_id:
            mw._show_error("Vui lòng nhập User ID!")
            return
        try:
            user = mw.bank.user_service.find_user_by_id(user_id)
            info = (
                f"User ID: {user.user_id}\n"
                f"Họ tên: {user.full_name}\n"
                f"Số điện thoại: {user.phone}\n"
                f"Email: {user.email}\n"
                f"Giới tính: {user.sex}\n"
                f"Địa chỉ: {user.address}\n"
                f"Nghề nghiệp: {user.job}\n"
                f"Ngày sinh: {user.dob}"
            )
            mw.find_user_result.setText(info)
        except ValueError as e:
            mw.find_user_result.setText(f"Không tìm thấy: {str(e)}")

    def _on_find_account(self):
        mw = self.mw
        account_id = mw.find_account_id.text().strip()
        if not account_id:
            mw._show_error("Vui lòng nhập số tài khoản!")
            return
        try:
            acc = mw.bank.account_service.find_account(account_id)
            info = (
                f"Số TK: {acc.account_id}\n"
                f"Chủ TK: {acc.full_name}\n"
                f"Số dư: {acc.balance:,.0f} VND\n"
                f"Trạng thái: {acc.status}\n"
                f"Chi nhánh: {acc.create_at}\n"
                f"Ngày mở: {acc.time_created}"
            )
            mw.find_account_result.setText(info)
        except ValueError as e:
            mw.find_account_result.setText(f"Không tìm thấy: {str(e)}")
