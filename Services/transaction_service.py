from Models.transaction import Transaction
from Structures.Linked_list import LinkedList
from datetime import datetime

class TransactionService():
    def __init__(self):
        self.trans_storage = LinkedList()

    def generate_transaction_id(self):
        '''
        auto gen new trans_id type int from 1,2,....
        like Index
        '''
        if self.trans_storage.is_empty():
            return 1
        return self.trans_storage.tail.key + 1
    
    def add_transaction(self, from_account: str, to_account: str, type_trans: str, 
                        amount: float, description: str, balance_after: float) -> Transaction:
        '''
        Return new transaction and add new transaction to trans_storage
        '''
        new_trans = Transaction(
            trans_id= self.generate_transaction_id(),
            from_account= from_account,
            to_account= to_account,
            type_trans= type_trans,
            amount= amount,
            timestamp= None,
            description= description,
            balance_after= balance_after
        )

        self.trans_storage.append(new_trans.trans_id, new_trans)
        return new_trans

    def get_transactions_by_account(self, account_id=None):
        filtered_list = LinkedList()
        current_node = self.trans_storage.head
        while current_node is not None:
            trans = current_node.value
            
            if not account_id or trans.from_account == account_id or trans.to_account == account_id:
                filtered_list.append(trans.trans_id, trans)
            
            current_node = current_node.next
        return filtered_list

    def get_transactions_by_date(self, account_id=None, start_date_str=None, end_date_str=None):
        filtered_list = LinkedList()
        # Parse ngày bắt đầu (Nếu trống, mặc định là quá khứ rất xa)
        if start_date_str:
            try:
                # ĐÃ SỬA: Gán chính xác vào biến start_date thay vì start_date_str
                start_date = datetime.strptime(f"{start_date_str} 00:00:00", "%d/%m/%Y %H:%M:%S")
            except ValueError:
                start_date = datetime.min
        else:
            start_date = datetime.min
        
        # Parse ngày kết thúc (Nếu trống, mặc định là thời gian hiện tại)
        if end_date_str:
            try: 
                # Thêm ' 23:59:59' để tính đến hết ngày hôm đó
                end_date = datetime.strptime(f"{end_date_str} 23:59:59", "%d/%m/%Y %H:%M:%S")
            except ValueError:
                end_date = datetime.now()
        else:
            end_date = datetime.now()

        current = self.trans_storage.head
        while current:
            trans = current.value

            # Kiểm tra tài khoản
            match_account = True
            if account_id: 
                if trans.from_account != account_id and trans.to_account != account_id:
                    match_account = False
            
            # Kiểm tra mốc thời gian của giao dịch
            match_date = False
            if trans.timestamp and str(trans.timestamp).strip() != 'None':
                try:
                    trans_time = datetime.strptime(str(trans.timestamp), "%d/%m/%Y %H:%M:%S")
                    # So sánh xem thời gian giao dịch có nằm trong khoảng [start_date, end_date] không
                    if start_date <= trans_time <= end_date:
                        match_date = True
                except ValueError:
                    # Nếu timestamp của giao dịch bị lỗi định dạng, bỏ qua không đưa vào kết quả
                    match_date = False

            # Nếu thỏa mãn cả tài khoản và thời gian thì thêm vào linkedlist
            if match_account and match_date:
                filtered_list.append(trans.trans_id, trans)

            current = current.next
        return filtered_list

    def get_all_transactions(self):
        return self.trans_storage