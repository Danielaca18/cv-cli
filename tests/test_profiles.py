import pytest
from unittest.mock import patch
from pathlib import Path

from src.cv_cli.profiles import new_profile, edit_profile, del_profile, init_profile, sync_profile, clone_profile

@pytest.fixture
def tmp_profiles_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("src.cv_cli.constants.PROFILES_DIR", tmp_path)
    monkeypatch.setattr("src.cv_cli.profiles.PROFILES_DIR", tmp_path)
    yield tmp_path

def test_new_profile_creates(tmp_profiles_dir):
    profile_name = "test"
    new_profile(profile_name, None)
    profile_path = tmp_profiles_dir / f"{profile_name}.yaml"
    assert profile_path.exists()

def test_new_profile_with_src(tmp_profiles_dir):
    src_name = "src"
    src_path = tmp_profiles_dir / f"{src_name}.yaml"
    src_path.write_text("test")
    profile_name = "test"
    
    new_profile(profile_name, src_name)
    profile_path = tmp_profiles_dir / f"{profile_name}.yaml"
    assert profile_path.read_text() == "test"

def test_new_profile_with_src_invalid(tmp_profiles_dir, capsys):
    src_name = "src"
    profile_name = "test"
    new_profile(profile_name, src_name)
    captured = capsys.readouterr()
    assert "not exist" in captured.out

def test_new_profile_exists(tmp_profiles_dir, capsys):
    profile_name = "test"
    profile_path = tmp_profiles_dir / f"{profile_name}.yaml"
    profile_path.touch()

    new_profile(profile_name, None)
    captured = capsys.readouterr()
    assert "already exists" in captured.out

def test_edit_profile_call(tmp_profiles_dir):
    profile_name = "test"
    profile_path = tmp_profiles_dir / f"{profile_name}.yaml"
    profile_path.touch()

    with patch("src.cv_cli.profiles.edit_file") as mock:
        edit_profile("code", profile_name)
        mock.assert_called_once_with(profile_path, "code")

def test_edit_profile_invalid(tmp_profiles_dir, capsys):
    edit_profile("invalid", "code")
    captured = capsys.readouterr()
    assert "not exist" in captured.out

def test_del_profile_deletes(tmp_profiles_dir):
    profile_name = "test"
    profile_path = tmp_profiles_dir / f"{profile_name}.yaml"
    profile_path.touch()
    del_profile(profile_name)
    assert not profile_path.exists()

def test_del_profile_invalid(tmp_profiles_dir, capsys):
    del_profile("invalid")
    captured = capsys.readouterr()
    assert "not exist" in captured.out

def test_init_profiles_calls(tmp_profiles_dir):
    with patch("src.cv_cli.profiles.git_init") as mock:
        init_profile("test", True)
        mock.assert_called_once_with(tmp_profiles_dir, "test", True)

def test_sync_profiles_calls(tmp_profiles_dir):
    with patch("src.cv_cli.profiles.git_sync") as mock:
        sync_profile()
        mock.assert_called_once()

def test_clone_profiles_calls(tmp_profiles_dir):
    with patch("src.cv_cli.profiles.git_clone") as mock:
        clone_profile("test.com", True)
        mock.assert_called_once_with("test.com", tmp_profiles_dir, True)