from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QComboBox
)


class UpdateInformationPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        form_w = QWidget()
        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        # =================================================
        # INPUTS
        # =================================================
        self.user_id_input = QLineEdit()

        self.full_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        self.sex_input = QComboBox()
        self.sex_input.addItems([
            "",
            "Nam",
            "Nữ",
            "Khác"
        ])

        self.address_input = QLineEdit()
        self.job_input = QLineEdit()
        self.dob_input = QLineEdit()

        self.dob_input.setPlaceholderText(
            "dd/mm/yyyy"
        )

        # =================================================
        # FORM
        # =================================================
        f_layout.addRow("User ID:", self.user_id_input)
        f_layout.addRow("Họ tên:", self.full_name_input)
        f_layout.addRow("Số điện thoại:", self.phone_input)
        f_layout.addRow("Email:", self.email_input)
        f_layout.addRow("Giới tính:", self.sex_input)
        f_layout.addRow("Địa chỉ:", self.address_input)
        f_layout.addRow("Nghề nghiệp:", self.job_input)
        f_layout.addRow("Ngày sinh:", self.dob_input)

        # =================================================
        # BUTTONS
        # =================================================
        btn_row = QHBoxLayout()

        btn_update = QPushButton("Cập nhật")
        btn_update.setObjectName("btnPrimary")
        btn_update.clicked.connect(self._on_update)

        btn_clear = QPushButton("Làm mới")
        btn_clear.setObjectName("btnNormal")
        btn_clear.clicked.connect(self._clear)

        btn_row.addStretch()
        btn_row.addWidget(btn_update)
        btn_row.addWidget(btn_clear)

        # =================================================
        # MAIN LAYOUT
        # =================================================
        layout.addWidget(form_w)
        layout.addLayout(btn_row)
        layout.addStretch()

    # =====================================================
    # CLEAR FORM
    # =====================================================
    def _clear(self):
        self.user_id_input.clear()
        self.full_name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.job_input.clear()
        self.dob_input.clear()

        self.sex_input.setCurrentIndex(0)

    # =====================================================
    # UPDATE CUSTOMER
    # =====================================================
    def _on_update(self):

        user_id = self.user_id_input.text().strip()

        full_name = self.full_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        sex = self.sex_input.currentText().strip()
        address = self.address_input.text().strip()
        job = self.job_input.text().strip()
        dob = self.dob_input.text().strip()

        if not user_id:
            self.mw._show_error(
                "Vui lòng nhập User ID!"
            )
            return

        try:

            # =============================================
            # FIND USER
            # =============================================
            user = self.mw.bank.user_service.find_user_by_id(
                user_id
            )

            # =============================================
            # UPDATE FULL NAME
            # =============================================
            if full_name:
                user.full_name = full_name

            # =============================================
            # UPDATE PHONE
            # =============================================
            if phone:

                if not phone.isdigit():
                    raise ValueError(
                        "Phone number must contain only numbers."
                    )

                if len(phone) != 10:
                    raise ValueError(
                        "Phone number must be exactly 10 digits."
                    )

                user.phone = phone

            # =============================================
            # UPDATE EMAIL
            # =============================================
            if email:

                self.mw.bank.user_service.validate_email(
                    email
                )

                user.email = email

            # =============================================
            # UPDATE SEX
            # =============================================
            if sex:
                user.sex = sex

            # =============================================
            # UPDATE ADDRESS
            # =============================================
            if address:
                user.address = address

            # =============================================
            # UPDATE JOB
            # =============================================
            if job:
                user.job = job

            # =============================================
            # UPDATE DOB
            # =============================================
            if dob:
                user.dob = dob

            # =============================================
            # SAVE DATA
            # =============================================
            self.mw.bank.save_all_data()

            self.mw._show_success(
                f"Cập nhật thông tin khách hàng "
                f"{user.user_id} thành công!"
            )

            self._clear()

        except Exception as e:
            self.mw._show_error(str(e))