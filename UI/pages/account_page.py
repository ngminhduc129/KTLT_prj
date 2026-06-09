from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt

class AccountPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()

    def _build(self):
            # 1. Layout gốc cho trang
            layout = QVBoxLayout(self)
            layout.setContentsMargins(20, 20, 20, 16)
            layout.setSpacing(14)

            # 2. Khung Panel chứa Form nhập liệu
            form_frame = QFrame()
            form_frame.setObjectName("formPanel")

            f_layout = QFormLayout(form_frame)
            f_layout.setContentsMargins(20, 18, 20, 18)
            f_layout.setSpacing(12)
            f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # ── HÀNG 1: USER ID + NÚT TRA CỨU ─────────────────
            row1 = QHBoxLayout()
            row1.setSpacing(8)

            self.mw.acc_user_id = QLineEdit()
            self.mw.acc_user_id.setObjectName("formInput")
            self.mw.acc_user_id.setPlaceholderText("Nhập User ID để kiểm tra...")
            self.mw.acc_user_id.setFixedHeight(36)
            self.mw.acc_user_id.returnPressed.connect(self._on_find_user)

            btn_find = QPushButton("Tra cứu")
            btn_find.setObjectName("btnNormal")
            btn_find.setFixedHeight(36)
            btn_find.clicked.connect(self._on_find_user)

            row1.addWidget(self.mw.acc_user_id, 1)
            row1.addWidget(btn_find)

            lbl_user_id = QLabel("User ID: *")
            lbl_user_id.setObjectName("formLabel")
            f_layout.addRow(lbl_user_id, row1)

        # ── HÀNG 2: THÔNG TIN CHI TIẾT KHÁCH HÀNG ──────────────────
            # Khởi tạo các QLabel hiển thị thông tin dạng Read-Only
            self.mw.acc_user_name = QLabel("—")
            self.mw.acc_user_phone = QLabel("—")
            self.mw.acc_user_email = QLabel("—")
            self.mw.acc_user_dob = QLabel("—")

            # Định dạng Style chung cho các nhãn kết quả để nhìn nổi bật và đồng bộ
            extended_info_style = "color: #1565c0; font-weight: 600; padding: 2px 0; font-size: 13px;"
            for lbl_widget in [self.mw.acc_user_name, self.mw.acc_user_phone, 
                            self.mw.acc_user_email, self.mw.acc_user_dob]:
                lbl_widget.setStyleSheet(extended_info_style)

            # Tạo các nhãn tiêu đề cột trái
            lbl_name_tag = QLabel("Tên khách hàng:")
            lbl_phone_tag = QLabel("Số điện thoại:")
            lbl_email_tag = QLabel("Email:")
            lbl_dob_tag = QLabel("Ngày sinh:")

            for lbl_tag in [lbl_name_tag, lbl_phone_tag, lbl_email_tag, lbl_dob_tag]:
                lbl_tag.setObjectName("formLabel")

            # Đẩy tuần tự các hàng thông tin vào QFormLayout
            f_layout.addRow(lbl_name_tag, self.mw.acc_user_name)
            f_layout.addRow(lbl_phone_tag, self.mw.acc_user_phone)
            f_layout.addRow(lbl_email_tag, self.mw.acc_user_email)
            f_layout.addRow(lbl_dob_tag, self.mw.acc_user_dob)

            # Thêm một đường phân cách mảnh trước khi sang phần nhập dữ liệu tài khoản mới
            sep_info = QFrame()
            sep_info.setFrameShape(QFrame.HLine)
            sep_info.setObjectName("formSep")
            f_layout.addRow(sep_info)

            # ── HÀNG 3: MẬT KHẨU ──────────────────────────────
            lbl_pwd = QLabel("Mật khẩu: *")
            lbl_pwd.setObjectName("formLabel")
            self.mw.acc_password = QLineEdit()
            self.mw.acc_password.setObjectName("formInput")
            self.mw.acc_password.setEchoMode(QLineEdit.Password)
            self.mw.acc_password.setFixedHeight(36)
            f_layout.addRow(lbl_pwd, self.mw.acc_password)

            # ── HÀNG 4: MÃ PIN ────────────────────────────────
            lbl_pin = QLabel("Mã PIN: *")
            lbl_pin.setObjectName("formLabel")
            self.mw.acc_pin = QLineEdit()
            self.mw.acc_pin.setObjectName("formInput")
            self.mw.acc_pin.setEchoMode(QLineEdit.Password)
            self.mw.acc_pin.setMaxLength(6)
            self.mw.acc_pin.setFixedHeight(36)
            f_layout.addRow(lbl_pin, self.mw.acc_pin)

            # ── HÀNG 5: CHI NHÁNH ─────────────────────────────
            lbl_brc = QLabel("Chi nhánh: *")
            lbl_brc.setObjectName("formLabel")
            self.mw.acc_branch = QLineEdit()
            self.mw.acc_branch.setObjectName("formInput")
            self.mw.acc_branch.setPlaceholderText("Nhập tên chi nhánh ngân hàng...")
            self.mw.acc_branch.setFixedHeight(36)
            f_layout.addRow(lbl_brc, self.mw.acc_branch)

            # Đẩy khung form hoàn chỉnh vào layout trang chính
            layout.addWidget(form_frame)

            # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
            btn_row = QHBoxLayout()
            btn_row.setSpacing(8)

            btn_submit = QPushButton("Tạo tài khoản")
            btn_submit.setObjectName("btnPrimary")
            btn_submit.setFixedHeight(38)
            btn_submit.clicked.connect(self._on_create)

            btn_clear = QPushButton("Làm mới")
            btn_clear.setObjectName("btnNormal")
            btn_clear.setFixedHeight(38)
            btn_clear.clicked.connect(self._clear)

            btn_row.addStretch()
            btn_row.addWidget(btn_clear)
            btn_row.addWidget(btn_submit)

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
                # Gọi service tìm kiếm thông tin khách hàng từ backend
                user = self.mw.bank.user_service.find_user_by_id(user_id)
                
                self.mw.acc_user_name.setText(user.full_name)
                self.mw.acc_user_phone.setText(user.phone if user.phone else "—")
                self.mw.acc_user_email.setText(user.email if user.email else "—")
                self.mw.acc_user_dob.setText(user.dob if user.dob else "—")
                
            except ValueError as e:
                # Nếu không tìm thấy, reset các trường về trạng thái ban đầu
                self.mw.acc_user_name.setText("Không tìm thấy")
                self.mw.acc_user_phone.setText("—")
                self.mw.acc_user_email.setText("—")
                self.mw.acc_user_dob.setText("—")
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