from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt


class InterestPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()

    # ──────────────────────────────────────────────
    #  BUILD UI
    # ──────────────────────────────────────────────
    def _build(self):
        # 1. Layout dọc gốc quản lý toàn trang
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(14)

        # 2. Khung Panel chính bao bọc form nghiệp vụ
        form_frame = QFrame()
        form_frame.setObjectName("formPanel")

        f_layout = QFormLayout(form_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # ── HÀNG 1: MÃ SỔ TIẾT KIỆM + NÚT KIỂM TRA ─────────────────
        row_sid = QHBoxLayout()
        row_sid.setSpacing(8)

        self.mw.int_saving_id = QLineEdit()
        self.mw.int_saving_id.setObjectName("formInput")
        self.mw.int_saving_id.setPlaceholderText("Nhập mã số sổ tiết kiệm...")
        self.mw.int_saving_id.setFixedHeight(36)
        self.mw.int_saving_id.returnPressed.connect(self._on_check)

        btn_check = QPushButton("Kiểm tra sổ")
        btn_check.setObjectName("btnNormal")
        btn_check.setFixedHeight(36)
        btn_check.clicked.connect(self._on_check)

        row_sid.addWidget(self.mw.int_saving_id, 1)
        row_sid.addWidget(btn_check)

        lbl_sid_tag = QLabel("Mã sổ tiết kiệm: *")
        lbl_sid_tag.setObjectName("formLabel")
        f_layout.addRow(lbl_sid_tag, row_sid)

        # ── HÀNG 2: THÔNG TIN SỔ TIẾT KIỆM ─────────────────────
        lbl_info_tag = QLabel("Thông tin sổ:")
        lbl_info_tag.setObjectName("formLabel")

        self.mw.int_info = QLabel("Chưa thực hiện kiểm tra")
        self.mw.int_info.setStyleSheet("color: #1565c0; font-weight: bold; padding: 4px 0; font-size: 13px;")
        self.mw.int_info.setWordWrap(True)
        f_layout.addRow(lbl_info_tag, self.mw.int_info)

        # Thanh phân tách mảnh trước khi nhập mật khẩu xác thực
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("formSep")
        f_layout.addRow(sep)

        # ── HÀNG 3: MÃ PIN BẢO MẬT ────────────────────────────
        lbl_pin = QLabel("Mã PIN: *")
        lbl_pin.setObjectName("formLabel")
        self.mw.int_pin = QLineEdit()
        self.mw.int_pin.setEchoMode(QLineEdit.Password)
        self.mw.int_pin.setMaxLength(6)
        self.mw.int_pin.setPlaceholderText("Nhập mã PIN 6 số để rút lãi...")
        f_layout.addRow(lbl_pin, self.mw.int_pin)

        # Định dạng chiều cao và ObjectName cho các ô nhập bảo mật nhóm dưới
        self.mw.int_pin.setObjectName("formInput")
        self.mw.int_pin.setFixedHeight(36)
        # Nạp toàn bộ khối Panel Form vào giao diện chính
        layout.addWidget(form_frame)

        # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Rút lãi")
        btn_submit.setObjectName("btnPrimary")
        btn_submit.setFixedHeight(38)
        btn_submit.clicked.connect(self._on_withdraw)

        btn_clear = QPushButton("Làm mới")
        btn_clear.setObjectName("btnNormal")
        btn_clear.setFixedHeight(38)
        btn_clear.clicked.connect(self._clear)

        btn_row.addStretch()
        btn_row.addWidget(btn_clear)
        btn_row.addWidget(btn_submit)

        layout.addLayout(btn_row)
        layout.addStretch()

    # ──────────────────────────────────────────────
    #  LOGIC METHODS
    # ──────────────────────────────────────────────
    def _clear(self):
        """Xóa sạch các trường dữ liệu và reset nhãn thông báo"""
        self.mw.int_saving_id.clear()
        self.mw.int_pin.clear()
        self.mw.int_info.setText("Chưa thực hiện kiểm tra")

    def _on_check(self):
        mw = self.mw
        saving_id = mw.int_saving_id.text().strip()
        if not saving_id:
            mw._show_error("Vui lòng điền mã số sổ tiết kiệm cần kiểm tra!")
            return
        try:
            saving = mw.bank.saving_service.find_saving_account(saving_id)
            interest = mw.bank.saving_service.calculate_interest(saving_id)
            mw.int_info.setText(
                f"Chủ sổ: {saving.full_name} | Số tiền gốc: {saving.amount:,.0f} VND\n"
                f"Tiền lãi hiện tại: {interest:,.0f} VND\n"
                f"Trạng thái sổ: {saving.status}"
            )
        except ValueError as e:
            mw.int_info.setText(f"Không tìm thấy thông tin: {str(e)}")

    def _on_withdraw(self):
        mw = self.mw
        saving_id = mw.int_saving_id.text().strip()
        pin = mw.int_pin.text().strip()

        if not saving_id or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin giao dịch bắt buộc (*)!")
            return

        try:
            account, interest = mw.bank.withdraw_interest(saving_id, pin)
            account_id = account.account_id
            msg = (f"Thực hiện rút lãi tiết kiệm thành công!\n\n"
                   f"• Tiền lãi trích xuất: +{interest:,.0f} VND\n"
                   f"• Đã chuyển vào TK:  {account_id}\n"
                   f"• Số dư mới của TK:   {account.balance:,.0f} VND")
            
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))

    # ──────────────────────────────────────────────
    #  STYLESHEET CSS ĐỒNG BỘ TEMPLATE
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
                margin: 4px 0;
            }

            /* ── Inputs (QLineEdit) ── */
            QLineEdit#formInput {
                border: 1.5px solid #c5cae9;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 13px;
                background: white;
                color: #263238;
            }
            QLineEdit#formInput:focus {
                border-color: #3f51b5;
                background: #fafbff;
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

            /* ── Nút làm mới, nút tra cứu phụ ── */
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