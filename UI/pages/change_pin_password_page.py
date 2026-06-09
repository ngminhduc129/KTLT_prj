from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QHBoxLayout, QLabel, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt


class ChangeSecurityPage(QWidget):
    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()
        self._apply_styles()

    # ──────────────────────────────────────────────
    #  BUILD UI
    # ──────────────────────────────────────────────
    def _build(self):
        # 1. Layout gốc quản lý toàn trang
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(14)

        # 2. Khung Panel chính bao bọc toàn bộ form dữ liệu bảo mật
        form_frame = QFrame()
        form_frame.setObjectName("formPanel")
        
        f_layout = QFormLayout(form_frame)
        f_layout.setContentsMargins(20, 18, 20, 18)
        f_layout.setSpacing(12)
        f_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # ── HÀNG 1: USER ID ───────────────────────────────
        lbl_uid = QLabel("User ID: *")
        lbl_uid.setObjectName("formLabel")
        self.user_id_input = QLineEdit()
        self.user_id_input.setObjectName("formInput")
        self.user_id_input.setPlaceholderText("Nhập User ID để tra cứu tài khoản...")
        self.user_id_input.setFixedHeight(36)
        f_layout.addRow(lbl_uid, self.user_id_input)

        # ── HÀNG 2: TÀI KHOẢN + NÚT TÌM KIẾM ─────────────────
        lbl_acc = QLabel("Tài khoản: *")
        lbl_acc.setObjectName("formLabel")
        
        self.account_box = QComboBox()
        self.account_box.setObjectName("formInput")
        self.account_box.setFixedHeight(36)
        self.account_box.setPlaceholderText("Bấm 'Tìm tài khoản' để chọn...")

        btn_find = QPushButton("Tìm tài khoản")
        btn_find.setObjectName("btnNormal")
        btn_find.setFixedHeight(36)
        btn_find.clicked.connect(self._load_accounts)

        account_row = QHBoxLayout()
        account_row.setSpacing(8)
        account_row.addWidget(self.account_box, 1)
        account_row.addWidget(btn_find)
        f_layout.addRow(lbl_acc, account_row)

        # ── HÀNG 3: LỰA CHỌN CHỨC NĂNG ─────────────────────
        lbl_act = QLabel("Chức năng: *")
        lbl_act.setObjectName("formLabel")
        
        self.action_box = QComboBox()
        self.action_box.setObjectName("formInput")
        self.action_box.setFixedHeight(36)
        self.action_box.addItems(["Đổi mật khẩu", "Đổi mã PIN"])
        self.action_box.currentIndexChanged.connect(self._switch_form)
        f_layout.addRow(lbl_act, self.action_box)

        # Thanh phân tách mảnh trước khi chuyển sang vùng nội dung động (Stack)
        sep_stack = QFrame()
        sep_stack.setFrameShape(QFrame.HLine)
        sep_stack.setObjectName("formSep")
        f_layout.addRow(sep_stack)

        # ── KHU VỰC TRÁO ĐỔI FORM ĐỘNG (QStackedWidget) ──────
        self.stack = QStackedWidget()
        self.stack.setObjectName("innerStack")

        # -------------------------------------------------
        # PAGE ĐỔI MẬT KHẨU
        # -------------------------------------------------
        password_page = QWidget()
        password_layout = QFormLayout(password_page)
        password_layout.setContentsMargins(0, 0, 0, 0) # Triệt tiêu margin thừa của stack con
        password_layout.setSpacing(12)
        password_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl_new_pwd = QLabel("Mật khẩu mới: *")
        lbl_new_pwd.setObjectName("formLabel")
        self.new_password_input = QLineEdit()
        self.new_password_input.setObjectName("formInput")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setFixedHeight(36)
        password_layout.addRow(lbl_new_pwd, self.new_password_input)

        # -------------------------------------------------
        # PAGE ĐỔI MÃ PIN
        # -------------------------------------------------
        pin_page = QWidget()
        pin_layout = QFormLayout(pin_page)
        pin_layout.setContentsMargins(0, 0, 0, 0) # Triệt tiêu margin thừa của stack con
        pin_layout.setSpacing(12)
        pin_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        lbl_new_pin = QLabel("Mã PIN mới: *")
        lbl_new_pin.setObjectName("formLabel")
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setObjectName("formInput")
        self.new_pin_input.setEchoMode(QLineEdit.Password)
        self.new_pin_input.setMaxLength(6)
        self.new_pin_input.setFixedHeight(36)
        self.new_pin_input.setPlaceholderText("Tối đa 6 số")
        pin_layout.addRow(lbl_new_pin, self.new_pin_input)

        # Add các page động vào Stack điều hướng
        self.stack.addWidget(password_page)
        self.stack.addWidget(pin_page)
        
        # Thêm nguyên khối Stack thành một hàng trong QFormLayout cha
        f_layout.addRow(self.stack)

        # Nạp toàn bộ Panel Form đã đóng gói vào layout chính của trang
        layout.addWidget(form_frame)

        # ── DÒNG NÚT BẤM HÀNH ĐỘNG ĐÁY TRANG ──────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_update = QPushButton("Cập nhật")
        btn_update.setObjectName("btnPrimary")
        btn_update.setFixedHeight(38)
        btn_update.clicked.connect(self._on_update)

        btn_clear = QPushButton("Làm mới")
        btn_clear.setObjectName("btnNormal")
        btn_clear.setFixedHeight(38)
        btn_clear.clicked.connect(self._clear)

        btn_row.addStretch()
        btn_row.addWidget(btn_clear)
        btn_row.addWidget(btn_update)
        layout.addLayout(btn_row)

        layout.addStretch()

    # =====================================================
    # LOAD ACCOUNTS
    # =====================================================
    def _load_accounts(self):

        user_id = (
            self.user_id_input.text().strip()
        )

        if not user_id:

            self.mw._show_error(
                "Vui lòng nhập CCCD!"
            )

            return

        try:

            accounts = (
                self.mw.bank.account_service
                .get_accounts_by_user_id(user_id)
            )

            self.account_box.clear()

            current = accounts.head

            if current is None:

                raise ValueError(
                    "Không tìm thấy tài khoản!"
                )

            while current:

                account = current.value

                self.account_box.addItem(
                    account.account_id
                )

                current = current.next

            self.mw._show_success(
                "Tải danh sách tài khoản thành công!"
            )

        except Exception as e:

            self.mw._show_error(str(e))

    # =====================================================
    # SWITCH FORM
    # =====================================================
    def _switch_form(self, index):

        self.stack.setCurrentIndex(index)

    # =====================================================
    # CLEAR
    # =====================================================
    def _clear(self):

        self.user_id_input.clear()

        self.account_box.clear()

        self.new_password_input.clear()

        self.new_pin_input.clear()

        self.action_box.setCurrentIndex(0)

    # =====================================================
    # UPDATE
    # =====================================================
    def _on_update(self):
        mw = self.mw
        account_id = (
            self.account_box.currentText().strip()
        )

        if not account_id:

            self.mw._show_error(
                "Vui lòng chọn tài khoản!"
            )

            return

        try:

            account = (
                self.mw.bank.account_service
                .find_account(account_id)
            )

            action = (
                self.action_box.currentText()
            )

            # =============================================
            # CHANGE PASSWORD
            # =============================================
            if action == "Đổi mật khẩu":

                new_password = (
                    self.new_password_input
                    .text()
                    .strip()
                )

                account = mw.bank.account_service.change_password(account.account_id, new_password)

                self.mw._show_success(
                    "Đổi mật khẩu thành công!"
                )

            # =============================================
            # CHANGE PIN
            # =============================================
            else:

                new_pin = (
                    self.new_pin_input
                    .text()
                    .strip()
                )

                account = self.mw.bank.account_service.change_pin(account.account_id, new_pin)

                self.mw._show_success(
                    "Đổi mã PIN thành công!"
                )

            # SAVE
            self.mw.bank.save_all_data()

            self._clear()

        except Exception as e:

            self.mw._show_error(str(e))

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