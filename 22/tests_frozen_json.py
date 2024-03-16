import json
import os
from explore0 import FrozenJSON


def test_can_use_frozen_json_getattr():
    with open('./22/data/osconfeed.json') as fp:
        raw_feed = json.load(fp)
        feed = FrozenJSON(raw_feed)
        assert len(feed.Schedule.speakers) == 357
        assert list(feed.keys()) == ['Schedule']
        assert sorted(feed.Schedule.keys()) == ['conferences', 'events', 'speakers', 'venues']
        assert feed.Schedule.speakers[-1].name == 'Carina C. Zona'
        talk = feed.Schedule.events[40]
        assert type(talk) == FrozenJSON
        assert talk.name == 'There *Will* Be Bugs'
        assert talk.speakers == [3471, 5199]

        try:
            talk.flavor
        except Exception as e:
            assert type(e) is KeyError
