"""
Define an Abstract Base Class (ABC) for models
"""
from datetime import datetime
from typing import List

from sqlalchemy import inspect

from src.core.database import db


class BaseModel():
    """ Generalize __init__, __repr__ and to_json
        Based on the models columns """

    _created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    _updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

    print_filter = ()
    to_json_filter = ()
    non_updatable_column = ("email", "id", "_created_at", "_updated_at")

    def __repr__(self):
        """ Define a base way to print models
            Columns inside `print_filter` are excluded """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    def updatable_columns(self) -> List[str]:
        """ Columns that are valid for updating
                    Columns that starts with _ or rel_, are ignored """
        return [
            column
            for column in self._to_dict().keys()
            if column not in self.non_updatable_column and not column.startswith("_") and not column.startswith("rel_")
        ]

    @property
    def json(self):
        """ Define a base way to jsonify models
            Columns that starts with _ or rel_, are ignored """
        return {
            column: value
            if not isinstance(value, datetime) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter and not column.startswith("_") and not column.startswith("rel_")
        }

    def _to_dict(self):
        """ This would more or less be the same as a `to_json`
            But putting it in a "private" function
            Allows to_json to be overriden without impacting __repr__
            Or the other way around
            And to add filter lists """
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
