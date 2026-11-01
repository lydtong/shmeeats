# shmeeats

Mimi & Lydia's restaurant map. Published at https://claude.ai/artifact/JLdA6U3xBJTohoV5hobTxt

- `src/template.html` — the page source (edit this, not index.html)
- `src/build.py` — inlines the logo, the US state outlines, and the city list into `index.html`
- `logo.png` — the cat drawing, cleaned up (transparent); `cat-original.png` is the photo
- Rebuild: `python3 -I src/build.py src/states-albers-10m.json src/cities15000.txt logo.png index.html`
- Admin: footer "admin" link, users mimi / lydia, password midia. Saving needs Editor access on the artifact.
