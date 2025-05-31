from .constants import TEMPLATES_DIR
from .io import copy_dir, edit_file
from .git import git_clone, git_init, git_sync

def new_template(template_name, src_template):
    template_path = TEMPLATES_DIR / template_name
    src_path = TEMPLATES_DIR / src_template

    if template_path.exists():
        print(f"[Error]: Profile {template_name} already exists.")
        return
    
    template_path.mkdir(parents=True, exist_ok=True)
    if src_template:
        copy_dir(src_path, template_path)

def edit_template(template_name, editor_cmd):
    template_path = TEMPLATES_DIR
    if template_name:
        template_path = template_path / template_name
    
    if not template_path:
        print(f"[Error]: Template {template_name} does not exist.")
        return
    edit_file(template_path, editor_cmd)

def del_template(template_name):
    template_path = TEMPLATES_DIR / f"{template_name}.yaml"

    if not template_path.exists():
        print(f"[Error]: Template {template_name} does not exist.")
    template_path.unlink(missing_ok=True)

def init_template(template_name, public:bool):
    template_path = TEMPLATES_DIR / template_name
    git_init(template_path, template_name, public)

def sync_template(template_name):
    template_path = TEMPLATES_DIR / template_name
    git_sync(template_path)

def clone_template(remote, template_name, force:bool):
    template_path = TEMPLATES_DIR / template_name
    git_clone(remote, template_path, force)