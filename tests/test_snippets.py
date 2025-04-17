import importlib.util
import sys
from pathlib import Path
from shutil import copy2

import pytest

paths = Path("drawBotGrid/docs").glob("snippet_*.py")


@pytest.mark.parametrize("file_path", paths)
def test_snippets(tmp_path: Path, file_path: Path) -> None:
    tmp_snippet_path = copy2(file_path, tmp_path / file_path.name)
    no_save_code = tmp_snippet_path.read_text().replace('saveImage(out_path, {"imageResolution": 144})', "")
    tmp_snippet_path.write_text(no_save_code)
    spec = importlib.util.spec_from_file_location(tmp_snippet_path.stem, tmp_snippet_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules["module.name"] = mod
    spec.loader.exec_module(mod)  # type: ignore
