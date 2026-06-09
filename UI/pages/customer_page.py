from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt


class CustomerPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()

    # ──────────────────────────────────────────────
    #  BUILD UI
    # ──────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(14)

        # ── Panel Form thông tin ─────────────────────
        form_frame = QFrame()
        form_frame.setObjectName("formPanel")
        
        # Sử dụng QFormLayout nằm bên trong Panel
        f_layout = QFormLayout(form_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Khởi tạo các ô nhập liệu của Form
        self.mw.cust_user_id = QLineEdit()
        self.mw.cust_full_name = QLineEdit()
        self.mw.cust_phone = QLineEdit()
        self.mw.cust_email = QLineEdit()
        
        self.mw.cust_sex = QComboBox()
        self.mw.cust_sex.addItems(["Nam", "Nữ", "Khác"])
        self.mw.cust_sex.setFixedHeight(36)
        self.mw.cust_sex.setObjectName("formInput")
        
        self.mw.cust_address = QLineEdit()
        self.mw.cust_job = QLineEdit()
        
        self.mw.cust_dob = QLineEdit()
        self.mw.cust_dob.setPlaceholderText("dd/mm/yyyy")

        # Định dạng chiều cao và định danh (ObjectName) cho các QLineEdit nhóm 1
        for widget in [self.mw.cust_user_id, self.mw.cust_full_name, self.mw.cust_phone,
                       self.mw.cust_email, self.mw.cust_address, self.mw.cust_job, self.mw.cust_dob]:
            widget.setFixedHeight(36)
            widget.setObjectName("formInput")

        # Thêm các hàng vào nhóm thông tin cá nhân
        f_layout.addRow(self._create_form_label("User ID: *"), self.mw.cust_user_id)
        f_layout.addRow(self._create_form_label("Họ tên: *"), self.mw.cust_full_name)
        f_layout.addRow(self._create_form_label("Số điện thoại: *"), self.mw.cust_phone)
        f_layout.addRow(self._create_form_label("Email:"), self.mw.cust_email)
        f_layout.addRow(self._create_form_label("Giới tính:"), self.mw.cust_sex)
        f_layout.addRow(self._create_form_label("Địa chỉ:"), self.mw.cust_address)
        f_layout.addRow(self._create_form_label("Nghề nghiệp:"), self.mw.cust_job)
        f_layout.addRow(self._create_form_label("Ngày sinh:"), self.mw.cust_dob)

        # Thanh phân tách (Separator mảnh) giữa 2 phân khu thông tin
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("formSep")
        f_layout.addRow(sep)

        # Khởi tạo các ô nhập liệu nhóm bảo mật hệ thống
        self.mw.cust_branch = QLineEdit()
        self.mw.cust_branch.setPlaceholderText("Chi nhánh mở tài khoản")
        
        self.mw.cust_password = QLineEdit()
        self.mw.cust_password.setEchoMode(QLineEdit.Password)
        
        self.mw.cust_pin = QLineEdit()
        self.mw.cust_pin.setEchoMode(QLineEdit.Password)
        self.mw.cust_pin.setMaxLength(6)

        # Định dạng chiều cao và định danh cho nhóm bảo mật
        for widget in [self.mw.cust_branch, self.mw.cust_password, self.mw.cust_pin]:
            widget.setFixedHeight(36)
            widget.setObjectName("formInput")

        # Thêm các hàng vào nhóm tài khoản hệ thống
        f_layout.addRow(self._create_form_label("Chi nhánh: *"), self.mw.cust_branch)
        f_layout.addRow(self._create_form_label("Mật khẩu: *"), self.mw.cust_password)
        f_layout.addRow(self._create_form_label("Mã PIN: *"), self.mw.cust_pin)

        root.addWidget(form_frame)

        # ── Dòng nút bấm hành động ────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Tạo khách hàng + Tài khoản")
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
        root.addLayout(btn_row)
        
        root.addStretch()

    def _create_form_label(self, text):
        """Hàm hỗ trợ tạo nhanh Label cho form đúng chuẩn định dạng CSS"""
        lbl = QLabel(text)
        lbl.setObjectName("formLabel")
        return lbl

    # ──────────────────────────────────────────────
    #  LOGIC HANDLERS
    # ──────────────────────────────────────────────
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
            mw._show_error("Vui lòng điền đầy đủ các thông tin bắt buộc (*)")
            return

        try:
            user, account = mw.bank.create_customer_and_account(
                user_id, full_name, phone, email, sex, address, job, dob,
                password, pin, branch
            )
            msg = (f"🎉 Tạo khách hàng thành công!\n\n"
                   f"User ID: {user.user_id}\n"
                   f"Họ tên: {user.full_name}\n\n"
                   f"Tài khoản cấp: {account.account_id}\n"
                   f"Số dư mặc định: {account.balance:,.0f} VND")
            mw.bank.save_all_data()
            mw._show_success(msg)
            self._clear()
        except Exception as e:
            mw._show_error(str(e))

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