import sys
from pathlib import Path

from markdown_it import MarkdownIt

md = MarkdownIt("gfm-like")

# html template
template = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link id="themeLink" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
<style>
/* hide until theme applied */
html {{ visibility: hidden; }}

/* CSS variables for theme */
:root {{
    --bg-color: #fdfdfd;
    --text-color: #222222;
    --link-color: #1a73e8;
    --nav-bg: #f7f7f7;
    --footer-color: #555;
    --code-bg: #d8d8d8;
    --table-bg: #ffffff;
    --table-alt-bg: #f0f0f0;
    --menu-toggle-color: black;
}}

html[data-theme='dark'] {{
    --bg-color: #181818;
    --text-color: #e0e0e0;
    --link-color: #8ab4f8;
    --nav-bg: #242424;
    --footer-color: #aaa;
    --code-bg: #2a2a2a;
    --table-bg: #1e1e1e;
    --table-alt-bg: #252525;
    --menu-toggle-color: white;
}}

html[data-theme] {{ visibility: visible; }}

* {{
    box-sizing: border-box;
    transition: background-color 0.3s, color 0.3s;
}}

#app {{
  opacity: 0;
  transform: translateY(30px) scale(0.98);
  transition: opacity 0.6s ease, transform 0.6s ease;
}}

#app.visible {{
  opacity: 1;
  transform: translateY(0) scale(1);
}}

* a {{
    color: var(--link-color);
    text-decoration: none;       
    font-weight: 500;
    position: relative;          
    transition: color 0.2s, transform 0.2s;
}}

* a:hover {{
    color: var(--link-color);
    transform: translateY(-1px); 
    filter: brightness(80%);
}}

* a:visited {{
    color: var(--link-color);
}}

body {{
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    display: flex;
    min-height: 100vh;
}}

pre, code {{
    background-color: var(--code-bg) !important;
    color: inherit !important;
    border-radius: 6px;
    padding: 0.3em 0.5em;
}}

nav {{
    width: 250px;
    background-color: var(--nav-bg);
    padding: 20px;
    flex-shrink: 0;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}}

.license-reminder {{
    display: inline-block;
    margin-left: calc(4em * 5.5);
    padding: 2px 4px;
}}

/* nav container */
nav {{
    width: 250px;
    background-color: var(--nav-bg);
    padding: 20px;
    flex-shrink: 0;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05);
    transition: background-color 0.3s, transform 0.3s ease;
}}

/* nav title */
nav h3 {{
    margin-top: 0;
    font-size: 1.2em;
    color: var(--text-color);
    margin-bottom: 12px;
}}

/* nav list */
nav ul {{
    list-style: none;
    padding-left: 0;
    margin: 0;
}}

/* nav items */
nav li {{
    margin: 6px 0;
}}

/* links styling */
nav a {{
    display: block;
    padding: 8px 12px;
    border-radius: 6px;
    color: var(--link-color);
    text-decoration: none;
    transition: background-color 0.2s, color 0.2s;
}}

/* hover effect */
nav a:hover {{
    background-color: rgba(255,255,255,0.1);
}}

/* active link */
nav a.active {{
    font-weight: bold;
    border-left: 4px solid var(--link-color);
    background-color: rgba(255,255,255,0.15);
    padding-left: 10px;
}}

/* visited links same as normal */
nav a:visited {{
    color: var(--link-color);
}}

/* dark theme tweaks */
html[data-theme='dark'] nav a:hover {{
    background-color: rgba(255,255,255,0.05);
}}
html[data-theme='dark'] nav a.active {{
    background-color: rgba(255,255,255,0.1);
}}

main {{ flex: 1; padding: 40px; max-width: 900px; }}
footer {{ margin-top: 60px; font-size: 0.9em; color: var(--footer-color); }}

table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
th, td {{ padding: 12px; border: 1px solid #ccc; }}
tr:nth-child(even) {{ background-color: var(--table-alt-bg); }}

#theme-toggle {{
    position: fixed; top: 20px; right: 20px;
    background: var(--nav-bg); color: var(--text-color);
    border: none; padding: 8px 12px; border-radius: 50%;
    cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-size: 18px; z-index:2000;
}}
#theme-toggle:hover {{ box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}

