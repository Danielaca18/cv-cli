from pathlib import Path
from argparse import ArgumentParser, Namespace
from .constants import DEFAULT_PROFILE, DEFAULT_TEMPLATE, DEFAULT_OUTPUT_FNAME, DEFAULT_PROFILE_REPO
from .render import compile_pdf
from .git import git_init, git_clone, git_sync
from .profiles import new_profile, edit_profile, del_profile, init_profiles, sync_profiles, clone_profiles

def build_parser(subparser):
    build = subparser.add_parser(name="build", help="Generate latex resumes from a yaml profile.")
    build.add_argument("-p", "--profile", help="Sets profile for build.", default=DEFAULT_PROFILE)
    build.add_argument("-t", "--template", help="Sets resume template for build.", default=DEFAULT_TEMPLATE)
    build.add_argument("-o", "--output", help="Sets output file path", default=DEFAULT_OUTPUT_FNAME, type=Path)

def profiles_parser(subparser):
    profiles = subparser.add_parser("profiles", help="Manage and sync profile data.")
    subparser = profiles.add_subparsers(dest="profiles_command", required=True)

    profiles_new = subparser.add_parser("new", help="Create new profile.")
    profiles_new.add_argument("name", help="Name of profile.")
    profiles_new.add_argument("-s", "--src", help="Base profile to copy from.", default=None)

    profiles_edit = subparser.add_parser("edit", help="Edit profile.")
    profiles_edit.add_argument("name", nargs="?", help="Name of profile.", default=None)
    profiles_edit.add_argument("-e", "--editor", help="Editor cmdline tool", default="code")

    profiles_del = subparser.add_parser("del", help="Delete profile.")
    profiles_del.add_argument("name", help="Name of profile.")

    profiles_init = subparser.add_parser("init", help="Initialize profiles repository.")
    profiles_init.add_argument("name", nargs="?", help="Name of repo.", default=DEFAULT_PROFILE_REPO)
    profiles_init.add_argument("-p", "--public", help="Make repo public.", action="store_true")

    # profile_sync
    subparser.add_parser("sync", help="Sync profiles with remote.")

    profiles_clone = subparser.add_parser("clone", help="Clone profiles from remote.")
    profiles_clone.add_argument("remote", help="Url to remote.")
    profiles_clone.add_argument("-f", "--force", help="Forces clone (Removes existing repo.)", action="store_true")

def templates_parser(subparser):
    raise NotImplementedError

def get_args() -> Namespace:
    parser = ArgumentParser(prog="resume", description="Command-line tool to generate resumes from YAML and LaTeX templates")
    subparser = parser.add_subparsers(dest="command", required=True)

    build_parser(subparser)
    profiles_parser(subparser)
    
    return parser.parse_args()

def run_profiles(args):
    if args.profiles_command == "new":
        new_profile(args.name, args.src)
    elif args.profiles_command == "edit":
        edit_profile(args.name, args.editor)
    elif args.profiles_command == "del":
        del_profile(args.name)
    elif args.profiles_command == "init":
        init_profiles(args.name, args.public)
    elif args.profiles_command == "sync":
        sync_profiles()
    elif args.profiles_command == "clone":
        clone_profiles(args.remote, args.force)

def run_templates(args):
    raise NotImplementedError

def main():
    args = get_args()

    if args.command == "build":
        compile_pdf(
            profile=args.profile,
            template=args.template,
            output_name=args.output
        )
    elif args.command == "git":
        print("Git functionality is currently unavailable.")

    elif args.command == "profiles":
        run_profiles(args)
    
    elif args.command == "templates":
        run_templates(args)