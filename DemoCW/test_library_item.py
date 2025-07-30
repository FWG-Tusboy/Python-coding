from library_item import LibraryItem

def test_info():
    item = LibraryItem("Imagine", "John Lennon", 5)
    assert item.info() == "Imagine - John Lennon *****"

def test_stars_zero():
    item = LibraryItem("Let It Be", "The Beatles")
    assert item.stars() == ""

def test_stars_partial():
    item = LibraryItem("Let It Be", "The Beatles", 3)
    assert item.stars() == "***"

def test_default_rating():
    item = LibraryItem("Shape of You", "Ed Sheeran")
    assert item.rating == 0

def test_default_play_count():
    item = LibraryItem("Halo", "Beyoncé")
    assert item.play_count == 0
