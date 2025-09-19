import json
import os.path
import sys
from pathlib import Path
import shutil
from markdown_it import MarkdownIt

md = MarkdownIt("gfm-like")
not_affiliated_with = ("GitHub", "Twemoji", "Twitter")
notice = "\n\n---\n**Notice:** This site uses assets from the following companies: " + ", ".join(not_affiliated_with) + ". " \
         "I am not affiliated with them in any way. All trademarks, logos, and assets remain the property of their respective owners.\n"

template_path = Path("resources/template.thtml")

def replace_in_obj(obj, old, new):
    if isinstance(obj, dict):
        return {k: replace_in_obj(v, old, new) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_in_obj(elem, old, new) for elem in obj]
    elif isinstance(obj, str):
        return obj.replace(old, new)
    else:
        return obj

# im stoopid, I maked this, but we can just parse web manifest, ok, im fine(fire)
base_url = sys.argv[2] if len(sys.argv) > 2 else ""

# html template
template = template_path.read_text(encoding="utf-8")

# directories
psp_dir = Path("PSPs")

# some magic with output_dir
output_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "html")
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(exist_ok=True)

# copy files needed for site
shutil.copytree(Path("resources/site"), output_dir, dirs_exist_ok=True)

# modify web manifest
file_path = Path(os.path.join(output_dir, "site.webmanifest"))
manifest_data = json.loads(file_path.read_text(encoding="utf-8"))
manifest_data = replace_in_obj(manifest_data, "{base_url}", base_url)
file_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")

# collect nav links
nav_links = '<li><a href="index.html">Introduction</a></li>\n'
for md_file in sorted(psp_dir.glob("*.md")):
    nav_links += f'<li><a href="{md_file.stem}.html">{md_file.stem}</a></li>\n'

def render_md(markdown):
    return md.render(
        markdown
    )

# convert README.md to index.html
readme_text = Path("README.md").read_text(encoding="utf-8")
readme_html = render_md(readme_text)
(output_dir / "index.html").write_text(template.format(title="Python Shit Proposals", content=readme_html, nav_links=nav_links, base_url=base_url), encoding="utf-8")

# convert PSP markdown files
for md_file in sorted(psp_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    html_content = render_md(text)
    (output_dir / (md_file.stem + ".html")).write_text(template.format(title=md_file.stem, content=html_content, nav_links=nav_links, base_url=base_url), encoding="utf-8")

# convert LICENSE if exists
if Path("LICENSE").exists():
    license_text = Path("LICENSE").read_text(encoding="utf-8")
    license_text += notice
    license_html = render_md(license_text)
    (output_dir / "LICENSE.html").write_text(template.format(title="LICENSE", content=license_html, nav_links=nav_links, base_url=base_url), encoding="utf-8")