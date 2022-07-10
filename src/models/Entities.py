from datetime import datetime
from decimal import Decimal
from pony.orm import PrimaryKey, Required, Optional ,Set
from src.providers.databases.ponyORM import PonyORMService
from uuid import UUID, uuid4

pony = PonyORMService()
db = pony.start()

class Member(db.Entity):
    _table_ = "TBL_Member"
    id = PrimaryKey(UUID, auto=True, default=uuid4)
    dcId = Required(str, unique=True)
    name = Required(str)
    balance = Required(Decimal, 10, 6, default=0.00)
    created_at = Required(datetime, default=datetime.utcnow)
    update_at = Required(datetime, default=datetime.utcnow)
    transactionsOwn = Set("Transaction", reverse="mid")
    transactionsDest = Set("Transaction", reverse="contributor")

class Transaction(db.Entity):
    _table_ = "TBL_Transaction"
    id = PrimaryKey(UUID, auto=True, default=uuid4)
    mid = Required(Member)
    type = Required(str)
    amount = Required(Decimal, 10, 6, default=0.00)
    contributor = Optional(Member, nullable=True)
    created_at = Required(datetime, default=datetime.utcnow)
    update_at = Required(datetime, default=datetime.utcnow)
    
class DefaultChannel(db.Entity):
    _table_ = "TBL_DefaultChannel"
    id = PrimaryKey(str)
    channel_id = Required(str, unique=True)
    created_at = Required(datetime, default=datetime.utcnow)
    update_at = Required(datetime, default=datetime.utcnow)
    update_by = Optional(str, nullable=True)

pony.migrate(db)