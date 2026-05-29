#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[3]
RULERS_TEMPLATE_DIR = Path(__file__).resolve().parents[1]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCED_BLOCK_RE = re.compile(r"```([A-Za-z0-9_-]*)\n(.*?)\n```", re.DOTALL)

ROOT_DOCS_WITHOUT_METADATA = {
    Path("AGENTS.md"),
    Path("INDEX.md"),
    Path("PROJECT_PROFILE.template.md"),
    Path("README.md"),
}

CORE_EXPECTED_REFERENCES = (
    "core/HARD_CONSTRAINTS.md",
    "core/WORKFLOW.md",
    "core/DOC_GOVERNANCE.md",
    "core/RULER_MAINTENANCE.md",
    "core/GIT_COMMIT_CONVENTION.md",
)

HIGH_RISK_DOCUMENTS = (
    Path("backend/INDEX.md"),
    Path("database/INDEX.md"),
    Path("bootstrap/ACTIVATION_LEVELS.md"),
)

AGENTS_KNOWN_REFERENCE_ALIASES = {
    "PROJECT_PROFILE.md": Path("PROJECT_PROFILE.template.md"),
}


class ValidationError(Exception):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def template_rel(path: Path) -> Path:
    return path.relative_to(RULERS_TEMPLATE_DIR)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_markdown_files() -> list[Path]:
    return sorted(path for path in RULERS_TEMPLATE_DIR.rglob("*.md") if path.is_file())


def is_relative_markdown_target(raw_target: str) -> bool:
    target = raw_target.strip()
    return bool(target) and not target.startswith(("http://", "https://", "mailto:", "#"))


def clean_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    target = target.split("#", 1)[0]
    return unquote(target).strip()


def resolve_template_path(base_dir: Path, raw_target: str) -> Path:
    target = clean_link_target(raw_target)
    return (base_dir / target).resolve()


def is_inside_rulers_dir(path: Path) -> bool:
    resolved = path.resolve()
    return resolved == RULERS_TEMPLATE_DIR or RULERS_TEMPLATE_DIR in resolved.parents


def validate_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        for raw_target in LINK_RE.findall(read_text(path)):
            if not is_relative_markdown_target(raw_target):
                continue
            target = clean_link_target(raw_target)
            if not target:
                continue
            resolved = resolve_template_path(path.parent, target)
            if not resolved.exists() or not is_inside_rulers_dir(resolved):
                errors.append(f"Broken markdown link: {rel(path)} -> {raw_target}")
    return errors


def yaml_metadata_block(text: str) -> str | None:
    for language, body in FENCED_BLOCK_RE.findall(text):
        if language.strip().lower() == "yaml" and re.search(r"(?m)^metadata:\s*$", body):
            return body
    return None


def normalize_metadata_value(value: str) -> str:
    return value.split("#", 1)[0].strip().strip('"\'')


def extract_metadata_list(metadata_block: str, key: str) -> list[str] | None:
    values: list[str] = []
    found_key = False
    in_target_list = False

    for line in metadata_block.splitlines():
        stripped = line.strip()
        if stripped == f"{key}:":
            found_key = True
            in_target_list = True
            continue
        if stripped == f"{key}: []":
            found_key = True
            in_target_list = False
            continue
        if in_target_list and stripped.startswith("- "):
            value = normalize_metadata_value(stripped[2:])
            if value:
                values.append(value)
            continue
        if in_target_list and stripped and not stripped.startswith("-"):
            in_target_list = False

    if not found_key:
        return None
    return values


def is_authoritative_document(path: Path) -> bool:
    return template_rel(path) not in ROOT_DOCS_WITHOUT_METADATA


def validate_metadata(files: list[Path]) -> list[str]:
    errors: list[str] = []
    required_keys = ("applies_to", "trigger_keywords", "must_load_with")

    for path in files:
        if not is_authoritative_document(path):
            continue
        text = read_text(path)
        metadata_block = yaml_metadata_block(text)
        if metadata_block is None:
            errors.append(f"Missing fenced yaml metadata block: {rel(path)}")
            continue
        for key in required_keys:
            values = extract_metadata_list(metadata_block, key)
            if not values:
                errors.append(f"Missing or empty metadata {key}: {rel(path)}")
    return errors


