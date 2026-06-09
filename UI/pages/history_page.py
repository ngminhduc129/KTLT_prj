# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
#     QPushButton, QLabel, QTableWidget, QTableWidgetItem,
#     QHeaderView, QAbstractItemView
# )
# from PyQt5.QtGui import QBrush, QColor


# class HistoryPage(QWidget):
#     def __init__(self, mw):
#         super().__init__()
#         self.mw = mw
#         self._build()

#     def _build(self):
#         layout = QVBoxLayout(self)

#         filter_row = QHBoxLayout()
#         self.mw.hist_account_id = QLineEdit()
#         self.mw.hist_account_id.setPlaceholderText("Nhập số tài khoản")
#         btn_load = QPushButton("Xem lịch sử")
#         btn_load.setObjectName("btnPrimary")
#         btn_load.clicked.connect(self._on_load)
#         btn_all = QPushButton("Tất cả")
#         btn_all.setObjectName("btnNormal")
#         btn_all.clicked.connect(self._on_load_all)
#         filter_row.addWidget(QLabel("Tài khoản:"))
#         filter_row.addWidget(self.mw.hist_account_id)
#         filter_row.addWidget(btn_load)
#         filter_row.addWidget(btn_all)
#         filter_row.addStretch()
#         layout.addLayout(filter_row)

#         self.mw.hist_table = QTableWidget()
#         self.mw.hist_table.setColumnCount(7)
#         self.mw.hist_table.setHorizontalHeaderLabels([
#             "Mã GD", "TK nguồn", "TK đích", "Loại",
#             "Số tiền", "Thời gian", "Số dư sau GD"
#         ])
#         self.mw.hist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         self.mw.hist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.mw.hist_table.horizontalHeader().setStretchLastSection(True)
#         self.mw.hist_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         layout.addWidget(self.mw.hist_table)

#         self.mw.hist_count = QLabel()
#         self.mw.hist_count.setStyleSheet("color: #757575;")
#         layout.addWidget(self.mw.hist_count)

#     def _populate(self, account_id=None):
#         mw = self.mw
#         mw.hist_table.setRowCount(0)
#         count = 0

#         try:
#             node = mw.bank.transaction_service.trans_storage.head
#             while node is not None:
#                 trans = node.value
#                 if account_id and trans.from_account != account_id and trans.to_account != account_id:
#                     node = node.next
#                     continue
#                 row = mw.hist_table.rowCount()
#                 mw.hist_table.insertRow(row)
#                 mw.hist_table.setItem(row, 0, QTableWidgetItem(str(trans.trans_id)))
#                 mw.hist_table.setItem(row, 1, QTableWidgetItem(trans.from_account or "-"))
#                 mw.hist_table.setItem(row, 2, QTableWidgetItem(trans.to_account or "-"))
#                 mw.hist_table.setItem(row, 3, QTableWidgetItem(trans.type_trans))
#                 amount_text = f"{trans.amount:,.0f} VND"
#                 item_amount = QTableWidgetItem(amount_text)
#                 if trans.type_trans in ("Deposit", "Receive", "Interest", "Settlement"):
#                     item_amount.setForeground(QBrush(QColor("#2e7d32")))
#                 else:
#                     item_amount.setForeground(QBrush(QColor("#c62828")))
#                 mw.hist_table.setItem(row, 4, item_amount)
#                 mw.hist_table.setItem(row, 5, QTableWidgetItem(trans.timestamp or "-"))
#                 mw.hist_table.setItem(row, 6, QTableWidgetItem(f"{trans.balance_after:,.0f} VND"))
#                 count += 1
#                 node = node.next
#         except Exception:
#             pass

#         if account_id:
#             mw.hist_count.setText(f"Tổng số giao dịch của {account_id}: {count}")
#         else:
#             mw.hist_count.setText(f"Tổng số giao dịch: {count}")

#     def _on_load(self):
#         account_id = self.mw.hist_account_id.text().strip()
#         if account_id:
#             self._populate(account_id)
#         else:
#             self.mw._show_error("Vui lòng nhập số tài khoản!")

#     def _on_load_all(self):
#         self.mw.hist_account_id.clear()
#         self._populate()

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QFrame, QSizePolicy
)
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QDate


