"""Commander-build hooks (mkdocs.commander.yml only — the public site never loads this).

UAT pages carry `search: exclude: true` front matter so they stay out of the
public site's search index while remaining reachable by direct URL. On a
Commander they are nav-listed and first-class, so clear the exclusion before
mkdocs-material's search plugin reads it in `on_page_context`.

Editing the front matter in the .md files instead would leak UAT into the
*public* search index — the exclusion has to stay in the source and be undone
per-build, which is what this does.
"""

from __future__ import annotations


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri.startswith("uat/"):
        page.meta["search"] = {}
    return markdown