def validate_metadata_paths(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if not is_authoritative_document(path):
            continue
        metadata_block = yaml_metadata_block(read_text(path))
        if metadata_block is None:
            continue
        for target in extract_metadata_list(metadata_block, "must_load_with") or []:
            resolved = resolve_template_path(path.parent, target)
            if resolved.suffix != ".md" or not resolved.is_file() or not is_inside_rulers_dir(resolved):
                errors.append(f"Broken metadata must_load_with path: {rel(path)} -> {target}")
    return errors


def known_ruler_references(files: list[Path]) -> dict[str, Path]:
    references: dict[str, Path] = {}
    for path in files:
        relative = template_rel(path)
        references[str(relative)] = path
        references[str(relative.with_suffix(""))] = path
        references[path.name] = path
    for alias, target in AGENTS_KNOWN_REFERENCE_ALIASES.items():
        references[alias] = RULERS_TEMPLATE_DIR / target
    return references


def extract_agents_example_references(text: str, files: list[Path]) -> list[str]:
    references = known_ruler_references(files)
    candidates: list[str] = []

    for _, block in FENCED_BLOCK_RE.findall(text):
        for raw_line in block.splitlines():
            line = re.sub(r"\s+\([^)]*\)\s*$", "", raw_line.strip())
            if not line:
                continue
            for token in re.split(r"\s+|->|[,+]", line):
                candidate = token.strip().strip("`.;:，。；：")
                if not candidate:
                    continue
                if candidate.endswith(".md") or candidate in references:
                    candidates.append(candidate)
    return candidates


def validate_agents_example_paths(files: list[Path]) -> list[str]:
    errors: list[str] = []
    agents_path = RULERS_TEMPLATE_DIR / "AGENTS.md"
    if not agents_path.is_file():
        return [f"Missing AGENTS entry: {rel(agents_path)}"]

    references = known_ruler_references(files)
    for candidate in extract_agents_example_references(read_text(agents_path), files):
        resolved = references.get(candidate)
        if resolved is None and candidate.endswith(".md"):
            resolved = (RULERS_TEMPLATE_DIR / candidate).resolve()
        if resolved is None or not resolved.is_file() or RULERS_TEMPLATE_DIR not in resolved.resolve().parents:
            errors.append(f"Broken AGENTS loading example reference: {rel(agents_path)} -> {candidate}")
    return errors


def validate_index_coverage(files: list[Path]) -> list[str]:
    errors: list[str] = []
    markdown_by_dir: dict[Path, list[Path]] = {}
    for path in files:
        markdown_by_dir.setdefault(path.parent, []).append(path)

    for index_path in sorted(path for path in files if path.name == "INDEX.md"):
        index_text = read_text(index_path)
        for sibling in sorted(markdown_by_dir.get(index_path.parent, [])):
            sibling_rel = template_rel(sibling)
            if sibling.name == "INDEX.md" or sibling_rel in ROOT_DOCS_WITHOUT_METADATA:
                continue
            if sibling.name not in index_text:
                errors.append(f"INDEX missing sibling markdown leaf reference: {rel(index_path)} -> {sibling.name}")
    return errors


def validate_core_references() -> list[str]:
    errors: list[str] = []
    agents_path = RULERS_TEMPLATE_DIR / "AGENTS.md"
    agents_text = read_text(agents_path) if agents_path.is_file() else ""
    for core_reference in CORE_EXPECTED_REFERENCES:
        if core_reference not in agents_text:
            errors.append(f"AGENTS missing core reference: {core_reference}")
    return errors


def validate_activation_levels() -> list[str]:
    errors: list[str] = []
    activation_path = RULERS_TEMPLATE_DIR / "bootstrap" / "ACTIVATION_LEVELS.md"
    if not activation_path.is_file():
        return [f"Missing activation levels document: {rel(activation_path)}"]

    activation_text = read_text(activation_path)
    for level in ("Level 0", "Level 1", "Level 2", "Level 3"):
        if level not in activation_text:
            errors.append(f"Activation levels document missing {level}: {rel(activation_path)}")
    return errors


def validate_high_risk_activation_language() -> list[str]:
    errors: list[str] = []
    activation_re = re.compile(r"\bLevel\s+[23]\b", re.IGNORECASE)
    for relative_path in HIGH_RISK_DOCUMENTS:
        path = RULERS_TEMPLATE_DIR / relative_path
        if not path.is_file():
            errors.append(f"Missing high-risk document: {rel(path)}")
            continue
        if not activation_re.search(read_text(path)):
            errors.append(f"High-risk document missing Level 2 or Level 3 activation language: {rel(path)}")
    return errors


def main() -> int:
    files = collect_markdown_files()
    errors: list[str] = []
    errors.extend(validate_links(files))
    errors.extend(validate_metadata(files))
    errors.extend(validate_metadata_paths(files))
    errors.extend(validate_agents_example_paths(files))
    errors.extend(validate_index_coverage(files))
    errors.extend(validate_core_references())
    errors.extend(validate_activation_levels())
    errors.extend(validate_high_risk_activation_language())

    if errors:
        print("Rulers template validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Rulers template validation passed.")
    print(f"Checked {len(files)} markdown files under {rel(RULERS_TEMPLATE_DIR)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())