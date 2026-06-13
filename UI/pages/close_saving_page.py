from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt


class CloseSavingPage(QWidget):
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

        self.mw.cls_saving_id = QLineEdit()
        self.mw.cls_saving_id.setObjectName("formInput")
        self.mw.cls_saving_id.setPlaceholderText("Nhập mã số sổ tiết kiệm cần tất toán...")
        self.mw.cls_saving_id.setFixedHeight(36)
        self.mw.cls_saving_id.returnPressed.connect(self._on_check)

        btn_check = QPushButton("Kiểm tra sổ")
        btn_check.setObjectName("btnNormal")
        btn_check.setFixedHeight(36)
        btn_check.clicked.connect(self._on_check)

        row_sid.addWidget(self.mw.cls_saving_id, 1)
        row_sid.addWidget(btn_check)

        lbl_sid_tag = QLabel("Mã sổ tiết kiệm: *")
        lbl_sid_tag.setObjectName("formLabel")
        f_layout.addRow(lbl_sid_tag, row_sid)

        # ── HÀNG 2: DỮ LIỆU ĐỐI CHIẾU SỔ TIẾT KIỆM ─────────────────
        lbl_info_tag = QLabel("Thông tin sổ:")
        lbl_info_tag.setObjectName("formLabel")

        self.mw.cls_info = QLabel("Chưa thực hiện kiểm tra")
        self.mw.cls_info.setStyleSheet("color: #1565c0; font-weight: bold; padding: 4px 0; font-size: 13px; line-height: 18px;")
        self.mw.cls_info.setWordWrap(True)
        f_layout.addRow(lbl_info_tag, self.mw.cls_info)

        # Thanh phân tách mảnh giữa phân khu thông tin sổ và xác thực bảo mật
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("formSep")
        f_layout.addRow(sep)


        # ── HÀNG 3: MÃ PIN GIAO DỊCH ────────────────────────────
        lbl_pin = QLabel("Mã PIN: *")
        lbl_pin.setObjectName("formLabel")
        self.mw.cls_pin = QLineEdit()
        self.mw.cls_pin.setEchoMode(QLineEdit.Password)
        self.mw.cls_pin.setMaxLength(6)
        self.mw.cls_pin.setPlaceholderText("Nhập mã PIN bảo mật 6 số...")
        f_layout.addRow(lbl_pin, self.mw.cls_pin)

        # Định dạng chiều cao và ObjectName cho các ô nhập bảo mật

        self.mw.cls_pin.setObjectName("formInput")
        self.mw.cls_pin.setFixedHeight(36)

        # Nạp toàn bộ khối Panel Form đã chuẩn hóa vào trang
        layout.addWidget(form_frame)

        # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Tất toán sổ")
        btn_submit.setObjectName("btnDanger") # Kế thừa màu đỏ rực cảnh báo hành động hủy/đóng quyền lợi tài khoản
        btn_submit.setFixedHeight(38)
        btn_submit.clicked.connect(self._on_close)

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
        """Reset sạch các ô thông tin nhập liệu"""
        self.mw.cls_saving_id.clear()
        self.mw.cls_pin.clear()
        self.mw.cls_info.setText("Chưa thực hiện kiểm tra")

    def _on_check(self):
        mw = self.mw
        saving_id = mw.cls_saving_id.text().strip()
        if not saving_id:
            mw._show_error("Vui lòng nhập mã sổ tiết kiệm trước khi kiểm tra!")
            return
        try:
            saving = mw.bank.saving_service.find_saving_account(saving_id)
            interest = mw.bank.saving_service.calculate_interest(saving_id)
            total = saving.amount + interest
            
            mw.cls_info.setText(
                f"• Chủ sổ tiết kiệm:  {saving.full_name}\n"
                f"• Số tiền gốc gửi:   {saving.amount:,.0f} VND\n"
                f"• Tiền lãi tích lũy: +{interest:,.0f} VND\n"
                f"• Tổng nhận thực tế: {total:,.0f} VND\n"
                f"• Trạng thái hiện tại: {saving.status}"
            )
        except ValueError as e:
            mw.cls_info.setText(f"Không tìm thấy thông tin: {str(e)}")

    def _on_close(self):
        mw = self.mw
        saving_id = mw.cls_saving_id.text().strip()
        pin = mw.cls_pin.text().strip()

        if not saving_id or not pin:
            mw._show_error("Vui lòng điền đầy đủ thông tin giao dịch bắt buộc (*)!")
            return

        try:
            # Thực thi nghiệp vụ rút toàn bộ tiền gốc + lãi, đóng sổ vĩnh viễn trên backend bank_service
            account, total = mw.bank.close_saving_account(saving_id, pin)
            account_id = account.account_id
            
            msg = (f"Hệ thống tất toán sổ tiết kiệm thành công!\n\n"
                   f"• Mã số đóng:     {saving_id}\n"
                   f"• Tổng tiền nhận:  {total:,.0f} VND (Gốc + Lãi)\n"
                   f"• Trích chuyển vào TK: {account_id}\n"
                   f"• Số dư mới của TK:   {account.balance:,.0f} VND")
            
            mw._show_success(msg)
            mw.bank.save_all_data()
            self._clear()
        except ValueError as e:
            mw._show_error(str(e))
        except Exception as e:
            mw._show_error(f"Lỗi hệ thống: {str(e)}")

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