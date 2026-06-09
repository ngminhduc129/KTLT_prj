from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt


class TransferPage(QWidget):
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


        # 2. Khung Panel chính bao bọc toàn bộ form giao dịch
        form_frame = QFrame()
        form_frame.setObjectName("formPanel")

        f_layout = QFormLayout(form_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Khởi tạo các ô nhập liệu
        self.mw.tr_src_id = QLineEdit()
        self.mw.tr_src_id.setPlaceholderText("Nhập số tài khoản trích tiền...")

        self.mw.tr_dst_id = QLineEdit()
        self.mw.tr_dst_id.setPlaceholderText("Nhập số tài khoản thụ hưởng...")

        self.mw.tr_amount = QLineEdit()
        self.mw.tr_amount.setPlaceholderText("Nhập số tiền chuyển (VND)...")

        self.mw.tr_pin = QLineEdit()
        self.mw.tr_pin.setEchoMode(QLineEdit.Password)
        self.mw.tr_pin.setMaxLength(6)
        self.mw.tr_pin.setPlaceholderText("Nhập mã PIN 6 số...")

        self.mw.tr_password = QLineEdit()
        self.mw.tr_password.setEchoMode(QLineEdit.Password)
        self.mw.tr_password.setPlaceholderText("Nhập mật khẩu xác thực...")

        for widget in [self.mw.tr_src_id, self.mw.tr_dst_id, self.mw.tr_amount, 
                       self.mw.tr_pin, self.mw.tr_password]:
            widget.setObjectName("formInput")
            widget.setFixedHeight(36)

        # Tạo các nhãn cột bên trái theo định dạng chuẩn CSS
        lbl_src = QLabel("TK nguồn: *")
        lbl_dst = QLabel("TK đích: *")
        lbl_amt = QLabel("Số tiền: *")
        lbl_pin = QLabel("Mã PIN: *")
        lbl_pwd = QLabel("Mật khẩu: *")

        for lbl in [lbl_src, lbl_dst, lbl_amt, lbl_pin, lbl_pwd]:
            lbl.setObjectName("formLabel")

        # Đẩy các hàng vào QFormLayout
        f_layout.addRow(lbl_src, self.mw.tr_src_id)
        f_layout.addRow(lbl_dst, self.mw.tr_dst_id)
        f_layout.addRow(lbl_amt, self.mw.tr_amount)
        f_layout.addRow(lbl_pin, self.mw.tr_pin)
        f_layout.addRow(lbl_pwd, self.mw.tr_password)

        # Nạp toàn bộ khối Panel Form vào giao diện chính
        layout.addWidget(form_frame)

        # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Chuyển khoản")
        btn_submit.setObjectName("btnPrimary")
        btn_submit.setFixedHeight(38)
        btn_submit.clicked.connect(self._on_transfer)

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
            mw._show_error("Vui lòng điền đầy đủ thông tin giao dịch bắt buộc (*)!")
            return

        if src == dst:
            mw._show_error("Tài khoản nguồn và tài khoản đích không được trùng nhau!")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                mw._show_error("Số tiền thực hiện chuyển khoản phải lớn hơn 0 ₫!")
                return
        except ValueError:
            mw._show_error("Số tiền không hợp lệ! Vui lòng chỉ nhập các ký tự số liền nhau.")
            return

        try:
            src_acc, dst_acc = mw.bank.transfer_money(
                src, dst, amount, pin, password
            )
            msg = (f" Chuyển khoản thành công!\n\n"
                   f"Số tiền đã chuyển: {amount:,.0f} VND\n\n"
                   f"TK nguồn ({src}): {src_acc.balance:,.0f} VND\n"
                   f"TK đích ({dst}): {dst_acc.balance:,.0f} VND")
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except Exception as e:
            mw._show_error(str(e))

    # ──────────────────────────────────────────────
    #  STYLESHEET CSS
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

            /* ── Nút submit chuyển khoản chính ── */
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