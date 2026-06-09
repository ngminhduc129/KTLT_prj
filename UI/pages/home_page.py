from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont



FEATURES = [
    ("Quản lý khách hàng",   "Thêm, sửa, xóa user",          "#E6F1FB", "#185FA5"),
    ("Tài khoản ngân hàng",  "Mở, đóng tài khoản",           "#E1F5EE", "#0F6E56"),
    ("Giao dịch",            "Nạp, rút, chuyển khoản",       "#FAEEDA", "#854F0B"),
    ("Sổ tiết kiệm",         "Tạo & quản lý tiết kiệm",      "#EAF3DE", "#3B6D11"),
    ("Lịch sử giao dịch",    "Tìm kiếm theo ngày",           "#EEEDFE", "#534AB7"),
    ("Tra cứu tài khoản",    "Tìm theo số TK / tên",         "#FAECE7", "#993C1D"),
    ("Cập nhật thông tin",   "Hồ sơ khách hàng",             "#FBEAF0", "#993556"),
    ("Bảo mật",              "Đổi mật khẩu & PIN",          "#F1EFE8", "#5F5E5A"),
]


class FeatureCard(QFrame):
    """Card hiển thị một chức năng"""

    def __init__(self, title, subtitle, bg_color, text_color):
        super().__init__()
        self.setObjectName("featureCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18) 
        layout.setSpacing(6)

        # Tiêu đề chức năng
        lbl_title = QLabel(title)
        lbl_title.setObjectName("cardTitle")
        lbl_title.setWordWrap(True)
        layout.addWidget(lbl_title)

        # Mô tả chức năng
        lbl_sub = QLabel(subtitle)
        lbl_sub.setObjectName("cardSub")
        lbl_sub.setWordWrap(True)
        layout.addWidget(lbl_sub)

        # Áp dụng màu nền (bg_color) và màu chữ riêng (text_color) cho từng Card
        self.setStyleSheet(f"""
            QFrame#featureCard {{
                background: white;
                border: 0.5px solid #e0e0e0;
                border-radius: 12px;
            }}
            QFrame#featureCard:hover {{
                border-color: {text_color};
                background: {bg_color}; /* Đổi màu nền nhẹ khi hover chuột vào card */
            }}
            QLabel#cardTitle {{
                font-size: 14px;
                font-weight: 600;
                color: {text_color};
            }}
            QLabel#cardSub {{
                font-size: 12px;
                color: #757575;
            }}
        """)


class StatCard(QFrame):
    """Card hiển thị số liệu thống kê hệ thống."""

    def __init__(self, label, value="—"):
        super().__init__()
        self.setObjectName("statCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setObjectName("statLabel")
        self.val = QLabel(value)
        self.val.setObjectName("statValue")
        layout.addWidget(lbl)
        layout.addWidget(self.val)

    def set_value(self, v):
        self.val.setText(str(v))


class HomePage(QWidget):
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
        root.setContentsMargins(28, 24, 28, 20)
        root.setSpacing(0)

        # ── Tiêu đề chính hệ thống ───────────────────
        eyebrow = QLabel("HỆ THỐNG QUẢN TRỊ NGÂN HÀNG")
        eyebrow.setObjectName("eyebrow")

        title = QLabel("Chào mừng đến với <span style='color:#185FA5;'>Ngân hàng DBC</span>")
        title.setObjectName("heroTitle")
        title.setTextFormat(Qt.RichText)

        subtitle = QLabel("Chọn chức năng từ menu bên trái để bắt đầu quản lý nghiệp vụ.")
        subtitle.setObjectName("heroSub")

        root.addWidget(eyebrow)
        root.addSpacing(6)
        root.addWidget(title)
        root.addSpacing(4)
        root.addWidget(subtitle)
        root.addSpacing(24)

        # ── Khối thẻ thống kê số liệu ─────────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        self._stat_users    = StatCard("Tổng số khách hàng")
        self._stat_accounts = StatCard("Tài khoản đang mở")
        self._stat_trans    = StatCard("Giao dịch hệ thống")
        self._stat_savings  = StatCard("Sổ tiết kiệm phát hành")

        for card in (self._stat_users, self._stat_accounts,
                     self._stat_trans, self._stat_savings):
            stats_row.addWidget(card)

        root.addLayout(stats_row)
        root.addSpacing(24)

        # ── Thanh gạch phân tách ──────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setObjectName("divider")
        root.addWidget(div)
        root.addSpacing(20)

        # ── Tiêu đề danh mục chức năng ────────────────
        lbl_section = QLabel("DANH MỤC CHỨC NĂNG HỆ THỐNG")
        lbl_section.setObjectName("sectionLabel")
        root.addWidget(lbl_section)
        root.addSpacing(12)

        # ── Lưới thẻ chức năng (Grid 4 cột) ───────────
        grid = QGridLayout()
        grid.setSpacing(12)
    
        for i, (title_f, sub, bg, fg) in enumerate(FEATURES):
            card = FeatureCard(title_f, sub, bg, fg)
            grid.addWidget(card, i // 4, i % 4)

        root.addLayout(grid)
        root.addStretch()

    # ──────────────────────────────────────────────
    #  LOGIC: Đọc dữ liệu tự động từ Backend
    # ──────────────────────────────────────────────
    def refresh_stats(self):
        """Đọc dữ liệu an toàn từ lớp lưu trữ và cập nhật lên màn hình chính"""
        try:
            bank = self.mw.bank
            num_users    = len(bank.customers) if hasattr(bank, "customers") else "—"
            num_accounts = len(bank.accounts)  if hasattr(bank, "accounts")  else "—"
            num_trans    = bank.transaction_service.trans_storage.size() \
                           if hasattr(bank, "transaction_service") else "—"
            num_savings  = len(bank.savings)   if hasattr(bank, "savings")   else "—"

            self._stat_users.set_value(num_users)
            self._stat_accounts.set_value(num_accounts)
            self._stat_trans.set_value(num_trans)
            self._stat_savings.set_value(num_savings)
        except Exception:
            pass

    # ──────────────────────────────────────────────
    #  STYLESHEET CSS GLOBAL
    # ──────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            /* Hero Section */
            QLabel#eyebrow {
                font-size: 11px;
                font-weight: 600;
                color: #9e9e9e;
                letter-spacing: 1.5px;
            }
            QLabel#heroTitle {
                font-size: 24px;
                font-weight: 700;
                color: #212121;
            }
            QLabel#heroSub {
                font-size: 14px;
                color: #616161;
            }

            /* Thẻ thống kê */
            QFrame#statCard {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 10px;
            }
            QLabel#statLabel {
                font-size: 12px;
                font-weight: 500;
                color: #6c757d;
            }
            QLabel#statValue {
                font-size: 24px;
                font-weight: 700;
                color: #1a237e;
            }

            /* Thanh gạch ngăn cách */
            QFrame#divider {
                color: #e0e0e0;
                margin: 0;
            }

            /* Nhãn phân khu */
            QLabel#sectionLabel {
                font-size: 11px;
                font-weight: 700;
                color: #9e9e9e;
                letter-spacing: 1.5px;
            }
        """)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_stats()