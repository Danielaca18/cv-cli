from .io import onDelError
from .constants import PROFILES_DIR
from pathlib import Path
from subprocess import run, CalledProcessError
from shutil import rmtree

def get_repo_url(repo_name:str) -> None:
    """Retrieves url of the specified repo.

    Args:
        repo_name (str): Name of git repo.

    Raises:
        FileNotFoundError: Repo does not exists.
    """
    result = run(["gh", "repo", "view", repo_name, "--json", "url", "--jq", ".url"], capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        return url
    raise FileNotFoundError("Repo could not be found.")

def git_init(repo_dir:Path|str, repo_name:str, public:bool) -> None:
    """Initialize git repo.

    Args:
        repo_dir (Path | str): Repo directory.
        repo_name (str): Name of repo.
        public (bool): Repo public/private flag.
    """
    repo_type = "--public" if public else "--private"
    if not repo_dir.exists():
        repo_dir.mkdir(parents=True)
    try:
        run(["gh", "repo", "create", repo_name, repo_type], cwd=repo_dir, check=True)
        run('echo "#CV-CLI" >> README.md', shell=True, check=True)
    except Exception:
        pass

    run(["git", "init"], cwd=repo_dir, check=True)
    print(f"Initialized repo in {repo_dir}.")

    try:
        repo_url = get_repo_url(repo_name)
    except FileNotFoundError:
        print("Failed to retrieve remote.")
        return

    run(["git", "remote", "remove", "origin"], cwd=repo_dir, check=False)
    run(["git", "remote", "add", "origin", repo_url], cwd=repo_dir, check=True)
    print(f"Updated remote to {repo_url}")

    git_sync(repo_dir)

def git_clone(remote_url:str, repo_dir:Path|str, force:bool) -> None:
    """Clones git repo.

    Args:
        remote_url (str): URL of source repo.
        repo_dir (Path | str): Repo directory.
        force (bool): Flag to force clone (Deletes pre-existing dir).
    """
    if force:
        rmtree(repo_dir, onerror=onDelError)
    run(["git", "clone", remote_url, repo_dir], check=True)

def git_pull(repo_dir:Path|str) -> None:
    """Updates from git remote.

    Args:
        repo_dir (Path|str): Repo directory.
    """
    run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True)
    run(["git", "pull", "origin", "main"], cwd=repo_dir, check=True)

def git_push(repo_dir:Path|str) -> None:
    """Pushes changes to git remote.

    Args:
        repo_dir (Path|str): Repo directory.
    """
    run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True)
    run(["git", "add", "."], cwd=repo_dir, check=True)
    try:
        run(["git", "commit", "-m", "sync: auto sync"], cwd=repo_dir, check=True)
    except CalledProcessError as e:
        if e.returncode > 1:
            print("[Error]: Commit failed.")
    run(["git", "push", "-u", "origin", "main"], cwd=repo_dir, check=True)

def git_sync(repo_dir:Path|str) -> None:
    """Syncs git repo with remote.

    Args:
        repo_dir (Path|str): Repo directory.
    """
    git_push(repo_dir)
    git_pull(repo_dir)