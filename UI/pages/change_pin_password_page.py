from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton,
    QHBoxLayout, QComboBox,
    QStackedWidget
)


class ChangeSecurityPage(QWidget):

    def __init__(self, mw):
        super().__init__()
        self.mw = mw
        self._build()

    def _build(self):

        layout = QVBoxLayout(self)

        # =================================================
        # FORM
        # =================================================
        form_w = QWidget()

        f_layout = QFormLayout(form_w)
        f_layout.setSpacing(10)

        # USER ID
        self.user_id_input = QLineEdit()

        # ACCOUNT BOX
        self.account_box = QComboBox()

        btn_find = QPushButton(
            "Tìm tài khoản"
        )

        btn_find.setObjectName(
            "btnNormal"
        )

        btn_find.clicked.connect(
            self._load_accounts
        )

        account_row = QHBoxLayout()

        account_row.addWidget(
            self.account_box
        )

        account_row.addWidget(
            btn_find
        )

        # ACTION
        self.action_box = QComboBox()

        self.action_box.addItems([
            "Đổi mật khẩu",
            "Đổi mã PIN"
        ])

        self.action_box.currentIndexChanged.connect(
            self._switch_form
        )

        # FORM LAYOUT
        f_layout.addRow(
            "Mã khách hàng (CCCD):",
            self.user_id_input
        )

        f_layout.addRow(
            "Tài khoản:",
            account_row
        )

        f_layout.addRow(
            "Chức năng:",
            self.action_box
        )

        # =================================================
        # STACK
        # =================================================
        self.stack = QStackedWidget()

        # -------------------------------------------------
        # PASSWORD PAGE
        # -------------------------------------------------
        password_page = QWidget()

        password_layout = QFormLayout(
            password_page
        )

        self.new_password_input = QLineEdit()

        self.new_password_input.setEchoMode(
            QLineEdit.Password
        )

        password_layout.addRow(
            "Mật khẩu mới:",
            self.new_password_input
        )

        # -------------------------------------------------
        # PIN PAGE
        # -------------------------------------------------
        pin_page = QWidget()

        pin_layout = QFormLayout(pin_page)

        self.new_pin_input = QLineEdit()

        self.new_pin_input.setEchoMode(
            QLineEdit.Password
        )

        self.new_pin_input.setMaxLength(6)

        pin_layout.addRow(
            "PIN mới:",
            self.new_pin_input
        )

        # ADD STACK
        self.stack.addWidget(password_page)
        self.stack.addWidget(pin_page)

        # =================================================
        # BUTTONS
        # =================================================
        btn_row = QHBoxLayout()

        btn_update = QPushButton(
            "Cập nhật"
        )

        btn_update.setObjectName(
            "btnPrimary"
        )

        btn_update.clicked.connect(
            self._on_update
        )

        btn_clear = QPushButton(
            "Làm mới"
        )

        btn_clear.setObjectName(
            "btnNormal"
        )

        btn_clear.clicked.connect(
            self._clear
        )

        btn_row.addStretch()

        btn_row.addWidget(
            btn_update
        )

        btn_row.addWidget(
            btn_clear
        )

        # =================================================
        # MAIN LAYOUT
        # =================================================
        layout.addWidget(form_w)

        layout.addWidget(self.stack)

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

                special_chars = (
                    "!@#$%^&*()-_=+[]{}|;:',.<>?/"
                )

                if len(new_password) < 8:
                    raise ValueError(
                        "Password must be at least 8 characters."
                    )

                if not new_password[0].isupper():
                    raise ValueError(
                        "Password must start with uppercase letter."
                    )

                if not any(
                    c.isdigit()
                    for c in new_password
                ):
                    raise ValueError(
                        "Password must contain at least one number."
                    )

                if not any(
                    c in special_chars
                    for c in new_password
                ):
                    raise ValueError(
                        "Password must contain at least one special character."
                    )

                account.password = new_password

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

                if not new_pin.isdigit():
                    raise ValueError(
                        "PIN must contain only numbers."
                    )

                if len(new_pin) != 6:
                    raise ValueError(
                        "PIN must be exactly 6 digits."
                    )

                account.pin = new_pin

                self.mw._show_success(
                    "Đổi mã PIN thành công!"
                )

            # SAVE
            self.mw.bank.save_all_data()

            self._clear()

        except Exception as e:

            self.mw._show_error(str(e))