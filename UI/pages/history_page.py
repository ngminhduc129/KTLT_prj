from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QBrush, QColor


class HistoryPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        filter_row = QHBoxLayout()
        self.mw.hist_account_id = QLineEdit()
        self.mw.hist_account_id.setPlaceholderText("Nhập số tài khoản")
        btn_load = QPushButton("Xem lịch sử")
        btn_load.setObjectName("btnPrimary")
        btn_load.clicked.connect(self._on_load)
        btn_all = QPushButton("Tất cả")
        btn_all.setObjectName("btnNormal")
        btn_all.clicked.connect(self._on_load_all)
        filter_row.addWidget(QLabel("Tài khoản:"))
        filter_row.addWidget(self.mw.hist_account_id)
        filter_row.addWidget(btn_load)
        filter_row.addWidget(btn_all)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        self.mw.hist_table = QTableWidget()
        self.mw.hist_table.setColumnCount(7)
        self.mw.hist_table.setHorizontalHeaderLabels([
            "Mã GD", "TK nguồn", "TK đích", "Loại",
            "Số tiền", "Thời gian", "Số dư sau GD"
        ])
        self.mw.hist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mw.hist_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.mw.hist_table.horizontalHeader().setStretchLastSection(True)
        self.mw.hist_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.mw.hist_table)

        self.mw.hist_count = QLabel()
        self.mw.hist_count.setStyleSheet("color: #757575;")
        layout.addWidget(self.mw.hist_count)

    def _populate(self, account_id=None):
        mw = self.mw
        mw.hist_table.setRowCount(0)
        count = 0

        try:
            node = mw.bank.transaction_service.trans_storage.head
            while node is not None:
                trans = node.value
                if account_id and trans.from_account != account_id and trans.to_account != account_id:
                    node = node.next
                    continue
                row = mw.hist_table.rowCount()
                mw.hist_table.insertRow(row)
                mw.hist_table.setItem(row, 0, QTableWidgetItem(str(trans.trans_id)))
                mw.hist_table.setItem(row, 1, QTableWidgetItem(trans.from_account or "-"))
                mw.hist_table.setItem(row, 2, QTableWidgetItem(trans.to_account or "-"))
                mw.hist_table.setItem(row, 3, QTableWidgetItem(trans.type_trans))
                amount_text = f"{trans.amount:,.0f} VND"
                item_amount = QTableWidgetItem(amount_text)
                if trans.type_trans in ("Deposit", "Receive", "Interest", "Settlement"):
                    item_amount.setForeground(QBrush(QColor("#2e7d32")))
                else:
                    item_amount.setForeground(QBrush(QColor("#c62828")))
                mw.hist_table.setItem(row, 4, item_amount)
                mw.hist_table.setItem(row, 5, QTableWidgetItem(trans.timestamp or "-"))
                mw.hist_table.setItem(row, 6, QTableWidgetItem(f"{trans.balance_after:,.0f} VND"))
                count += 1
                node = node.next
        except Exception:
            pass

        if account_id:
            mw.hist_count.setText(f"Tổng số giao dịch của {account_id}: {count}")
        else:
            mw.hist_count.setText(f"Tổng số giao dịch: {count}")

    def _on_load(self):
        account_id = self.mw.hist_account_id.text().strip()
        if account_id:
            self._populate(account_id)
        else:
            self.mw._show_error("Vui lòng nhập số tài khoản!")

    def _on_load_all(self):
        self.mw.hist_account_id.clear()
        self._populate()
