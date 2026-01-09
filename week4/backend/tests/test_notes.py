def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_case_insensitive(client):
    """Test that search is case-insensitive"""
    # Create a note with uppercase content
    payload = {"title": "UPPERCASE", "content": "HELLO WORLD"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Search with lowercase query should find the uppercase note
    r = client.get("/notes/search/", params={"q": "hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(note["content"].upper() == "HELLO WORLD" for note in items)

    # Search with uppercase query should also work
    r = client.get("/notes/search/", params={"q": "UPPERCASE"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(note["title"].upper() == "UPPERCASE" for note in items)


def test_search_title_only(client):
    """Test search matching title only"""
    # Create a note with unique title
    payload = {"title": "UniqueTitle123", "content": "Different content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Search for the unique title
    r = client.get("/notes/search/", params={"q": "UniqueTitle"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any("UniqueTitle123" in note["title"] for note in items)


def test_search_content_only(client):
    """Test search matching content only"""
    # Create a note with unique content
    payload = {"title": "Generic Title", "content": "UniqueContent456"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Search for the unique content
    r = client.get("/notes/search/", params={"q": "UniqueContent"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any("UniqueContent456" in note["content"] for note in items)


def test_search_no_results(client):
    """Test search with no matching results returns empty list"""
    r = client.get("/notes/search/", params={"q": "NonexistentQuery987654321"})
    assert r.status_code == 200
    items = r.json()
    assert items == []


def test_search_empty_query(client):
    """Test search with empty query returns all notes"""
    # Create a test note
    payload = {"title": "Test Note", "content": "Test Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Get all notes
    r = client.get("/notes/")
    all_notes = r.json()

    # Search with empty query should return all notes
    r = client.get("/notes/search/", params={"q": ""})
    assert r.status_code == 200
    search_results = r.json()
    assert len(search_results) == len(all_notes)
