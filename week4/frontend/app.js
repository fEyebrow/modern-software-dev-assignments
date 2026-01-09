async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function renderNotes(notes) {
  const ul = document.getElementById('notes');
  ul.innerHTML = '';
  if (notes.length === 0) {
    ul.innerHTML = '<li>No results found</li>';
    return;
  }
  notes.forEach(note => {
    const li = document.createElement('li');
    li.textContent = `${note.title}: ${note.content}`;
    ul.appendChild(li);
  });
}

async function loadNotes() {
  const notes = await fetchJSON('/notes/');
  renderNotes(notes);
}

async function searchNotes(query) {
  const notes = await fetchJSON(`/notes/search/?q=${encodeURIComponent(query)}`);
  renderNotes(notes);
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  document.getElementById('search-btn').addEventListener('click', async () => {
    const query = document.getElementById('note-search').value;
    if (query.trim()) {
      await searchNotes(query);
    }
  });

  document.getElementById('clear-search-btn').addEventListener('click', async () => {
    document.getElementById('note-search').value = '';
    await loadNotes();
  });

  document.getElementById('note-search').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const query = document.getElementById('note-search').value;
      if (query.trim()) {
        await searchNotes(query);
      }
    }
  });

  loadNotes();
  loadActions();
});
