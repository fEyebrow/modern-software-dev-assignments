def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_delete_note_success(client):
    payload = {"title": "To be deleted", "content": "This will be removed"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_create_note_empty_title(client):
    payload = {"title": "", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_whitespace_only_title(client):
    payload = {"title": "   ", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_title_too_long(client):
    payload = {"title": "a" * 201, "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_empty_content(client):
    payload = {"title": "Title", "content": ""}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_content_too_long(client):
    payload = {"title": "Title", "content": "a" * 10001}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_list_notes_invalid_sort_field(client):
    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 400
    assert "Invalid sort field" in r.json()["detail"]


def test_list_notes_invalid_sort_field_with_prefix(client):
    r = client.get("/notes/", params={"sort": "-invalid_field"})
    assert r.status_code == 400
    assert "Invalid sort field" in r.json()["detail"]
