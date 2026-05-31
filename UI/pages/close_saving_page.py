from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel
)


class CloseSavingPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.cls_saving_id = QLineEdit()
        # self.mw.cls_password = QLineEdit()
        # self.mw.cls_password.setEchoMode(QLineEdit.Password)
        self.mw.cls_pin = QLineEdit()
        self.mw.cls_pin.setEchoMode(QLineEdit.Password)
        self.mw.cls_pin.setMaxLength(6)

        f_layout.addRow("Mã sổ tiết kiệm:", self.mw.cls_saving_id)
        # f_layout.addRow("Mật khẩu:", self.mw.cls_password)
        f_layout.addRow("Mã PIN:", self.mw.cls_pin)

        self.mw.cls_info = QLabel()
        self.mw.cls_info.setStyleSheet("color: #1565c0; padding: 8px;")
        self.mw.cls_info.setWordWrap(True)
        f_layout.addRow(self.mw.cls_info)

        btn_check = QPushButton("Kiểm tra sổ")
        btn_check.setObjectName("btnNormal")
        btn_check.clicked.connect(self._on_check)
        f_layout.addRow("", btn_check)

        btn_submit = QPushButton("Tất toán sổ")
        btn_submit.setObjectName("btnDanger")
        btn_submit.clicked.connect(self._on_close)
        f_layout.addRow("", btn_submit)

        layout.addWidget(form_w)
        layout.addStretch()

    def _on_check(self):
        mw = self.mw
        saving_id = mw.cls_saving_id.text().strip()
        if not saving_id:
            return
        try:
            saving = mw.bank.saving_service.find_saving_account(saving_id)
            interest = mw.bank.saving_service.calculate_interest(saving_id)
            total = saving.amount + interest
            mw.cls_info.setText(
                f"Chủ sổ: {saving.full_name}\n"
                f"Tiền gốc: {saving.amount:,.0f} VND\n"
                f"Tiền lãi: {interest:,.0f} VND\n"
                f"Tổng nhận: {total:,.0f} VND\n"
                f"Trạng thái: {saving.status}"
            )
        except ValueError as e:
            mw.cls_info.setText(f"Lỗi: {str(e)}")

    def _on_close(self):
        mw = self.mw
        saving_id = mw.cls_saving_id.text().strip()
        password = mw.cls_password.text().strip()
        pin = mw.cls_pin.text().strip()

        if not saving_id or not password or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            account, total = mw.bank.close_saving_account(saving_id, password, pin)
            account_id = account.account_id
            msg = (f"Tất toán thành công!\n\n"
                   f"Tổng tiền nhận: {total:,.0f} VND\n"
                   f"Đã chuyển vào TK: {account_id}\n"
                   f"Số dư mới: {account.balance:,.0f} VND")
            mw._show_success(msg)
        except ValueError as e:
            mw._show_error(str(e))
