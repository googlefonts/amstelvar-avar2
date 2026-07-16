import json
import os
import plistlib


from pathlib import Path
from fontParts.world import OpenFont

# Folder containing this script
SCRIPT_DIR = Path(__file__).resolve().parent

# Repository root
ROOT = SCRIPT_DIR.parent.parent

# Default UFO
DEFAULT_UFO = ROOT / "Sources" / "Roman" / "AmstelvarA2-Roman_wght400.ufo"

SETS_FILE = (
    ROOT
    / "Sources"
    / "Roman"
    / "AmstelvarA2-Roman.roboFontSets"
)

OUTPUT_FILE = (
    ROOT
    / "Tools"
    / "proofing"
    / "cyrillicProofGlyphs.json"
)

UPPERCASE_PARTS = [
    "Obarcyr-stroke",
    "U-stroke",
    "Ha-stroke",
    "Cy-descendercomb.case",
    "horizontalbar",
    "horizontalbarH",
    "Yu-dash.case",
]

LOWERCASE_PARTS = [
    "horizontalbarlc",
    "ustraight-stroke",
    "yu.bgr-stroke",
    "cy-descendercomb",
    "ha-stroke",
    "obarcyr-stroke",
    "yu-i",
    "idot",
]

UPPERCASE_ACCENTS = [
    "breve.cyrcomb.case",
    "Yi-dieresiscomb.case",
]

LOWERCASE_ACCENTS = [
    "breve.cyrcomb",
    "yi-dieresiscomb",
]


def find_named_item(items, name):
    for item in items:
        if item.get("smartSetName") == name:
            return item

    raise KeyError(f"Smart set not found: {name}")


def get_glyph_names(data, parent_name, child_name):
    parent = find_named_item(data, parent_name)
    child = find_named_item(parent.get("group", []), child_name)

    return child.get("glyphNames", [])


def validate_selected_names(selected_names, available_names, group_path):
    missing = [
        glyph_name
        for glyph_name in selected_names
        if glyph_name not in available_names
    ]

    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(
            f"These glyphs were not found in {group_path}: "
            f"{missing_text}"
        )


def unique_in_order(glyph_names):
    return list(dict.fromkeys(glyph_names))


def main():
    with open(SETS_FILE, "rb") as file:
        smart_sets = plistlib.load(file)

    uppercase_cyrillic = get_glyph_names(
        smart_sets,
        "uppercase",
        "cyrillic",
    )

    lowercase_cyrillic = get_glyph_names(
        smart_sets,
        "lowercase",
        "cyrillic",
    )

    all_uppercase_parts = get_glyph_names(
        smart_sets,
        "uppercase",
        "parts",
    )

    all_lowercase_parts = get_glyph_names(
        smart_sets,
        "lowercase",
        "parts",
    )

    all_uppercase_accents = get_glyph_names(
        smart_sets,
        "uppercase",
        "accents comb",
    )

    all_lowercase_accents = get_glyph_names(
        smart_sets,
        "lowercase",
        "accents comb",
    )

    validate_selected_names(
        UPPERCASE_PARTS,
        all_uppercase_parts,
        "uppercase/parts",
    )

    validate_selected_names(
        LOWERCASE_PARTS,
        all_lowercase_parts,
        "lowercase/parts",
    )

    validate_selected_names(
        UPPERCASE_ACCENTS,
        all_uppercase_accents,
        "uppercase/accents comb",
    )

    validate_selected_names(
        LOWERCASE_ACCENTS,
        all_lowercase_accents,
        "lowercase/accents comb",
    )

    cyrillic_proof_glyphs = unique_in_order(
        uppercase_cyrillic
        + lowercase_cyrillic
        + UPPERCASE_PARTS
        + LOWERCASE_PARTS
        + UPPERCASE_ACCENTS
        + LOWERCASE_ACCENTS
    )

    output_folder = os.path.dirname(OUTPUT_FILE)

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    cyrillic_proof_glyphs = unique_in_order(
        uppercase_cyrillic
        + lowercase_cyrillic
        + UPPERCASE_PARTS
        + LOWERCASE_PARTS
        + UPPERCASE_ACCENTS
        + LOWERCASE_ACCENTS
    )

    # Remove glyphs that contain components.
    font = OpenFont(str(DEFAULT_UFO), showInterface=False)

    filtered_glyphs = []

    for glyph_name in cyrillic_proof_glyphs:
        if glyph_name not in font:
            print(f"Missing glyph, skipping: {glyph_name}")
            continue

        if font[glyph_name].components:
            print(f"Component glyph, skipping: {glyph_name}")
            continue

        filtered_glyphs.append(glyph_name)

    font.close()

    cyrillic_proof_glyphs = filtered_glyphs

    # Save the filtered list.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(cyrillic_proof_glyphs, file, indent=2, ensure_ascii=False)

    print(
        f"Saved {len(cyrillic_proof_glyphs)} glyph names to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()