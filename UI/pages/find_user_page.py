from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTextEdit, QGroupBox, QFrame, QFormLayout
)
from PyQt5.QtCore import Qt


class FindPageUser(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(14)

        user_frame = QFrame()
        user_frame.setObjectName("searchPanel")

        f_layout = QFormLayout(user_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl_uid = QLabel("User ID:")
        lbl_uid.setObjectName("searchLabel")
        self.mw.find_user_id = QLineEdit()
        self.mw.find_user_id.setObjectName("searchInput")
        self.mw.find_user_id.setPlaceholderText("Nhập User ID cần tìm...")
        self.mw.find_user_id.setFixedHeight(36)

        # Bấm Enter tự động kích hoạt tìm kiếm
        self.mw.find_user_id.returnPressed.connect(self._on_find_user)

        f_layout.addRow(lbl_uid, self.mw.find_user_id)

        btn_find_user = QPushButton("Tìm khách hàng")
        btn_find_user.setObjectName("btnPrimary")
        btn_find_user.setFixedHeight(38)
        btn_find_user.clicked.connect(self._on_find_user)

        f_layout.addWidget(lbl_uid)
        f_layout.addWidget(self.mw.find_user_id)
        f_layout.addWidget(btn_find_user)

        # Khung hiển thị kết quả (Dùng QTextEdit nhưng đã bọc CSS sạch sẽ)
        self.mw.find_user_result = QTextEdit()
        self.mw.find_user_result.setObjectName("searchResultBox")
        self.mw.find_user_result.setReadOnly(True)
        self.mw.find_user_result.setMaximumHeight(200)
        self.mw.find_user_result.setPlaceholderText("Thông tin chi tiết khách hàng sẽ hiển thị tại đây...")
        f_layout.addWidget(self.mw.find_user_result)

        root.addWidget(user_frame)
        root.addStretch()

    def _on_find_user(self):
        mw = self.mw
        user_id = mw.find_user_id.text().strip()
        if not user_id:
            mw._show_error("Vui lòng nhập User ID!")
            return
        try:
            user = mw.bank.user_service.find_user_by_id(user_id)
            info = (
                f"User ID: {user.user_id}\n"
                f"Họ tên: {user.full_name}\n"
                f"Số điện thoại: {user.phone}\n"
                f"Email: {user.email}\n"
                f"Giới tính: {user.sex}\n"
                f"Địa chỉ: {user.address}\n"
                f"Nghề nghiệp: {user.job}\n"
                f"Ngày sinh: {user.dob}"
            )
            mw.find_user_result.setText(info)
        except ValueError as e:
            mw.find_user_result.setText(f"Không tìm thấy: {str(e)}")

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