class HistoryPage(QWidget):
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


        # ── Panel bộ lọc ───────────────────────────
        filter_frame = QFrame()
        filter_frame.setObjectName("filterPanel")
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 14, 16, 14)
        filter_layout.setSpacing(10)

        # Dòng 1: Tài khoản
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        lbl_acc = QLabel("Tài khoản:")
        lbl_acc.setObjectName("filterLabel")
        lbl_acc.setFixedWidth(80)

        self.mw.hist_account_id = QLineEdit()
        self.mw.hist_account_id.setObjectName("filterInput")
        self.mw.hist_account_id.setPlaceholderText("Nhập số tài khoản (để trống = tất cả)")
        self.mw.hist_account_id.setFixedHeight(36)
        # Enter để tìm kiếm
        self.mw.hist_account_id.returnPressed.connect(self._on_search)

        row1.addWidget(lbl_acc)
        row1.addWidget(self.mw.hist_account_id, 1)
        filter_layout.addLayout(row1)

        # Separator mảnh
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("filterSep")
        filter_layout.addWidget(sep)

        # Dòng 2: Khoảng ngày + nút
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        lbl_date = QLabel("Khoảng ngày:")
        lbl_date.setObjectName("filterLabel")
        lbl_date.setFixedWidth(90)

        self._from_date = QLineEdit()
        self._from_date.setObjectName("filterInput")
        self._from_date.setPlaceholderText("Từ ngày  dd/mm/yyyy")
        self._from_date.setFixedHeight(36)
        self._from_date.setFixedWidth(170)

        lbl_to = QLabel("→")
        lbl_to.setObjectName("arrowLabel")
        lbl_to.setAlignment(Qt.AlignCenter)

        self._to_date = QLineEdit()
        self._to_date.setObjectName("filterInput")
        self._to_date.setPlaceholderText("Đến ngày  dd/mm/yyyy")
        self._to_date.setFixedHeight(36)
        self._to_date.setFixedWidth(170)

        # Nút "Hôm nay"
        btn_today = QPushButton("Hôm nay")
        btn_today.setObjectName("btnQuick")
        btn_today.setFixedHeight(36)
        btn_today.clicked.connect(self._set_today)

        # Nút "7 ngày qua"
        btn_7d = QPushButton("7 ngày qua")
        btn_7d.setObjectName("btnQuick")
        btn_7d.setFixedHeight(36)
        btn_7d.clicked.connect(self._set_last7)

        # Nút "Tháng này"
        btn_month = QPushButton("Tháng này")
        btn_month.setObjectName("btnQuick")
        btn_month.setFixedHeight(36)
        btn_month.clicked.connect(self._set_this_month)

        row2.addWidget(lbl_date)
        row2.addWidget(self._from_date)
        row2.addWidget(lbl_to)
        row2.addWidget(self._to_date)
        row2.addWidget(btn_today)
        row2.addWidget(btn_7d)
        row2.addWidget(btn_month)
        row2.addStretch()
        filter_layout.addLayout(row2)

        # Dòng 3: Nút hành động
        row3 = QHBoxLayout()
        row3.setSpacing(8)

        btn_search = QPushButton("Tìm kiếm")
        btn_search.setObjectName("btnPrimary")
        btn_search.setFixedHeight(38)
        btn_search.clicked.connect(self._on_search)

        btn_all = QPushButton("Xem tất cả")
        btn_all.setObjectName("btnNormal")
        btn_all.setFixedHeight(38)
        btn_all.clicked.connect(self._on_load_all)

        btn_clear = QPushButton("Xóa bộ lọc")
        btn_clear.setObjectName("btnDanger")
        btn_clear.setFixedHeight(38)
        btn_clear.clicked.connect(self._on_clear_filter)

        row3.addStretch()
        row3.addWidget(btn_clear)
        row3.addWidget(btn_all)
        row3.addWidget(btn_search)
        filter_layout.addLayout(row3)

        root.addWidget(filter_frame)

        # ── Bảng dữ liệu ───────────────────────────
        self.mw.hist_table = QTableWidget()
        self.mw.hist_table.setObjectName("histTable")
        self.mw.hist_table.setColumnCount(7)
        self.mw.hist_table.setHorizontalHeaderLabels([
            "Mã GD", "TK nguồn", "TK đích", "Loại GD",
            "Số tiền", "Thời gian", "Số dư sau GD"
        ])
        self.mw.hist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mw.hist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.mw.hist_table.setAlternatingRowColors(True)
        self.mw.hist_table.verticalHeader().setVisible(False)
        self.mw.hist_table.horizontalHeader().setStretchLastSection(True)
        self.mw.hist_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mw.hist_table.setSortingEnabled(True)
        root.addWidget(self.mw.hist_table)

        # ── Thanh trạng thái ───────────────────────
        status_row = QHBoxLayout()
        self.mw.hist_count = QLabel("Chưa tải dữ liệu")
        self.mw.hist_count.setObjectName("statusLabel")
        self._lbl_filter_info = QLabel("")
        self._lbl_filter_info.setObjectName("filterInfo")
        self._lbl_filter_info.setAlignment(Qt.AlignRight)
        status_row.addWidget(self.mw.hist_count)
        status_row.addStretch()
        status_row.addWidget(self._lbl_filter_info)
        root.addLayout(status_row)

    # ──────────────────────────────────────────────
    #  QUICK DATE SHORTCUTS
    # ──────────────────────────────────────────────
    def _set_today(self):
        today = QDate.currentDate().toString("dd/MM/yyyy")
        self._from_date.setText(today)
        self._to_date.setText(today)

    def _set_last7(self):
        today = QDate.currentDate()
        self._from_date.setText(today.addDays(-6).toString("dd/MM/yyyy"))
        self._to_date.setText(today.toString("dd/MM/yyyy"))

    def _set_this_month(self):
        today = QDate.currentDate()
        first = QDate(today.year(), today.month(), 1)
        self._from_date.setText(first.toString("dd/MM/yyyy"))
        self._to_date.setText(today.toString("dd/MM/yyyy"))

    # ──────────────────────────────────────────────
    #  POPULATE TABLE
    # ──────────────────────────────────────────────
    def _populate(self, account_id=None, from_date=None, to_date=None):
        """
        Nạp dữ liệu vào bảng.
        - Nếu có from_date / to_date → gọi get_transactions_by_date (có lọc ngày)
        - Nếu không có ngày       → gọi get_transactions_by_account (không lọc ngày)
        """
        mw = self.mw
        mw.hist_table.setSortingEnabled(False)   # Tắt sort tạm thời để tránh crash khi insert
        mw.hist_table.setRowCount(0)
        count = 0

        try:
            use_date_filter = bool(from_date or to_date)

            if use_date_filter:
                # BUG FIX: dùng đúng hàm có lọc ngày
                filtered_linked_list = mw.bank.transaction_service.get_transactions_by_date(
                    account_id=account_id,
                    start_date_str=from_date,
                    end_date_str=to_date
                )
            else:
                filtered_linked_list = mw.bank.transaction_service.get_transactions_by_account(
                    account_id
                )

            node = filtered_linked_list.head
            while node is not None:
                trans = node.value
                row = mw.hist_table.rowCount()
                mw.hist_table.insertRow(row)

                # Mã GD (căn giữa)
                item_id = QTableWidgetItem(str(trans.trans_id))
                item_id.setTextAlignment(Qt.AlignCenter)
                mw.hist_table.setItem(row, 0, item_id)

                mw.hist_table.setItem(row, 1, QTableWidgetItem(trans.from_account or "—"))
                mw.hist_table.setItem(row, 2, QTableWidgetItem(trans.to_account or "—"))

                # Badge loại giao dịch
                item_type = QTableWidgetItem(trans.type_trans)
                item_type.setTextAlignment(Qt.AlignCenter)
                mw.hist_table.setItem(row, 3, item_type)

                # Số tiền + màu sắc
                amount_text = f"{trans.amount:,.0f} ₫"
                item_amount = QTableWidgetItem(amount_text)
                item_amount.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                INCOME_TYPES = {"Deposit", "Receive", "Interest", "Settlement"}
                if trans.type_trans in INCOME_TYPES:
                    item_amount.setForeground(QBrush(QColor("#1b7a3e")))  # Xanh lá đậm
                    item_amount.setText(f"+{amount_text}")
                else:
                    item_amount.setForeground(QBrush(QColor("#c0392b")))  # Đỏ

                mw.hist_table.setItem(row, 4, item_amount)

                # Thời gian
                ts = str(trans.timestamp) if trans.timestamp and str(trans.timestamp).strip() != "None" else "—"
                mw.hist_table.setItem(row, 5, QTableWidgetItem(ts))

                # Số dư sau GD (căn phải)
                item_bal = QTableWidgetItem(f"{trans.balance_after:,.0f} ₫")
                item_bal.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                mw.hist_table.setItem(row, 6, item_bal)

                count += 1
                node = node.next

        except Exception as e:
            print(f"[HistoryPage] Lỗi hiển thị dữ liệu: {e}")

        mw.hist_table.setSortingEnabled(True)   # Bật lại sort sau khi insert xong

        # Cập nhật status bar
        acc_info = f"tài khoản {account_id}" if account_id else "tất cả tài khoản"
        mw.hist_count.setText(f"Tìm thấy  {count}  giao dịch  ({acc_info})")

        # Hiển thị thông tin bộ lọc ngày nếu có
        if from_date or to_date:
            f = from_date or "..."
            t = to_date or "..."
            self._lbl_filter_info.setText(f"  {f}  →  {t}")
        else:
            self._lbl_filter_info.setText("")

    # ──────────────────────────────────────────────
    #  BUTTON HANDLERS
    # ──────────────────────────────────────────────
    def _on_search(self):
        account_id = self.mw.hist_account_id.text().strip() or None
        from_date  = self._from_date.text().strip() or None
        to_date    = self._to_date.text().strip()   or None
        self._populate(account_id=account_id, from_date=from_date, to_date=to_date)

    def _on_load_all(self):
        """Xem tất cả, GIỮ nguyên bộ lọc ngày đang nhập."""
        self.mw.hist_account_id.clear()
        from_date = self._from_date.text().strip() or None
        to_date   = self._to_date.text().strip()   or None
        self._populate(account_id=None, from_date=from_date, to_date=to_date)

    def _on_clear_filter(self):
        """Xóa toàn bộ bộ lọc và tải lại tất cả."""
        self.mw.hist_account_id.clear()
        self._from_date.clear()
        self._to_date.clear()
        self._populate()

    # ──────────────────────────────────────────────
    #  AUTO REFRESH KHI HIỂN THỊ TAB
    # ──────────────────────────────────────────────
    def showEvent(self, event):
        """
        BUG FIX: Khi chuyển sang tab, GIỮ nguyên các bộ lọc đã nhập
        thay vì reset hoàn toàn như trước.
        """
        super().showEvent(event)
        account_id = self.mw.hist_account_id.text().strip() or None
        from_date  = self._from_date.text().strip() or None
        to_date    = self._to_date.text().strip()   or None
        self._populate(account_id=account_id, from_date=from_date, to_date=to_date)

    # ──────────────────────────────────────────────
    #  STYLES
    # ──────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""


            /* ── Panel bộ lọc ── */
            QFrame#filterPanel {
                background: #f8f9ff;
                border: 1px solid #c5cae9;
                border-radius: 10px;
            }
            QLabel#filterLabel {
                font-size: 13px;
                font-weight: 600;
                color: #37474f;
            }
            QLabel#arrowLabel {
                font-size: 16px;
                color: #7986cb;
                font-weight: bold;
            }
            QLabel#filterInfo {
                font-size: 12px;
                color: #5c6bc0;
                font-style: italic;
            }
            QFrame#filterSep {
                color: #dde1f5;
                margin: 0 0;
            }

            /* ── Inputs ── */
            QLineEdit#filterInput {
                border: 1.5px solid #c5cae9;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 13px;
                background: white;
                color: #263238;
            }
            QLineEdit#filterInput:focus {
                border-color: #3f51b5;
                background: #fafbff;
            }

            /* ── Nút chính ── */
            QPushButton#btnPrimary {
                background: #3f51b5;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 0 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#btnPrimary:hover  { background: #303f9f; }
            QPushButton#btnPrimary:pressed{ background: #283593; }

            /* ── Nút phụ ── */
            QPushButton#btnNormal {
                background: #eceff1;
                color: #37474f;
                border: 1px solid #cfd8dc;
                border-radius: 7px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#btnNormal:hover { background: #e0e0e0; }

            /* ── Nút xóa ── */
            QPushButton#btnDanger {
                background: white;
                color: #e53935;
                border: 1.5px solid #ef9a9a;
                border-radius: 7px;
                padding: 0 14px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#btnDanger:hover { background: #ffebee; }

            /* ── Nút shortcut ngày ── */
            QPushButton#btnQuick {
                background: #e8eaf6;
                color: #3949ab;
                border: 1px solid #c5cae9;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton#btnQuick:hover { background: #c5cae9; }

            /* ── Bảng ── */
            QTableWidget#histTable {
                border: 1px solid #dde1f5;
                border-radius: 8px;
                gridline-color: #eef0fa;
                font-size: 13px;
                background: white;
                alternate-background-color: #f5f6ff;
                selection-background-color: #e8eaf6;
                selection-color: #1a237e;
            }
            QTableWidget#histTable::item {
                padding: 6px 8px;
                color: #263238;
            }
            QHeaderView::section {
                background: #3f51b5;
                color: white;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 6px;
                border: none;
                border-right: 1px solid #5c6bc0;
            }
            QHeaderView::section:last {
                border-right: none;
            }

            /* ── Status ── */
            QLabel#statusLabel {
                font-size: 12px;
                color: #546e7a;
                padding: 2px 0;
            }
        """)