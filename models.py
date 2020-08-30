import firebase_admin
import json
import locale
import os

from datetime import datetime, date
from firebase_admin import credentials
from firebase_admin import firestore


locale.setlocale(locale.LC_TIME, "es_CO.utf8")

cred = credentials.Certificate(os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH"))
firebase_admin.initialize_app(cred)

db = firestore.client()

class Expense():

    collection_name = 'expenses'

    def __init__(self, id=None, data=None):
        self.id = id
        self.date = date.today() if data is None else data['date']
        self.user = "" if data is None else data['user']
        self.value = None if data is None else data['value']
        self.group = "" if data is None else data['group']
        self.category = "" if data is None else data['category']
        self.comment = "" if data is None else data['comment']

    def create_expense(self):
        coll_ref = db.collection(self.collection_name)
        data = self.to_dict()
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        coll_ref.add(data)

    def update_expense(self):
        doc_ref = db.collection(self.collection_name).document(self.id)
        data = self.to_dict()
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        doc_ref.set(data)

    def delete_expense(self):
        db.collection(self.collection_name).document(self.id).delete()
    
    def to_dict(self):
        return {
            'date': self.date,
            'user': self.user,
            'value': self.value,
            'group': self.group,
            'category': self.category,
            'comment': self.comment,
        }

    @classmethod
    def get_expense(cls, id):
        doc_ref = db.collection(cls.collection_name).document(id)
        doc = doc_ref.get()
        if doc.exists:
            return cls(id, doc.to_dict())
        else:
            # TODO retornar algo util aca
            return 'No such document!'

    @classmethod
    def get_expenses_for_table(cls):
        coll_ref = db.collection(cls.collection_name)\
            .order_by('date', direction=firestore.Query.DESCENDING)\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = coll_ref.stream()

        fields = [
            {'field': 'date', 'label': 'Fecha'},
            {'field': 'day_name', 'label': 'Día'},
            {'field': 'user', 'label': 'Responsable'},
            {'field': 'value', 'label': 'Valor'},
            {'field': 'group', 'label': 'Grupo'},
            {'field': 'category', 'label': 'Categoría'},
            {'field': 'comment', 'label': 'Observaciones'},
        ]
        expenses = []
        for doc in docs:
            #print(f'{doc.id} => {doc.to_dict()}')
            raw_expense = doc.to_dict()

            if 'date' in raw_expense:
                parsed_date = datetime.strptime(raw_expense['date'], '%Y-%m-%d')
                day_name = parsed_date.strftime('%A')
                raw_expense['day_name'] = day_name

            printable_expense = [raw_expense[field['field']] if field['field'] in raw_expense else '' for field in fields]
            expense_id = doc.id

            expenses.append({'id': expense_id, 'data':printable_expense})

        return {'header': [field['label'] for field in fields], 'data': expenses}

    @classmethod
    def get_expenses_for_download(cls):
        coll_ref = db.collection(cls.collection_name)\
            .order_by('date')\
            .order_by('timestamp')
        docs = coll_ref.stream()

        fields = [
            'date',
            'day_name',
            'user',
            'value',
            'group',
            'category',
            'comment',
        ]
        expenses = []
        for doc in docs:
            raw_expense = doc.to_dict()

            if 'date' in raw_expense:
                parsed_date = datetime.strptime(raw_expense['date'], '%Y-%m-%d')
                day_name = parsed_date.strftime('%A')
                raw_expense['day_name'] = day_name
                ## Date formatting:
                raw_expense['date'] = parsed_date.strftime('%d/%m/%Y')
            printable_expense = [raw_expense[field] if field in raw_expense else '' for field in fields]

            expenses.append(printable_expense)

        return expenses
    
    @classmethod
    def delete_all(cls):
        coll_ref = db.collection(cls.collection_name)
        batch_size = 10
        
        def delete_collection(coll_ref, batch_size):
            docs = coll_ref.limit(batch_size).stream()
            deleted = 0

            for doc in docs:
                print(f'Deleting doc {doc.id} => {doc.to_dict()}')
                doc.reference.delete()
                deleted = deleted + 1

            if deleted >= batch_size:
                return delete_collection(coll_ref, batch_size)
        
        return delete_collection(coll_ref, batch_size)

class User:

    collection_name = 'users'

    def __init__(self, id=None, data=None):
        self.id = id
        self.name = '' if data is None else data['name']
    
    def to_dict(self):
        return {
            'name': self.name,
        }

    @classmethod
    def all(cls):
        coll_ref = db.collection(cls.collection_name).order_by('name')
        docs = coll_ref.stream()

        users = []
        for doc in docs:
            doc_dict = doc.to_dict()
            users.append(doc_dict['name'])
        return users

class Category:

    collection_name = 'categories'

    def __init__(self, id=None, group='', category='', type=''):
        self.id = id
        self.group = group
        self.category = category
        self.type = type
    
    def create(self):
        coll_ref = db.collection(self.collection_name)
        data = self.to_dict()
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        coll_ref.add(data)

    def update(self):
        doc_ref = db.collection(self.collection_name).document(self.id)
        data = self.to_dict()
        data['timestamp'] = firestore.SERVER_TIMESTAMP
        doc_ref.set(data)

    def delete(self):
        db.collection(self.collection_name).document(self.id).delete()
    
    def to_dict(self):
        return {
            'group': self.group,
            'category': self.category,
            'type': self.type,
        }

    def __repr__(self):
        return f"""Category(id='{self.id}', group='{self.group}',
            category='{self.category}', type='{self.type}')"""
    
    @classmethod
    def all(cls):
        coll_ref = db.collection(cls.collection_name).where('type', '==', 'Egreso')\
            .order_by('group').order_by('category')
        docs = coll_ref.stream()

        result = []
        for doc in docs:
            cat_item = doc.to_dict()
            cat = cls(
                id=doc.id,
                group=cat_item['group'],
                category=cat_item['category'],
                type=cat_item['type']
            )
            result.append(cat)
        return result
    
    @classmethod
    def init_collection(cls):
        with open('data/categories.json', 'r') as fp:
            cat_list = json.load(fp)

        for cat_item in cat_list:
            cat = cls(
                group=cat_item['group'],
                category=cat_item['category'],
                type=cat_item['type']
            )
            cat.create()
