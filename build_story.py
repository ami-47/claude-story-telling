"""
Build the story page from the verified facts.

    python3 generate_calls.py --seed 42
    python3 verify_calls.py
    python3 build_story.py

The template contains no numbers. This script drops answers/facts.json into it.
If a figure on the page is wrong, the fix is in verify_calls.py, never in the
HTML. That is the whole point of splitting it this way.

Every generated file goes in output/, never in the project root. The root
holds source: the template, the generator, the verifier. output/ holds
whatever the last build produced. Never edit anything in output/ by hand,
it is overwritten every run.
"""

import json
import pathlib

root = pathlib.Path(__file__).parent
out_dir = root / "output"
out_dir.mkdir(exist_ok=True)

facts = json.loads((root / "answers" / "facts.json").read_text())
tpl = (root / "story.template.html").read_text()

if "__FACTS__" not in tpl:
    raise SystemExit("template is missing the __FACTS__ placeholder")

# a quick guard against a number being hand typed back into the template
import re
suspicious = re.findall(r">\s*\d+\.\d+\s*(?:percent|%)", tpl)
if suspicious:
    raise SystemExit(f"hard coded figures found in the template: {suspicious}")

out = tpl.replace("__FACTS__", json.dumps(facts, separators=(",", ":")))
(out_dir / "story.html").write_text(out)

# A second copy with the document wrapper removed, for publishing as an
# artifact, where the host supplies the page skeleton.
frag = out
for a, b in (("<!doctype html>", ""), ("<html lang=\"en\">", ""),
             ("</html>", ""), ("<body>", ""), ("</body>", ""),
             ("<head>", ""), ("</head>", "")):
    frag = frag.replace(a, b)
for line in ('<meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             "<title>The Hour Nobody Was Watching</title>"):
    frag = frag.replace(line, "")
(out_dir / "story.artifact.html").write_text(frag.strip())

print(f"output/story.html written, {len(out) // 1024} KB, "
      f"{len(facts['facts'])} facts embedded")
