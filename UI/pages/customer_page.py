from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt


class CustomerPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        self.mw.cust_user_id = QLineEdit()
        self.mw.cust_full_name = QLineEdit()
        self.mw.cust_phone = QLineEdit()
        self.mw.cust_email = QLineEdit()
        self.mw.cust_sex = QComboBox()
        self.mw.cust_sex.addItems(["Nam", "Nữ", "Khác"])
        self.mw.cust_address = QLineEdit()
        self.mw.cust_job = QLineEdit()
        self.mw.cust_dob = QLineEdit()
        self.mw.cust_dob.setPlaceholderText("dd/mm/yyyy")

        f_layout.addRow("User ID:", self.mw.cust_user_id)
        f_layout.addRow("Họ tên:", self.mw.cust_full_name)
        f_layout.addRow("Số điện thoại:", self.mw.cust_phone)
        f_layout.addRow("Email:", self.mw.cust_email)
        f_layout.addRow("Giới tính:", self.mw.cust_sex)
        f_layout.addRow("Địa chỉ:", self.mw.cust_address)
        f_layout.addRow("Nghề nghiệp:", self.mw.cust_job)
        f_layout.addRow("Ngày sinh:", self.mw.cust_dob)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #e0e0e0;")
        f_layout.addRow(sep)

        self.mw.cust_branch = QLineEdit()
        self.mw.cust_branch.setPlaceholderText("Chi nhánh mở tài khoản")
        self.mw.cust_password = QLineEdit()
        self.mw.cust_password.setEchoMode(QLineEdit.Password)
        self.mw.cust_pin = QLineEdit()
        self.mw.cust_pin.setEchoMode(QLineEdit.Password)
        self.mw.cust_pin.setMaxLength(6)

        f_layout.addRow("Chi nhánh:", self.mw.cust_branch)
        f_layout.addRow("Mật khẩu:", self.mw.cust_password)
        f_layout.addRow("Mã PIN:", self.mw.cust_pin)

        btn_row = QHBoxLayout()
        btn_submit = QPushButton("Tạo khách hàng + Tài khoản")
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
        for w in [self.mw.cust_user_id, self.mw.cust_full_name, self.mw.cust_phone,
                  self.mw.cust_email, self.mw.cust_address, self.mw.cust_job,
                  self.mw.cust_dob, self.mw.cust_branch, self.mw.cust_password,
                  self.mw.cust_pin]:
            w.clear()
        self.mw.cust_sex.setCurrentIndex(0)

    def _on_create(self):
        mw = self.mw
        user_id = mw.cust_user_id.text().strip()
        full_name = mw.cust_full_name.text().strip()
        phone = mw.cust_phone.text().strip()
        email = mw.cust_email.text().strip()
        sex = mw.cust_sex.currentText()
        address = mw.cust_address.text().strip()
        job = mw.cust_job.text().strip()
        dob = mw.cust_dob.text().strip()
        branch = mw.cust_branch.text().strip()
        password = mw.cust_password.text().strip()
        pin = mw.cust_pin.text().strip()

        if not all([user_id, full_name, phone, branch, password, pin]):
            mw._show_error("Vui lòng điền đầy đủ thông tin bắt buộc!")
            return

        try:
            user, account = mw.bank.create_customer_and_account(
                user_id, full_name, phone, email, sex, address, job, dob,
                password, pin, branch
            )
            msg = (f"Tạo khách hàng thành công!\n\n"
                   f"User ID: {user.user_id}\n"
                   f"Họ tên: {user.full_name}\n\n"
                   f"Tài khoản: {account.account_id}\n"
                   f"Số dư: {account.balance:,.0f} VND")
            mw._show_success(msg)
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))
