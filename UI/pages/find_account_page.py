from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTextEdit, QGroupBox, QFrame, QFormLayout
)

from PyQt5.QtCore import Qt

class FindPageAccount(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()
    def _build(self):
        # Khoi tao layout goc quan ly toan bo trang
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(14)

        # 2. PANEL TRA CỨU TÀI KHOẢN ─────────────────────────────────────────
        acc_frame = QFrame()
        acc_frame.setObjectName("searchPanel")

        acc_layout = QFormLayout(acc_frame)
        acc_layout.setContentsMargins(20, 18, 20, 18)
        acc_layout.setSpacing(12)
        acc_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl_aid = QLabel("Số tài khoản:")
        lbl_aid.setObjectName("searchLabel")
        self.mw.find_account_id = QLineEdit()
        self.mw.find_account_id.setObjectName("searchInput")
        self.mw.find_account_id.setPlaceholderText("Nhập số tài khoản cần tìm...")
        self.mw.find_account_id.setFixedHeight(36)
        # Bấm Enter tự động kích hoạt tìm kiếm
        self.mw.find_account_id.returnPressed.connect(self._on_find_account)

        acc_layout.addRow(lbl_aid, self.mw.find_account_id)

        # Nut bam
        btn_find_acc = QPushButton("Tìm tài khoản")
        btn_find_acc.setObjectName("btnPrimary")
        btn_find_acc.setFixedHeight(38)
        btn_find_acc.clicked.connect(self._on_find_account)

        acc_layout.addWidget(lbl_aid)
        acc_layout.addWidget(self.mw.find_account_id)
        acc_layout.addWidget(btn_find_acc)

        # Khung hiển thị kết quả tài khoản
        self.mw.find_account_result = QTextEdit()
        self.mw.find_account_result.setObjectName("searchResultBox")
        self.mw.find_account_result.setReadOnly(True)
        self.mw.find_account_result.setMaximumHeight(200)
        self.mw.find_account_result.setPlaceholderText("Thông tin chi tiết tài khoản sẽ hiển thị tại đây...")
        acc_layout.addWidget(self.mw.find_account_result)


        # Thêm toàn bộ dòng tra cứu song song này vào layout chính của trang
        root.addWidget(acc_frame)
        root.addStretch()


    def _on_find_account(self):
        mw = self.mw
        account_id = mw.find_account_id.text().strip()
        if not account_id:
            mw._show_error("Vui lòng nhập số tài khoản!")
            return
        try:
            acc = mw.bank.account_service.find_account(account_id)
            info = (
                f"Số TK: {acc.account_id}\n"
                f"Chủ TK: {acc.full_name}\n"
                f"Số dư: {acc.balance:,.0f} VND\n"
                f"Trạng thái: {acc.status}\n"
                f"Chi nhánh: {acc.create_at}\n"
                f"Ngày mở: {acc.time_created}"
            )
            mw.find_account_result.setText(info)
        except ValueError as e:
            mw.find_account_result.setText(f"Không tìm thấy: {str(e)}")

    def _apply_styles(self):
        self.setStyleSheet("""
            /* ── Panel Khung chứa ── */
            QFrame#searchPanel {
                background: #f8f9ff;
                border: 1px solid #c5cae9;
                border-radius: 10px;
            }
            QLabel#searchPanelTitle {
                font-size: 14px;
                font-weight: 700;
                color: #1a237e;
                padding-bottom: 2px;
            }
            QLabel#searchLabel {
                font-size: 13px;
                font-weight: 600;
                color: #37474f;
            }

            /* ── Ô nhập liệu QLineEdit ── */
            QLineEdit#searchInput {
                border: 1.5px solid #c5cae9;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 13px;
                background: white;
                color: #263238;
            }
            QLineEdit#searchInput:focus {
                border-color: #3f51b5;
                background: #fafbff;
            }

            /* ── Khung hiển thị kết quả QTextEdit ── */
            QTextEdit#searchResultBox {
                background: white;
                border: 1px solid #dde1f5;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                font-family: "Consolas", "Monospace", "Arial"; /* Đổi font chữ dạng Monospace cho thông tin ngay ngắn */
                color: #263238;
            }
        """)