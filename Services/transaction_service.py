from Models.transaction import Transaction
from Persistence.Transaction_repository import Transaction_repository
from Structures.Linked_list import LinkedList
from Models.account import Account
from Services.account_service import AccountService

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
        return self.trans_storage.tail.value.trans_id + 1
    
    
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
    

    def get_transaction_by_account(self):
        '''
        '''
    
if __name__ == "__main__":
    sv = TransactionService()
    t1 = sv.add_transaction("ACC001", "ACC002", "TRANSFER", 500000.0, "Chuyen tien", 2000000.0)
    print(f"ID: {t1.trans_id}, From: {t1.from_account}, Amount: {t1.amount}")
    t2 = sv.add_transaction("ACC001", "ACC003", "TRANSFER", 300000.0, "Chuyen tien", 1700000.0)
    print(f"ID: {t2.trans_id}, So du sau: {t2.balance_after}")
    t3 = sv.add_transaction("ACC002", "ACC001", "DEPOSIT", 1000000.0, "Nap tien", 3000000.0)
    print(f"ID: {t3.trans_id}, Loai: {t3.type_trans}")
    print(f"Tong giao dich: {sv.trans_storage.length()}")
    help(TransactionService.add_transaction)