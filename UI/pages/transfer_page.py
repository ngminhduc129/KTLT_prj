from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout
)


class TransferPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.tr_src_id = QLineEdit()
        self.mw.tr_dst_id = QLineEdit()
        self.mw.tr_amount = QLineEdit()
        self.mw.tr_amount.setPlaceholderText("Số tiền chuyển")
        self.mw.tr_pin = QLineEdit()
        self.mw.tr_pin.setEchoMode(QLineEdit.Password)
        self.mw.tr_pin.setMaxLength(6)
        self.mw.tr_password = QLineEdit()
        self.mw.tr_password.setEchoMode(QLineEdit.Password)

        f_layout.addRow("TK nguồn:", self.mw.tr_src_id)
        f_layout.addRow("TK đích:", self.mw.tr_dst_id)
        f_layout.addRow("Số tiền:", self.mw.tr_amount)
        f_layout.addRow("Mã PIN:", self.mw.tr_pin)
        f_layout.addRow("Mật khẩu:", self.mw.tr_password)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Chuyển khoản")
        btn_submit.setObjectName("btnPrimary")
        btn_submit.clicked.connect(self._on_transfer)
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
        self.mw.tr_src_id.clear()
        self.mw.tr_dst_id.clear()
        self.mw.tr_amount.clear()
        self.mw.tr_pin.clear()
        self.mw.tr_password.clear()

    def _on_transfer(self):
        mw = self.mw
        src = mw.tr_src_id.text().strip()
        dst = mw.tr_dst_id.text().strip()
        amount_text = mw.tr_amount.text().strip()
        pin = mw.tr_pin.text().strip()
        password = mw.tr_password.text().strip()

        if not all([src, dst, amount_text, pin, password]):
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            amount = float(amount_text)
            src_acc, dst_acc = mw.bank.transfer_money(
                src, dst, amount, pin, password
            )
            msg = (f"Chuyển {amount:,.0f} VND thành công!\n\n"
                   f"TK nguồn ({src}): {src_acc.balance:,.0f} VND\n"
                   f"TK đích ({dst}): {dst_acc.balance:,.0f} VND")
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))
