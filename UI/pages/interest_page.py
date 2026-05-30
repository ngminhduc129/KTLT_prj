from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel
)


class InterestPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.int_saving_id = QLineEdit()
        self.mw.int_password = QLineEdit()
        self.mw.int_password.setEchoMode(QLineEdit.Password)
        self.mw.int_pin = QLineEdit()
        self.mw.int_pin.setEchoMode(QLineEdit.Password)
        self.mw.int_pin.setMaxLength(6)

        f_layout.addRow("Mã sổ tiết kiệm:", self.mw.int_saving_id)
        f_layout.addRow("Mật khẩu:", self.mw.int_password)
        f_layout.addRow("Mã PIN:", self.mw.int_pin)

        self.mw.int_info = QLabel()
        self.mw.int_info.setStyleSheet("color: #1565c0; padding: 8px;")
        self.mw.int_info.setWordWrap(True)
        f_layout.addRow(self.mw.int_info)

        btn_check = QPushButton("Kiểm tra sổ")
        btn_check.setObjectName("btnNormal")
        btn_check.clicked.connect(self._on_check)
        f_layout.addRow("", btn_check)

        btn_submit = QPushButton("Rút lãi")
        btn_submit.setObjectName("btnPrimary")
        btn_submit.clicked.connect(self._on_withdraw)
        f_layout.addRow("", btn_submit)

        layout.addWidget(form_w)
        layout.addStretch()

    def _on_check(self):
        mw = self.mw
        saving_id = mw.int_saving_id.text().strip()
        if not saving_id:
            return
        try:
            saving = mw.bank.saving_service.find_saving_account(saving_id)
            interest = mw.bank.saving_service.calculate_interest(saving_id)
            mw.int_info.setText(
                f"Chủ sổ: {saving.full_name} | Số tiền gốc: {saving.amount:,.0f} VND\n"
                f"Tiền lãi hiện tại: {interest:,.0f} VND\n"
                f"Trạng thái: {saving.status}"
            )
        except ValueError as e:
            mw.int_info.setText(f"Lỗi: {str(e)}")

    def _on_withdraw(self):
        mw = self.mw
        saving_id = mw.int_saving_id.text().strip()
        password = mw.int_password.text().strip()
        pin = mw.int_pin.text().strip()

        if not saving_id or not password or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            account, interest = mw.bank.withdraw_interest(saving_id, pin)
            account_id = account.account_id
            msg = (f"Rút lãi thành công!\n\n"
                   f"Tiền lãi: {interest:,.0f} VND\n"
                   f"Đã chuyển vào TK: {account_id}\n"
                   f"Số dư mới: {account.balance:,.0f} VND")
            mw._show_success(msg)
        except ValueError as e:
            mw._show_error(str(e))
