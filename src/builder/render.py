import yaml
from os import chdir, getcwd, system
from re import sub
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .constants import TEMPLATE_FNAME

def tex_esc(text) -> str:
    """Regex filter for escaping special characters.

    Args:
        text (_type_): text to be formatted

    Returns:
        str: Formatted string.
    """
    text = str(text)
    return sub(r'([&_#%{}$^~\\])', r'\\\1', text)

def get_jinja_env(template_dir: Path) -> Environment:
    """Initializes jinja enviornment.

    Args:
        template_dir (Path): path to template directory

    Returns:
        Environment: Jinja environment.
    """
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{{",
        variable_end_string="}}",
    )
    return env

def build_template(profile_path: str, template_dir: str, tex_path: str) -> None:
    """Renders resume template from jinja template.

    Args:
        profile_path (str): path to profile directory
        template_dir (str): path to template directory
        tex_path (str): path to tex template
    """
    with open(profile_path) as f:
        data = yaml.safe_load(f)
    
    env = get_jinja_env(template_dir)
    env.filters['tex'] = tex_esc

    template_obj = env.get_template(f"{TEMPLATE_FNAME}")
    rendered = template_obj.render(data)

    with open(f"{tex_path}", "w") as f:
        f.write(rendered)

def latex_render(profile_build_dir: str) -> None:
    """Renders latex file into pdf.

    Args:
        profile_build_dir (str): path to profile directory
    """
    starting_dir = getcwd()
    try:
        chdir(profile_build_dir)
        system(
            "latexmk -pdf resume.tex"
            "&& latexmk -c"
        )
    finally:
        chdir(starting_dir)