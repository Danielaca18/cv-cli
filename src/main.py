# from jinja2 import Environment, FileSystemLoader
# from pathlib import Path
# import yaml
# import os
# import re
# import sys
# import argparse
# import shutil

# BASE_DIR = Path(__file__).resolve().parent
# PROFILES_DIR = BASE_DIR / "profiles"
# TEMPLATES_DIR = BASE_DIR / "templates"
# BUILD_DIR = BASE_DIR / "build"
# OUTPUT_DIR = BASE_DIR / "output"

# DEFAULT_TEMPLATE = "default"
# DEFAULT_PROFILE = "profile_default"
# OUTPUT_FILE = OUTPUT_DIR / "resume_output.tex"

# TEX_FNAME = "resume.tex"
# TEMPLATE_FNAME = "template.j2"
# STYLE_FNAME = "style.tex"

# def tex_esc(text) -> str:
#     """Regex filter for escaping special characters.

#     Args:
#         text (_type_): text to be formatted

#     Returns:
#         str: Formatted string.
#     """
#     text = str(text)
#     return re.sub(r'([&_#%{}$^~\\])', r'\\\1', text)

# # def make_dirs():
# #     """Creates required project directories.
# #     """
# #     os.makedirs(f"{OUTPUT_DIR}", exist_ok=True)
# #     os.makedirs(f"{BUILD_DIR}", exist_ok=True)

# def move_pdf(pdf_path:str, output_path:str) -> None:
#     """Moves specified pdf file.

#     Args:
#         pdf_path (str): source path
#         output_path (str): destination path
#     """
#     if os.path.exists(pdf_path):
#         os.replace(pdf_path, output_path)
#         print(f"PDF moved to {output_path}")
#     else:
#         print(f"PDF not found: {pdf_path}")

# def get_jinja_env(template_dir: Path) -> Environment:
#     """Initializes jinja enviornment.

#     Args:
#         template_dir (Path): path to template directory

#     Returns:
#         Environment: Jinja environment.
#     """
#     env = Environment(
#         loader=FileSystemLoader(str(template_dir)),
#         trim_blocks=True,
#         lstrip_blocks=True,
#         block_start_string="{%",
#         block_end_string="%}",
#         variable_start_string="{{",
#         variable_end_string="}}",
#     )
#     return env

# def get_args() -> argparse.Namespace:
#     """Parses cli arguments

#     Returns:
#         argparse.Namespace: Parsed arguments.
#     """
#     parser = argparse.ArgumentParser(description="Generate latex resumes from a yaml profile.")
#     parser.add_argument(
#         "-p", "--profile",
#         default=DEFAULT_PROFILE,
#         help="Name of yaml profile (e.g. default -> profiles/default.yaml)"
#     )
#     parser.add_argument(
#         "-t", "--template",
#         default=DEFAULT_TEMPLATE,
#         help="Name of resume template (e.g. default -> templates/default.j2)"
#     )
#     parser.add_argument(
#         "-o", "--output",
#         help="Name of output pdf (e.g. resume -> resume.pdf)"
#     )

#     args = parser.parse_args()
#     return args

# def init_build(profile_build_dir: str, style_path: str) -> None:
#     """Initializes required directories and files.

#     Args:
#         profile_build_dir (str): path to profiles directory
#         style_path (str): path to styles directory
#     """
#     os.makedirs(f"{OUTPUT_DIR}", exist_ok=True)
#     os.makedirs(profile_build_dir, exist_ok=True)
#     shutil.copy(style_path, profile_build_dir)

# def build_template(profile_path: str, template_dir: str, tex_path: str) -> None:
#     """Renders resume template from jinja template.

#     Args:
#         profile_path (str): path to profile directory
#         template_dir (str): path to template directory
#         tex_path (str): path to tex template
#     """
#     with open(profile_path) as f:
#         data = yaml.safe_load(f)
    
#     env = get_jinja_env(template_dir)
#     env.filters['tex'] = tex_esc

#     template_obj = env.get_template(f"{TEMPLATE_FNAME}")
#     rendered = template_obj.render(data)

#     with open(f"{tex_path}", "w") as f:
#         f.write(rendered)    

# def latex_render(profile_build_dir: str) -> None:
#     """Renders latex file into pdf.

#     Args:
#         profile_build_dir (str): path to profile directory
#     """
#     starting_dir = os.getcwd()
#     try:
#         os.chdir(profile_build_dir)
#         os.system(
#             "latexmk -pdf resume.tex"
#             "&& latexmk -c"
#         )
#     finally:
#         os.chdir(starting_dir)

import sys
sys.path.append("src") 

from builder.cli import get_args
from builder.render import build_template, latex_render
from builder.io import init_build, move_pdf
from builder.constants import PROFILES_DIR, TEMPLATES_DIR, BUILD_DIR, TEX_FNAME, OUTPUT_DIR

def compile_pdf(profile: str, template: str, output_name: str) -> None:
    """Compiles template and profile into a pdf resume.

    Args:
        profile (str): name of profile
        template (str): name of template
        output_name (str): pdf file name (no extension)
    """
    profile_path = PROFILES_DIR / f"{profile}.yaml"
    template_dir = TEMPLATES_DIR / template
    profile_build_dir = BUILD_DIR / profile
    pdf_fname = f"{output_name}.pdf"
    tex_path = profile_build_dir / TEX_FNAME

    init_build(profile_build_dir, template_dir)
    build_template(profile_path, template_dir, tex_path)
    latex_render(profile_build_dir)
    
    pdf_path = profile_build_dir / "resume.pdf"
    output_path = OUTPUT_DIR / pdf_fname

    move_pdf(pdf_path, output_path)

def main():
    args = get_args()

    if args.command == "build":
        compile_pdf(
            profile=args.profile,
            template=args.template,
            output_name=args.output or args.profile
        )
    elif args.command == "git":
        print("Git functionality is currently unavailable.")

if __name__ == "__main__":
    main()