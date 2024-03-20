from evt import Event, Record
def test_basic_behaviour_event():
    event = Event()
    assert event.venue == Record(serial=1449)
    assert event.venue.name == 'Portland 251'
    for spkr in event.speakers:
        print(f'{spkr.serial}: {spkr.name}')
    