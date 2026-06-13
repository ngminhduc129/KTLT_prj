from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt


class SavingPage(QWidget):
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

        # Khởi tạo các ô nhập thông tin
        self.mw.sav_account_id = QLineEdit()
        self.mw.sav_account_id.setPlaceholderText("Nhập số tài khoản trích tiền gửi...")

        self.mw.sav_amount = QLineEdit()
        self.mw.sav_amount.setPlaceholderText("Nhập số tiền muốn gửi tiết kiệm (VND)...")

        # Chuẩn hóa chiều cao và ObjectName cho các ô nhập liệu
        for widget in [self.mw.sav_account_id, self.mw.sav_amount]:
            widget.setObjectName("formInput")
            widget.setFixedHeight(36)

        # Tạo các nhãn bên cột trái định dạng chuẩn CSS
        lbl_acc = QLabel("Tài khoản nhận: *")
        lbl_amt = QLabel("Số tiền gửi: *")
        
        lbl_acc.setObjectName("formLabel")
        lbl_amt.setObjectName("formLabel")

        # Đẩy các hàng vào QFormLayout
        f_layout.addRow(lbl_acc, self.mw.sav_account_id)
        f_layout.addRow(lbl_amt, self.mw.sav_amount)

        # Hàng hiển thị khối kết quả chi tiết sau khi tạo sổ
        lbl_res_tag = QLabel("Kết quả xử lý:")
        lbl_res_tag.setObjectName("formLabel")

        self.mw.sav_result = QLabel("Chưa thực hiện giao dịch")
        self.mw.sav_result.setStyleSheet("color: #1565c0; font-weight: bold; padding: 4px 0; font-size: 13px;")
        self.mw.sav_result.setWordWrap(True)
        f_layout.addRow(lbl_res_tag, self.mw.sav_result)

        # Nạp toàn bộ khối Panel Form vào giao diện chính của trang
        layout.addWidget(form_frame)

        # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_submit = QPushButton("Gửi tiết kiệm")
        btn_submit.setObjectName("btnSuccess") 
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

    # ──────────────────────────────────────────────
    #  LOGIC METHODS
    # ──────────────────────────────────────────────
    def _clear(self):
        self.mw.sav_account_id.clear()
        self.mw.sav_amount.clear()
        self.mw.sav_result.setText("Chưa thực hiện giao dịch") 

    def _on_create(self):
        mw = self.mw
        account_id = mw.sav_account_id.text().strip()
        amount_text = mw.sav_amount.text().strip()

        if not account_id or not amount_text:
            mw._show_error("Vui lòng điền đầy đủ các thông tin bắt buộc (*)!")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                mw._show_error("Số tiền trích gửi tiết kiệm phải lớn hơn 0 ₫!")
                return
        except ValueError:
            mw._show_error("Số tiền nhập vào không hợp lệ! Vui lòng chỉ dùng ký tự số liền nhau.")
            return

        try:
            saving = mw.bank.create_saving(account_id, amount)
            msg = (f"THÔNG TIN SỔ TIẾT KIỆM PHÁT HÀNH:\n\n"
                   f"• Mã sổ: {saving.saving_id}\n"
                   f"• Khách hàng: {saving.full_name} ({saving.user_id})\n"
                   f"• Số tiền gửi: {saving.amount:,.0f} VND\n"
                   f"• Kỳ hạn áp dụng: {saving.term}\n"
                   f"• Ngày mở sổ: {saving.start_date}\n"
                   f"• Trạng thái sổ: {saving.status}")
            
            mw.sav_result.setText(msg)
            mw._show_success("Hệ thống đã khởi tạo sổ tiết kiệm thành công!")
            mw.bank.save_all_data()
            
            # Chỉ làm mới ô nhập liệu, giữ lại nhãn thông tin hóa đơn cho người dùng đối chiếu
            self.mw.sav_account_id.clear()
            self.mw.sav_amount.clear()
            
        except ValueError as e:
            mw._show_error(str(e))
        except TypeError as e:
            mw._show_error(f"Lỗi liên kết dữ liệu hệ thống: {str(e)}")

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