from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel
)


class DepositPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.dep_account_id = QLineEdit()
        self.mw.dep_amount = QLineEdit()
        self.mw.dep_amount.setPlaceholderText("Số tiền nạp")
        self.mw.dep_pin = QLineEdit()
        self.mw.dep_pin.setEchoMode(QLineEdit.Password)
        self.mw.dep_pin.setMaxLength(6)

        f_layout.addRow("Số tài khoản:", self.mw.dep_account_id)
        f_layout.addRow("Số tiền:", self.mw.dep_amount)
        f_layout.addRow("Mã PIN:", self.mw.dep_pin)

        self.mw.dep_info_label = QLabel()
        self.mw.dep_info_label.setStyleSheet("color: #1565c0; padding: 8px;")
        f_layout.addRow(self.mw.dep_info_label)

        btn_check = QPushButton("Kiểm tra tài khoản")
        btn_check.setObjectName("btnNormal")
        btn_check.clicked.connect(self._on_check)
        f_layout.addRow("", btn_check)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Nạp tiền")
        btn_submit.setObjectName("btnSuccess")
        btn_submit.clicked.connect(self._on_deposit)
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
        self.mw.dep_account_id.clear()
        self.mw.dep_amount.clear()
        self.mw.dep_pin.clear()
        self.mw.dep_info_label.clear()

    def _on_check(self):
        mw = self.mw
        account_id = mw.dep_account_id.text().strip()
        if not account_id:
            return
        try:
            acc = mw.bank.account_service.find_account(account_id)
            mw.dep_info_label.setText(
                f"Chủ TK: {acc.full_name} | Số dư: {acc.balance:,.0f} VND | "
                f"Trạng thái: {acc.status}"
            )
        except ValueError:
            mw.dep_info_label.setText("Không tìm thấy tài khoản!")

    def _on_deposit(self):
        mw = self.mw
        account_id = mw.dep_account_id.text().strip()
        amount_text = mw.dep_amount.text().strip()
        pin = mw.dep_pin.text().strip()

        if not account_id or not amount_text or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            amount = float(amount_text)
            account, trans = mw.bank.deposit_money(account_id, amount, pin)
            msg = (f"Nạp {amount:,.0f} VND thành công!\n\n"
                   f"Số dư mới: {account.balance:,.0f} VND\n"
                   f"Mã GD: {trans.trans_id}")
            mw._show_success(msg)
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))
