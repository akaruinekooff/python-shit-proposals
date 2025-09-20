import json
import shutil
from pathlib import Path
from markdown_it import MarkdownIt

# initialize Markdown parser
md = MarkdownIt("gfm-like")

# template file path
template_path = Path("resources/template.thtml")
template = template_path.read_text(encoding="utf-8")

# PSP directory
psp_dir = Path("PSPs")
output_dir = Path("html")

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

# convert README.md to index.html
readme_text = Path("README.md").read_text(encoding="utf-8")
readme_html = render_md(readme_text)
(output_dir / "index.html").write_text(
    template.format(title="Python Shit Proposals", content=readme_html, nav_links="", base_url=""),
    encoding="utf-8"
)

# convert each PSP markdown
for md_file in sorted(psp_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    html_content = render_md(text)
    (output_dir / f"{md_file.stem}.html").write_text(
        template.format(title=md_file.stem, content=html_content, nav_links="", base_url=""),
        encoding="utf-8"
    )

# LICENSE conversion if exists
if Path("LICENSE").exists():
    license_text = Path("LICENSE").read_text(encoding="utf-8")
    license_html = render_md(license_text)
    (output_dir / "LICENSE.html").write_text(
        template.format(title="LICENSE", content=license_html, nav_links="", base_url=""),
        encoding="utf-8"
    )
