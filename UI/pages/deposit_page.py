from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt


class DepositPage(QWidget):
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


        # 2. Khung Panel chính bao bọc form giao dịch
        form_w = QFrame()
        form_w.setObjectName("formPanel")

        f_layout = QFormLayout(form_w)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # ── HÀNG 1: SỐ TÀI KHOẢN + NÚT KIỂM TRA 
        row_acc = QHBoxLayout()
        row_acc.setSpacing(8)

        self.mw.dep_account_id = QLineEdit()
        self.mw.dep_account_id.setObjectName("formInput")
        self.mw.dep_account_id.setPlaceholderText("Nhập số tài khoản thanh toán...")
        self.mw.dep_account_id.setFixedHeight(36)
        self.mw.dep_account_id.returnPressed.connect(self._on_check)

        btn_check = QPushButton("Kiểm tra")
        btn_check.setObjectName("btnNormal")
        btn_check.setFixedHeight(36)
        btn_check.clicked.connect(self._on_check)

        row_acc.addWidget(self.mw.dep_account_id, 1)
        row_acc.addWidget(btn_check)

        lbl_uid = QLabel("Số tài khoản: *")
        lbl_uid.setObjectName("formLabel")
        f_layout.addRow(lbl_uid, row_acc)

        # ── HÀNG 2: THÔNG TIN CHỦ TÀI KHOẢN 
        lbl_info_tag = QLabel("Thông tin tài khoản:")
        lbl_info_tag.setObjectName("formLabel")
        
        self.mw.dep_info_label = QLabel("Chưa kiểm tra")
        self.mw.dep_info_label.setStyleSheet("color: #1565c0; font-weight: bold; padding: 4px 0;")
        f_layout.addRow(lbl_info_tag, self.mw.dep_info_label)

        # Thanh phân tách mảnh giữa thông tin tài khoản và form nạp tiền
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("formSep")
        f_layout.addRow(sep)

        # ── HÀNG 3: SỐ TIỀN NẠP
        lbl_amount = QLabel("Số tiền nạp: *")
        lbl_amount.setObjectName("formLabel")

        self.mw.dep_amount = QLineEdit()
        self.mw.dep_amount.setObjectName("formInput")
        self.mw.dep_amount.setPlaceholderText("Nhập số tiền cần nạp (VND)...")
        self.mw.dep_amount.setFixedHeight(36)
        f_layout.addRow(lbl_amount, self.mw.dep_amount)
        
        # ── HÀNG 4: MÃ PIN BẢO MẬT 
        lbl_pin = QLabel("Mã PIN: *")
        lbl_pin.setObjectName("formLabel")

        self.mw.dep_pin = QLineEdit()
        self.mw.dep_pin.setObjectName("formInput")
        self.mw.dep_pin.setEchoMode(QLineEdit.Password)
        self.mw.dep_pin.setPlaceholderText("Nhập mã PIN 6 số để xác thực...")
        self.mw.dep_pin.setMaxLength(6)
        self.mw.dep_pin.setFixedHeight(36)
        f_layout.addRow(lbl_pin, self.mw.dep_pin)

        # Nạp toàn bộ khối Panel Form vào giao diện chính
        layout.addWidget(form_w)


        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Nạp tiền")
        btn_submit.setObjectName("btnSuccess")
        btn_submit.setFixedHeight(38)
        btn_submit.clicked.connect(self._on_deposit)

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
        self.mw.dep_account_id.clear()
        self.mw.dep_amount.clear()
        self.mw.dep_pin.clear()
        self.mw.dep_info_label.clear()

    def _on_check(self):
        mw = self.mw
        account_id = mw.dep_account_id.text().strip()
        if not account_id:
            return
        try:
            acc = mw.bank.account_service.find_account(account_id)
            mw.dep_info_label.setText(
                f"Chủ TK: {acc.full_name} | Số dư: {acc.balance:,.0f} VND | "
                f"Trạng thái: {acc.status}"
            )
        except ValueError:
            mw.dep_info_label.setText("Không tìm thấy tài khoản!")

    def _on_deposit(self):
        mw = self.mw
        account_id = mw.dep_account_id.text().strip()
        amount_text = mw.dep_amount.text().strip()
        pin = mw.dep_pin.text().strip()

        if not account_id or not amount_text or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin!")
            return

        try:
            amount = float(amount_text)
            account, trans = mw.bank.deposit_money(account_id, amount, pin)
            msg = (f"Nạp {amount:,.0f} VND thành công!\n\n"
                   f"Số dư mới: {account.balance:,.0f} VND\n"
                   f"Mã GD: {trans.trans_id}")
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except ValueError as e:
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
                margin: 4px 0;
            }
            QStackedWidget#innerStack {
                background: transparent;
                border: none;
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

            /* ── Nút cập nhật chính ── */
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

            /* ── Nút phụ (Tra cứu, Làm mới) ── */
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