from __future__ import annotations

import json
from pathlib import Path


def find_notebooks(repo_root: Path) -> list[Path]:
    return sorted(repo_root.rglob("*.ipynb"))


def has_output_data(output: dict) -> bool:
    data = output.get("data")
    return isinstance(data, dict) and len(data) > 0


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        return [f"Could not read notebook: {exc}"]

    cells = payload.get("cells", [])
    if not isinstance(cells, list):
        return ["Invalid format: 'cells' is not a list"]

    for idx, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            errors.append(f"Cell {idx}: invalid format")
            continue

        if cell.get("cell_type") != "code":
            continue

        outputs = cell.get("outputs", [])
        execution_count = cell.get("execution_count")

        if isinstance(outputs, list) and len(outputs) > 0:
            errors.append(f"Cell {idx}: contains outputs ({len(outputs)})")
            for out_idx, output in enumerate(outputs, start=1):
                if isinstance(output, dict) and has_output_data(output):
                    mime_types = sorted(output.get("data", {}).keys())
                    errors.append(
                        f"Cell {idx}, output {out_idx}: contains embedded data {mime_types}"
                    )

        if execution_count is not None:
            errors.append(
                f"Cell {idx}: execution_count={execution_count} (should be null)"
            )

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    notebooks = find_notebooks(repo_root)

    if not notebooks:
        print("No notebooks found. Validation OK.")
        return 0

    failures = 0
    for notebook in notebooks:
        relative_path = notebook.relative_to(repo_root)
        notebook_errors = validate_notebook(notebook)
        if notebook_errors:
            failures += 1
            print(f"\nNotebook not clean: {relative_path}")
            for err in notebook_errors:
                print(f"  - {err}")

    if failures:
        print(
            "\nValidation failed: there are notebooks with outputs, images, or execution_count set."
        )
        print(
            "Clean the notebooks before committing (e.g., with nbstripout or VS Code)."
        )
        return 1

    print("All notebooks are clean. Validation OK.")
    return 0
