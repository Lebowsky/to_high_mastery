import inspect
import json

JSON_PATH = 'data/osconfeed.json'


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)

    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)

        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record

        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)
    return records


class Record:
    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__} serial={self.serial!r}'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):
    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)


if __name__ == '__main__':
    event = Record.fetch('event.33950')
    # assert event.venue == Record(serial=1449)
    assert event.venue.name == 'Portland 251'
    assert event.venue_serial == 1449
