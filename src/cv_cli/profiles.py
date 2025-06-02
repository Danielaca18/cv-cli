from .io import edit_file
from .git import git_init, git_sync, git_clone
from .constants import PROFILES_DIR

def new_profile(profile_name:str, src_profile:str=None) -> None:
    """Creates a new profile.

    Args:
        profile_name (str): Profile name.
        src_profile (str, optional): Source profile name. Defaults to None.
    """
    profile_path = PROFILES_DIR / f"{profile_name}.yaml"

    if profile_path.exists():
        print(f"[Error]: Profile {profile_name} already exists.")
        return
    
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.touch()
    if src_profile:
        src_path = PROFILES_DIR / f"{src_profile}.yaml"
        if not src_path.exists():
            print(f"[Error]: Source profile {profile_name} does not exist.")
            return
        profile_path.write_text(src_path.read_text())

def edit_profile(editor_cmd:str, profile_name:str=None) -> None:
    """Opens code editor in profile page.

    Args:
        editor_cmd (str): Command line editor command.
        profile_name (str, optional): Profile name. Defaults to None.
    """
    profile_path = PROFILES_DIR
    if profile_name:
        profile_path = profile_path / f"{profile_name}.yaml"

    if not profile_path.exists():
        print(f"[Error]: Profile {profile_name} does not exist.")
        return
    edit_file(profile_path, editor_cmd)

def del_profile(profile_name:str) -> None:
    """Deletes specified profile.

    Args:
        profile_name (str): Profile name.
    """
    profile_path = PROFILES_DIR / f"{profile_name}.yaml"

    if not profile_path.exists():
        print(f"[Error]: Profile {profile_name} does not exist.")
    profile_path.unlink(missing_ok=True)

def init_profile(repo_name:str, public:bool) -> None:
    """Initializes profiles repo.

    Args:
        repo_name (str): Repo name.
        public (bool): Flag public/private repo.
    """
    git_init(PROFILES_DIR, repo_name, public)

def sync_profile() -> None:
    """Syncs profile repo with remote.
    """
    git_sync(PROFILES_DIR)

def clone_profile(remote:str, force:bool) -> None:
    """Clones profile repo from remote.

    Args:
        remote (str): URL to source repo.
        force (bool): Flag to force clone (Deletes pre-existing repo).
    """
    git_clone(remote, PROFILES_DIR, force)