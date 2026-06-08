from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel
)


class SavingPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.sav_account_id = QLineEdit()
        self.mw.sav_amount = QLineEdit()
        self.mw.sav_amount.setPlaceholderText("Số tiền gửi")

        f_layout.addRow("Tài khoản nhận:", self.mw.sav_account_id)
        f_layout.addRow("Số tiền gửi:", self.mw.sav_amount)

        self.mw.sav_result = QLabel()
        self.mw.sav_result.setStyleSheet("color: #1565c0; padding: 8px;")
        self.mw.sav_result.setWordWrap(True)
        f_layout.addRow(self.mw.sav_result)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Gửi tiết kiệm")
        btn_submit.setObjectName("btnSuccess")
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
        self.mw.sav_account_id.clear()
        self.mw.sav_amount.clear()
        self.mw.sav_result.clear()

    def _on_create(self):
        mw = self.mw
        account_id = mw.sav_account_id.text().strip()
        amount_text = mw.sav_amount.text().strip()

        if not account_id or not amount_text:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            amount = float(amount_text)
            saving = mw.bank.create_saving(account_id, amount)
            msg = (f"Tạo sổ tiết kiệm thành công!\n\n"
                   f"Mã số: {saving.saving_id}\n"
                   f"Họ và tên: {saving.full_name}\n"
                   f"Mã khách hàng: {saving.user_id}\n"
                   f"Số tiền: {saving.amount:,.0f} VND\n"
                   f"Trạng thái: {saving.status}\n"
                   f"Kỳ hạn: {saving.term}\n"
                   f"Ngày phát hành: {saving.start_date}")
            mw.sav_result.setText(msg)
            mw._show_success("Tạo sổ tiết kiệm thành công!")
            mw.bank.save_all_data()
        except ValueError as e:
            mw._show_error(str(e))
        except TypeError as e:
            mw._show_error(f"Lỗi hệ thống: {str(e)}")