#menu-toggle {{
    display: none; position: fixed; top:20px; left:20px;
    background: var(--nav-bg); border: none; padding:8px 12px; border-radius:4px;
    cursor:pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); font-size:20px; z-index:2000;
}}
#menu-toggle:hover {{ box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}

@media (max-width:768px) {{
    nav {{ position: fixed; left:0; top:0; height:100%; transform:translateX(-100%); z-index:1000; }}
    nav.open {{ transform: translateX(0); }}
    #menu-toggle {{ display:block; }}
    main {{ padding: 20px; }}
}}
</style>

<!-- Apply saved theme immediately to html -->
<script>
(function(){{
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
}})();
</script>

</head>
<body>
<button id="menu-toggle">☰</button>
<button id="theme-toggle"><span id="theme-icon">☀️</span></button>
<nav>
<h3>PSPs</h3>
<ul>
{nav_links}
</ul>
</nav>
<main id="app">
{content}
<footer>
<a href="LICENSE.html" class="license-reminder">See LICENSE</a>
</footer>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script>
hljs.highlightAll();

// highlight current nav link
document.querySelectorAll('nav a').forEach(a=>{{
    if(a.getAttribute('href')===location.pathname.split("/").pop()) a.classList.add('active');
}});

const menuToggle = document.getElementById("menu-toggle");

// theme toggle icon & switching
document.addEventListener('DOMContentLoaded', ()=>{{
    requestAnimationFrame(()=>{{
        document.getElementById('app').classList.add('visible');
    }});
    const toggle = document.getElementById("theme-toggle");
    const icon = document.getElementById("theme-icon");
    const root = document.documentElement;
    
    icon.textContent = root.getAttribute('data-theme')==='dark' ? '🌙' : '☀️';
    menuToggle.style.color = getComputedStyle(root).getPropertyValue('--menu-toggle-color');
    if(root.getAttribute('data-theme') === 'dark') {{
        themeLink.href = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css";
    }} else {{
        themeLink.href = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css";
    }}

    toggle.addEventListener('click', ()=>{{
        const newTheme = root.getAttribute('data-theme')==='dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        icon.textContent = newTheme==='dark' ? '🌙' : '☀️';
        menuToggle.style.color = getComputedStyle(root).getPropertyValue('--menu-toggle-color');
        if(root.getAttribute('data-theme') === 'dark') {{
            themeLink.href = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css";
        }} else {{
            themeLink.href = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css";
        }}
    }});
}});

// mobile nav toggle
const nav = document.querySelector("nav");
menuToggle.addEventListener("click", ()=>{{ nav.classList.toggle("open"); }});
document.querySelectorAll('nav a').forEach(a=>{{
    a.addEventListener("click", ()=>{{ if(nav.classList.contains("open")) nav.classList.remove("open"); }});
}});
</script>
</body>
</html>
"""


# directories
psp_dir = Path("PSPs")
output_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "html")
output_dir.mkdir(exist_ok=True)

# collect nav links
nav_links = '<li><a href="index.html">Introduction</a></li>\n'
for md_file in sorted(psp_dir.glob("*.md")):
    nav_links += f'<li><a href="{md_file.stem}.html">{md_file.stem}</a></li>\n'

def render_md(text):
    return md.render(
        text
    )

# convert README.md to index.html
readme_text = Path("README.md").read_text(encoding="utf-8")
readme_html = render_md(readme_text)
(output_dir / "index.html").write_text(template.format(title="Introduction", content=readme_html, nav_links=nav_links), encoding="utf-8")

# convert PSP markdown files
for md_file in sorted(psp_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    html_content = render_md(text)
    (output_dir / (md_file.stem + ".html")).write_text(template.format(title=md_file.stem, content=html_content, nav_links=nav_links), encoding="utf-8")

# convert LICENSE if exists
if Path("LICENSE").exists():
    license_text = Path("LICENSE").read_text(encoding="utf-8")
    license_html = render_md(license_text)
    (output_dir / "LICENSE.html").write_text(template.format(title="LICENSE", content=license_html, nav_links=nav_links), encoding="utf-8")