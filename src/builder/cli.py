import argparse
from .constants import DEFAULT_PROFILE, DEFAULT_TEMPLATE

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="resume")
    subparser = parser.add_subparsers(dest="command", required=True)

    build_parser = subparser.add_parser(name="build", help="Generate latex resumes from a yaml profile.")
    git_parser = subparser.add_parser(name="git", help="Sync profiles and templates with git.")

    build_parser.add_argument("-p", "--profile", default=DEFAULT_PROFILE)
    build_parser.add_argument("-t", "--template", default=DEFAULT_TEMPLATE)
    build_parser.add_argument("-o", "--output")
    
    return parser.parse_args()
