"""Acceptance tests for Internal Data Storage & Stroke Loader (Task 2.0)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from chinese_chars.models import CharacterData
from chinese_chars.stroke import INTERNAL_STORAGE_DIR, StrokeFileLoader


# ── Fixtures ────────────────────────────────────────────────────────

@pytest.fixture()
def valid_data_file(tmp_path: Path) -> Path:
    """Create a minimal valid internal JSON file for 'test' character."""
    fake_dir = tmp_path / "characters"
    fake_dir.mkdir(parents=True)
    
    data = {
        "character": "永",
        "stroke_count": 1,
        "strokes": [
            {
                "order": 1,
                "path": [0.0, 0.0, 1.0, 1.0] 
            }
        ]
    }
    
    filepath = fake_dir / "永.json"
    filepath.write_text(json.dumps(data))
    return filepath


def _create_valid_json(filepath: Path) -> None:
    """Helper to write basic valid JSON."""
    content = {
        "character": "田",
        "stroke_count": 1, 
        "strokes": [
            {"order": 1, "path": [0.0, 0.0, 1.0, 1.0]}
        ]
    }
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(json.dumps(content))


# ── Tests: Loader Logic ─────────────────────────────────────────────

def test_load_character_data(valid_data_file):
    """Verify full loading of valid internal data into CharacterData model."""
    loader = StrokeFileLoader(storage_dir=valid_data_file.parent)
    
    res = loader.load("永")
    assert isinstance(res, CharacterData), "Should return CharacterData model"
    assert res.char == "永"
    assert len(res.strokes) == 1
    
    stroke = res.strokes[0]
    assert len(stroke.points) == 2  # [x,y], [x,y] -> 2 points

def test_loader_raises_on_missing_file():
    """Loader should fail loudly when internal data is not found."""
    loader = StrokeFileLoader(storage_dir=_fake_temp_dir())
    
    with pytest.raises(KeyError, match="Stroke data not found"):
        loader.load("不存在") # "永" won't exist in empty temp dir

def test_loader_loads_real_data():
    """Test loading actual file from internal storage directory defined in code."""
    target_char = "一"
    
    # Ensure there's a copy of the real data for testing, or just read directly
    real_file = INTERNAL_STORAGE_DIR / f"{target_char}.json"
    if not real_file.exists():  # Skip if we don't have real file (should exist based on Task 2.0)
        pytest.skip(f"Real internal storage file missing: {real_file}")
    
    loader = StrokeFileLoader(storage_dir=INTERNAL_STORAGE_DIR)
    assert loader.has_char(target_char)
    
    result = loader.load(target_char)
    assert result.char == target_char



# ── Helpers & Configs ───────────────────────────────────────────────

def _fake_temp_dir():
    import tempfile
    
    return Path(tempfile.mkdtemp()).parent
