import re
from pathlib import Path

ETL = Path(__file__).resolve().parents[1]
CORE = ETL / "core"


def test_every_module_has_md_with_three_sections():
    for py in CORE.glob("*.py"):
        if py.name.startswith(("test_", "__")):
            continue
        text = py.with_suffix(".md").read_text()
        assert all(h in text for h in ("## 语义", "## 接口", "## 示例")), py.name


def test_handoff_links_resolve_and_requirements_pin_versions():
    h = (ETL / "handoff.md").read_text()
    for target in re.findall(r"\]\(([^)#]+)\)", h):
        if not target.startswith("http"):
            assert (ETL / target).exists(), target
    r = (ETL / "requirements.txt").read_text().lower()
    for pin in ["daft==0.7.26", "duckdb==2.0.0", "pyarrow==25.0.1", "gemmi==0.7.5",
                "pytest==9.2.0"]:
        assert pin in r
    assert re.search(r"^anarci==2026\.2\.13\.2", r, re.M)
