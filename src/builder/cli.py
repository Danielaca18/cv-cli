import argparse
from .constants import DEFAULT_PROFILE, DEFAULT_TEMPLATE

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate latex resumes from a yaml profile.")
    parser.add_argument("-p", "--profile", default=DEFAULT_PROFILE)
    parser.add_argument("-t", "--template", default=DEFAULT_TEMPLATE)
    parser.add_argument("-o", "--output")
    return parser.parse_args()
