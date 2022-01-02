from src.providers.databases.ponyORM import PonyORMService
from src.models.TransactionType import TransactionType
from pony.orm import PrimaryKey, Required, Set
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

pony = PonyORMService()
db = pony.start()

class Member(db.Entity):
    _table_ = "TBL_Member"
    id = PrimaryKey(UUID, auto=True, default=uuid4)
    dcId = Required(str, unique=True)
    name = Required(str)
    balance = Required(Decimal, 10, 2, default=0.00)
    created_at = Required(datetime)
    update_at = Required(datetime)
    transactionsOwn = Set("Transactions", reverse="mid")
    transactionsDest = Set("Transactions", reverse="contributor")

class Transactions(db.Entity):
    _table_ = "TBL_Transactions"
    id = PrimaryKey(UUID, auto=True, default=uuid4)
    mid = Required(Member)
    type = Required(str)
    amount = Required(Decimal, 10, 2, default=0.00)
    contributor = Required(Member, nullable=True)
    created_at = Required(datetime)
    update_at = Required(datetime)

pony.migrate(db)