from Models.transaction import Transaction
from Persistence.Transaction_repository import Transaction_repository
from Structures.Linked_list import LinkedList
from Models.account import Account
from Services.account_service import AccountService

class TransactionService():
    def __init__(self):
        self.trans_storage = LinkedList()

    
