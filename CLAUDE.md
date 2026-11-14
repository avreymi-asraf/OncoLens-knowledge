# OncoLens knowledge

A cortex (see the `cortex` skill) for building a method that trains small models to extract information from oncology patient records. Read `cortex/profile.md` before any operation; it states the purpose, layout, anchors and checking rules.

- `sources/` immutable originals and stored text; `cortex/` claims, pages, tensions, questions, `index.md`.
- Run the checker as `uv run .claude/skills/cortex/scripts/cortex.py check` from the repo root; it must pass before every commit.
- PDFs are converted with the `pdf-to-markdown-mcp` skill before `cortex.py store`.
