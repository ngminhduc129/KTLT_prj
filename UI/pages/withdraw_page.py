from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout
)


class WithdrawPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.wd_account_id = QLineEdit()
        self.mw.wd_amount = QLineEdit()
        self.mw.wd_amount.setPlaceholderText("Số tiền rút")
        self.mw.wd_pin = QLineEdit()
        self.mw.wd_pin.setEchoMode(QLineEdit.Password)
        self.mw.wd_pin.setMaxLength(6)

        f_layout.addRow("Số tài khoản:", self.mw.wd_account_id)
        f_layout.addRow("Số tiền:", self.mw.wd_amount)
        f_layout.addRow("Mã PIN:", self.mw.wd_pin)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Rút tiền")
        btn_submit.setObjectName("btnDanger")
        btn_submit.clicked.connect(self._on_withdraw)
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
        self.mw.wd_account_id.clear()
        self.mw.wd_amount.clear()
        self.mw.wd_pin.clear()

    def _on_withdraw(self):
        mw = self.mw
        account_id = mw.wd_account_id.text().strip()
        amount_text = mw.wd_amount.text().strip()
        pin = mw.wd_pin.text().strip()

        if not account_id or not amount_text or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            amount = float(amount_text)
            account, trans = mw.bank.withdraw_money(account_id, amount, pin)
            msg = (f"Rút {amount:,.0f} VND thành công!\n\n"
                   f"Số dư mới: {account.balance:,.0f} VND\n"
                   f"Mã GD: {trans.trans_id}")
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))
