from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel
)


class AccountPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        row1 = QHBoxLayout()
        self.mw.acc_user_id = QLineEdit()
        self.mw.acc_user_id.setPlaceholderText("Nhập User ID")
        btn_find = QPushButton("Tra cứu")
        btn_find.setObjectName("btnNormal")
        btn_find.clicked.connect(self._on_find_user)
        row1.addWidget(self.mw.acc_user_id)
        row1.addWidget(btn_find)

        f_layout.addRow("User ID:", row1)

        self.mw.acc_user_name = QLabel("")
        self.mw.acc_user_name.setStyleSheet("color: #1565c0; font-weight: bold; padding: 4px 0;")
        f_layout.addRow(self.mw.acc_user_name)

        self.mw.acc_password = QLineEdit()
        self.mw.acc_password.setEchoMode(QLineEdit.Password)
        self.mw.acc_pin = QLineEdit()
        self.mw.acc_pin.setEchoMode(QLineEdit.Password)
        self.mw.acc_pin.setMaxLength(6)
        self.mw.acc_branch = QLineEdit()
        self.mw.acc_branch.setPlaceholderText("Chi nhánh")

        f_layout.addRow("Mật khẩu:", self.mw.acc_password)
        f_layout.addRow("Mã PIN:", self.mw.acc_pin)
        f_layout.addRow("Chi nhánh:", self.mw.acc_branch)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Tạo tài khoản")
        btn_submit.setObjectName("btnPrimary")
        btn_submit.clicked.connect(self._on_create)
        btn_clear = QPushButton("Làm mới")
        btn_clear.setObjectName("btnNormal")
        btn_clear.clicked.connect(self._clear)
        btn_row.addStretch()
        btn_row.addWidget(btn_submit)
        btn_row.addWidget(btn_clear)

        layout.addWidget(form_w)
        layout.addLayout(btn_row)
        layout.addStretch()

    def _clear(self):
        self.mw.acc_user_id.clear()
        self.mw.acc_user_name.clear()
        self.mw.acc_password.clear()
        self.mw.acc_pin.clear()
        self.mw.acc_branch.clear()

    def _on_find_user(self):
        user_id = self.mw.acc_user_id.text().strip()
        if not user_id:
            self.mw._show_error("Vui lòng nhập User ID!")
            return
        try:
            user = self.mw.bank.user_service.find_user_by_id(user_id)
            self.mw.acc_user_name.setText(f"Khách hàng: {user.full_name}")
        except ValueError as e:
            self.mw.acc_user_name.clear()
            self.mw._show_error(str(e))

    def _on_create(self):
        mw = self.mw
        user_id = mw.acc_user_id.text().strip()
        password = mw.acc_password.text().strip()
        pin = mw.acc_pin.text().strip()
        branch = mw.acc_branch.text().strip()

        if not all([user_id, password, pin, branch]):
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            account = mw.bank.create_account(user_id, password, pin, branch)
            msg = (f"Tạo tài khoản thành công!\n\n"
                   f"Số tài khoản: {account.account_id}\n"
                   f"Chủ tài khoản: {account.full_name}\n"
                   f"Số dư: {account.balance:,.0f} VND\n"
                   f"Chi nhánh: {account.create_at}")
            mw.bank.save_all_data()
            mw._show_success(msg)
            self._clear()
        except Exception as e:
            mw._show_error(str(e))
