import json
import os
import shutil
import sys
from pathlib import Path
from markdown_it import MarkdownIt

# initialize Markdown parser
md = MarkdownIt("gfm-like")

# template file path
template_path = Path("resources/template.thtml")
template = template_path.read_text(encoding="utf-8")

base_url = sys.argv[2] if len(sys.argv) > 2 else ""

# PSP directory
psp_dir = Path("PSPs")
output_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "html")

# clean previous output
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(exist_ok=True)

# copy static site resources
shutil.copytree(Path("resources/site"), output_dir, dirs_exist_ok=True)

# collect PSPs into a JSON file for dynamic nav
psp_list = []
for md_file in sorted(psp_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    title_line = text.splitlines()[0].lstrip("# ").strip() if text else md_file.stem
    psp_list.append({"file": f"{md_file.stem}.html", "title": title_line})

# save the JSON
(Path(output_dir) / "psp_list.json").write_text(
    json.dumps(psp_list, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# helper: render markdown
def render_md(markdown):
    return md.render(markdown)

def replace_in_obj(obj, old, new):
    if isinstance(obj, dict):
        return {k: replace_in_obj(v, old, new) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_in_obj(elem, old, new) for elem in obj]
    elif isinstance(obj, str):
        return obj.replace(old, new)
    else:
        return obj

# modify web manifest
file_path = Path(os.path.join(output_dir, "site.webmanifest"))
manifest_data = json.loads(file_path.read_text(encoding="utf-8"))
manifest_data = replace_in_obj(manifest_data, "{base_url}", base_url)
file_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")

# convert README.md to index.html
readme_text = Path("README.md").read_text(encoding="utf-8")
readme_html = render_md(readme_text)
(output_dir / "index.html").write_text(
    template.format(title="Python Shit Proposals", content=readme_html, nav_links="", base_url=base_url),
    encoding="utf-8"
)

# convert each PSP markdown
for md_file in sorted(psp_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    html_content = render_md(text)
    (output_dir / f"{md_file.stem}.html").write_text(
        template.format(title=md_file.stem, content=html_content, nav_links="", base_url=base_url),
        encoding="utf-8"
    )

# LICENSE conversion if exists
if Path("LICENSE").exists():
    license_text = Path("LICENSE").read_text(encoding="utf-8")
    license_html = render_md(license_text)
    (output_dir / "LICENSE.html").write_text(
        template.format(title="LICENSE", content=license_html, nav_links="", base_url=base_url),
        encoding="utf-8"
    )
