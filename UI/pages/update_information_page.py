from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QComboBox, QFrame, QLabel
)
from PyQt5.QtCore import Qt

class UpdateInformationPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()

    def _build(self):
        root =QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(14)

        # Panel Form thong tin
        form_frame = QFrame()
        form_frame.setObjectName("formPanel")

        # Su dung QFormLayout nam ben trong Panel
        f_layout = QFormLayout(form_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Khoi tao o nhap lieu
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
        self.sex_input.setObjectName("formInput")
        self.address_input = QLineEdit()
        self.job_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText(
            "dd/mm/yyyy"
        )

        # =================================================
        # FORM
        # =================================================
        f_layout.addRow(self._create_form_label("User ID: *"), self.user_id_input)
        f_layout.addRow(self._create_form_label("Họ tên: *"), self.full_name_input)
        f_layout.addRow(self._create_form_label("Số điện thoại: *"), self.phone_input)
        f_layout.addRow(self._create_form_label("Email:"), self.email_input)
        f_layout.addRow(self._create_form_label("Giới tính:"), self.sex_input)
        f_layout.addRow(self._create_form_label("Địa chỉ:"), self.address_input)
        f_layout.addRow(self._create_form_label("Nghề nghiệp:"), self.job_input)
        f_layout.addRow(self._create_form_label("Ngày sinh:"), self.dob_input)

        root.addWidget(form_frame)

        # =================================================
        # BUTTONS
        # =================================================
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_update = QPushButton("Cập nhật")
        btn_update.setObjectName("btnPrimary")
        btn_update.setFixedHeight(38)
        btn_update.clicked.connect(self._on_update)

        btn_clear = QPushButton("Làm mới")
        btn_clear.setObjectName("btnNormal")
        btn_clear.setFixedHeight(38)
        btn_clear.clicked.connect(self._clear)

        btn_row.addStretch()
        btn_row.addWidget(btn_update)
        btn_row.addWidget(btn_clear)
        root.addLayout(btn_row)

        root.addStretch()

    def _create_form_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("formLabel")
        return lbl
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

    # ──────────────────────────────────────────────
    #  STYLES
    # ──────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""

            /* ── Panel Form bao bọc ── */
            QFrame#formPanel {
                background: #f8f9ff;
                border: 1px solid #c5cae9;
                border-radius: 10px;
            }
            QLabel#formLabel {
                font-size: 13px;
                font-weight: 600;
                color: #37474f;
                min-width: 100px;
            }
            QFrame#formSep {
                color: #dde1f5;
                margin: 6px 0;
            }

            /* ── Inputs (LineEdit & ComboBox) ── */
            QLineEdit#formInput, QComboBox#formInput {
                border: 1.5px solid #c5cae9;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 13px;
                background: white;
                color: #263238;
            }
            QLineEdit#formInput:focus, QComboBox#formInput:focus {
                border-color: #3f51b5;
                background: #fafbff;
            }
            
            /* Cấu hình thêm cho ComboBox */
            QComboBox#formInput::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox#formInput::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7986cb;
                width: 0;
                height: 0;
            }

            /* ── Nút submit chính ── */
            QPushButton#btnPrimary {
                background: #3f51b5;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 0 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#btnPrimary:hover  { background: #303f9f; }
            QPushButton#btnPrimary:pressed{ background: #283593; }

            /* ── Nút làm mới phụ ── */
            QPushButton#btnNormal {
                background: #eceff1;
                color: #37474f;
                border: 1px solid #cfd8dc;
                border-radius: 7px;
                padding: 0 20px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#btnNormal:hover { background: #e0e0e0; }
        """)