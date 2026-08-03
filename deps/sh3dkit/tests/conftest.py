import pytest
from sh3d.model.Home import Home
from sh3d.FileLoader import FileLoader
from pathlib import Path

@pytest.fixture(scope="module")
def sh3d_path() -> Path:
    self_dir = Path(__file__).resolve().parent
    return self_dir.joinpath('assets/myHome.sh3d')

@pytest.fixture(scope="module")
def home(sh3d_path: Path) -> Home:
    with FileLoader(sh3d_path) as fl:
        return fl.home
