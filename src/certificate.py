import settings
import database
from datetime import datetime

FIND_ALL_CERTIFICATES = """
    SELECT id, name, domains, first_created, last_updated
    FROM Certificates
"""
FIND_CERTIFICATE_SQL = FIND_ALL_CERTIFICATES + """
    WHERE id = ?
"""

UPDATE_CERTIFICATE_SQL = """
    UPDATE Certificates
    SET last_updated = ?, name = ?
    WHERE id = ?;
"""

CREATE_CERTIFICATE_SQL = """
    INSERT INTO Certificates (domains, name)
    VALUES (?, ?);
"""

class CertificateManager:
    def __init__(self, db):
        self.db = db

    def find_all (self, ):
        cursor = self.db.cursor()
        instances = [Certificate(data=record, db=self.db) for record in cursor.execute(FIND_ALL_CERTIFICATES)]
        cursor.close()
        return instances

    def create(self, data):
        return Certificate(db=self.db, data=data)

class Certificate:
    db = None
    data = {}
    renewing = False

    def __init__(self, data={}, db=None):
        self._set('db', db)
        self._set('data', data)
        print(self.data)

    def __getattr__(self, key):
        try:
            return self.data[key]
        except:
            return None
    def __setattr__(self, key, value):
        self.data[key] = value

    def is_created(self):
        return self.id is not None

    def save (self):
        if self.is_created():
            self.update()
        else:
            self.insert()
            self.reload()

    def update(self):
        cursor = self.db.cursor()
        cursor.execute(UPDATE_CERTIFICATE_SQL, (self.last_updated, self.name, self.id))
        self.db.commit()
        cursor.close()

    def insert(self):
        cursor = self.db.cursor()
        cursor.execute(CREATE_CERTIFICATE_SQL, (self.domains, self.name,))
        self.id = cursor.lastrowid
        self.db.commit()
        cursor.close()

    def reload(self):
        cursor = self.db.cursor()
        data = cursor.execute(FIND_CERTIFICATE_SQL, (self.id,)).fetchone()
        self._set('data', data)
        self.db.commit()
        cursor.close()

    def get_all(self):
        return self.data

    def last_renewed(self):
        if self.last_updated is not None:
            return datetime.strptime(self.last_updated, '%y-%m-%d %H:%M:%S')
        else:
            return None

    def is_renewing(self, status=None):
        if status is None:
            return self.renewing
        else:
            self._set('renewing', status)

    def renewed(self):
        self.last_renewed = datetime.now()
        self._set('renewing', False)

    def _set(self, key, value):
        object.__setattr__(self, key, value)
