import datetime
from dataclasses import asdict, dataclass, fields
from decimal import Decimal


@dataclass
class statement_transaction:
    trntype: str
    dtposted: datetime
    trnamt: Decimal
    fitid: str
    name: str
    category: str


@dataclass
class transaction_mapping_name:
    name: str
    category: str


@dataclass
class budget:
    year: int
    month: int
    category: str
    amount: Decimal
