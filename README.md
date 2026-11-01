# shmeeats

Mimi & Lydia's restaurant map. Live at https://lydtong.github.io/shmeeats/

- `index.html` — the whole site (built; do not edit by hand)
- `src/template.html` — the page source. Edit this, then rebuild:
  `python3 -I src/build.py src/states-albers-10m.json src/cities15000.txt logo.png index.html`
- `data/reviews.json` — every review. The admin page writes here through the GitHub API.
- `photos/` — review photos, uploaded by the admin page.
- `logo.png` — the cat drawing, cleaned up; `cat-original.png` is the photo.

Admin: the footer "admin" link. Users mimi / lydia, password midia. To save, paste a
fine-grained GitHub token (repo access: this repo only; permission: Contents read & write)
into the "connect to github" box once per browser.
