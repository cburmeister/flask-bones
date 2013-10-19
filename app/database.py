from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(),
                isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class DataTable(object):
    model = None
    query = None
    sortable = []
    searchable = []
    limits = []
    orders = ['asc', 'desc']

    def __init__(self, model, sortable, searchable, filterable, limits, request_values):
        self.model = model
        self.query = self.model.query
        self.sortable = sortable
        self.searchable = searchable
        self.filterable = filterable
        self.limits = limits

        for f in self.filterable:
            value = request_values.get(f.name, None)
            if value:
                self.filter(f.name, value)

        self.search(request_values.get('query', None))

        self.sort(
            request_values.get('sort', self.sortables),
            request_values.get('order', self.orders[0])
        )

        self.paginate(
            request_values.get('page', 1, type=int),
            request_values.get('limit', self.limits[1], type=int)
        )

    @property
    def sortables(self):
        return [x.name for x in self.sortable]

    @property
    def searchables(self):
        return [x.name for x in self.searchable]

    @property
    def filterables(self):
        return [x.name for x in self.filterable]

    def sort(self, sort, order):
        if sort in self.sortables and order in self.orders:
            field = getattr(getattr(self.model, sort), order)
            self.query = self.query.order_by(field())

    def filter(self, field, value):
        field = getattr(self.model, field)
        self.query = self.query.filter(field==value)

    def search(self, search, fields=[]):
        if search:
            search_query = '%%%s%%' % search
            from sqlalchemy import or_
            fields = [getattr(self.model, x) for x in self.searchables]
            self.query = self.query.filter(or_(*[x.like(search_query) for x in fields]))

    def paginate(self, page, limit):
        self.query = self.query.paginate(page, limit)
