#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine('mysql://sanjeevan:AexahWie4u@aria/nanoinvoice_py')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

invoice = Table(u'invoice', metadata,
    Column(u'id', BIGINT(), primary_key=True, nullable=False),
    Column(u'user_id', BIGINT(), ForeignKey('user.id')),
    Column(u'contact_id', BIGINT(), ForeignKey('contact.id')),
    Column(u'payment_term_id', BIGINT(), ForeignKey('payment_term.id')),
    Column(u'source', VARCHAR(length=255)),
    Column(u'status', VARCHAR(length=255)),
    Column(u'reference', VARCHAR(length=255)),
    Column(u'po_reference', VARCHAR(length=255)),
    Column(u'currency_code', VARCHAR(length=5)),
    Column(u'date_issued', DATETIME()),
    Column(u'due_date', DATETIME()),
    Column(u'written_off_date', DATETIME()),
    Column(u'sub_total', DECIMAL(precision=8, scale=2)),
    Column(u'tax', DECIMAL(precision=8, scale=2)),
    Column(u'total', DECIMAL(precision=8, scale=2)),
    Column(u'created_at', DATETIME(), nullable=False),
    Column(u'updated_at', DATETIME(), nullable=False),
)

invoice_item = Table(u'invoice_item', metadata,
    Column(u'id', BIGINT(), primary_key=True, nullable=False),
    Column(u'invoice_id', BIGINT(), ForeignKey('invoice.id')),
    Column(u'type_id', BIGINT(), ForeignKey('invoice_item_type.id')),
    Column(u'tax_rate_id', BIGINT(), ForeignKey('tax_rate.id')),
    Column(u'description', TEXT()),
    Column(u'quantity', DECIMAL(precision=5, scale=3)),
    Column(u'price', DECIMAL(precision=8, scale=2)),
    Column(u'tax', DECIMAL(precision=8, scale=2)),
    Column(u'total', DECIMAL(precision=8, scale=2)),
    Column(u'sort_order', Integer()),
    Column(u'created_at', DATETIME(), nullable=False),
    Column(u'updated_at', DATETIME(), nullable=False),
)

profile = Table(u'profile', metadata,
    Column(u'id', BIGINT(), primary_key=True, nullable=False),
    Column(u'user_id', BIGINT(), ForeignKey('user.id'), nullable=False),
    Column(u'logo_id', BIGINT(), ForeignKey('file.id')),
    Column(u'company_type_id', BIGINT(), ForeignKey('account_type.id')),
    Column(u'company_name', VARCHAR(length=255)),
    Column(u'company_address1', VARCHAR(length=255)),
    Column(u'company_address2', VARCHAR(length=255)),
    Column(u'company_town', VARCHAR(length=255)),
    Column(u'company_county', VARCHAR(length=255)),
    Column(u'company_post_code', VARCHAR(length=20)),
    Column(u'company_registration_number', VARCHAR(length=30)),
    Column(u'is_complete', Integer()),
    Column(u'last_seen_ip', VARCHAR(length=40)),
    Column(u'created_at', DATETIME(), nullable=False),
    Column(u'updated_at', DATETIME(), nullable=False),
)

user_group = Table(u'user_group', metadata,
    Column(u'user_id', BIGINT(), ForeignKey('user.id'), primary_key=True, nullable=False),
    Column(u'group_id', BIGINT(), ForeignKey('group.id'), primary_key=True, nullable=False),
    Column(u'created_at', DATETIME(), nullable=False),
    Column(u'updated_at', DATETIME(), nullable=False),
)

vat_registration = Table(u'vat_registration', metadata,
    Column(u'id', BIGINT(), primary_key=True, nullable=False),
    Column(u'user_id', BIGINT(), ForeignKey('user.id'), nullable=False),
    Column(u'status', VARCHAR(length=255)),
    Column(u'number', VARCHAR(length=20)),
    Column(u'registration_date', DATETIME()),
    Column(u'de_registration_date', DATETIME()),
    Column(u'first_return_date', DATETIME()),
    Column(u'scheme_id', BIGINT(), ForeignKey('vat_scheme.id')),
    Column(u'created_at', DATETIME(), nullable=False),
    Column(u'updated_at', DATETIME(), nullable=False),
)


class BankAccount(DeclarativeBase):
    __tablename__ = 'bank_account'

    __table_args__ = {}

    #column definitions
    account_name = Column(u'account_name', VARCHAR(length=255))
    bank_name = Column(u'bank_name', VARCHAR(length=255))
    created_at = Column(u'created_at', DATETIME(), nullable=False)
    id = Column(u'id', BIGINT(), primary_key=True, nullable=False)
    is_personal = Column(u'is_personal', Integer())
    is_primary = Column(u'is_primary', Integer())
    number = Column(u'number', VARCHAR(length=100))
    show_on_invoice = Column(u'show_on_invoice', Integer())
    sort_code = Column(u'sort_code', VARCHAR(length=100))
    updated_at = Column(u'updated_at', DATETIME(), nullable=False)
    user_id = Column(u'user_id', BIGINT(), ForeignKey('user.id'), nullable=False)

    #relation definitions
    user = relation('User', primaryjoin='BankAccount.user_id==User.id')





   #relation definitions


class ForgotPassword(DeclarativeBase):
    __tablename__ = 'forgot_password'

    __table_args__ = {}

    #column definitions
    created_at = Column(u'created_at', DATETIME(), nullable=False)
    expires_at = Column(u'expires_at', DATETIME(), nullable=False)
    id = Column(u'id', BIGINT(), primary_key=True, nullable=False)
    unique_key = Column(u'unique_key', VARCHAR(length=255))
    updated_at = Column(u'updated_at', DATETIME(), nullable=False)
    user_id = Column(u'user_id', BIGINT(), ForeignKey('user.id'), nullable=False)

    #relation definitions
    user = relation('User', primaryjoin='ForgotPassword.user_id==User.id')


class Group(DeclarativeBase):
    __tablename__ = 'group'

    __table_args__ = {}

    #column definitions
    created_at = Column(u'created_at', DATETIME(), nullable=False)
    description = Column(u'description', TEXT())
    id = Column(u'id', BIGINT(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255))
    updated_at = Column(u'updated_at', DATETIME(), nullable=False)

    #relation definitions
    users = relation('User', primaryjoin='Group.id==UserGroup.group_id', secondary=user_group, secondaryjoin='UserGroup.user_id==User.id')


class Invoice(DeclarativeBase):
    __table__ = invoice


    #relation definitions
    contact = relation('Contact', primaryjoin='Invoice.contact_id==Contact.id')
    user = relation('User', primaryjoin='Invoice.user_id==User.id')
    payment_term = relation('PaymentTerm', primaryjoin='Invoice.payment_term_id==PaymentTerm.id')
    invoice_item_types = relation('InvoiceItemType', primaryjoin='Invoice.id==InvoiceItem.invoice_id', secondary=invoice_item, secondaryjoin='InvoiceItem.type_id==InvoiceItemType.id')


class InvoiceItem(DeclarativeBase):
    __table__ = invoice_item


    #relation definitions
    invoice_item_type = relation('InvoiceItemType', primaryjoin='InvoiceItem.type_id==InvoiceItemType.id')
    invoice = relation('Invoice', primaryjoin='InvoiceItem.invoice_id==Invoice.id')
    tax_rate = relation('TaxRate', primaryjoin='InvoiceItem.tax_rate_id==TaxRate.id')






class Profile(DeclarativeBase):
    __table__ = profile


    #relation definitions
    account_type = relation('AccountType', primaryjoin='Profile.company_type_id==AccountType.id')
    user = relation('User', primaryjoin='Profile.user_id==User.id')
    file = relation('File', primaryjoin='Profile.logo_id==File.id')


class TaxRate(DeclarativeBase):
    __tablename__ = 'tax_rate'

    __table_args__ = {}

    #column definitions
    created_at = Column(u'created_at', DATETIME(), nullable=False)
    id = Column(u'id', BIGINT(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=100))
    rate = Column(u'rate', DECIMAL(precision=5, scale=2))
    type = Column(u'type', VARCHAR(length=255))
    updated_at = Column(u'updated_at', DATETIME(), nullable=False)

    #relation definitions
    invoices = relation('Invoice', primaryjoin='TaxRate.id==InvoiceItem.tax_rate_id', secondary=invoice_item, secondaryjoin='InvoiceItem.invoice_id==Invoice.id')





class VatRegistration(DeclarativeBase):
    __table__ = vat_registration


    #relation definitions
    vat_scheme = relation('VatScheme', primaryjoin='VatRegistration.scheme_id==VatScheme.id')
    user = relation('User', primaryjoin='VatRegistration.user_id==User.id')


class VatScheme(DeclarativeBase):
    __tablename__ = 'vat_scheme'

    __table_args__ = {}

    #column definitions
    created_at = Column(u'created_at', DATETIME(), nullable=False)
    id = Column(u'id', BIGINT(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=100))
    updated_at = Column(u'updated_at', DATETIME(), nullable=False)
    vat_rate = Column(u'vat_rate', DECIMAL(precision=5, scale=2))

    #relation definitions
    users = relation('User', primaryjoin='VatScheme.id==VatRegistration.scheme_id', secondary=vat_registration, secondaryjoin='VatRegistration.user_id==User.id')


