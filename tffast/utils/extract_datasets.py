#!/usr/bin/env python3
"""
extract_datasets.py - Text-Fabric Extractor (created for upgrading Synoptic Viewer (https://github.com/cbop-dev/synoptic-viewer) to v.1.0)
Extracts verse texts, word tokens (with lemma IDs), apparatus notes,
full lexemes, and concordance data from Text-Fabric datasets into static JSON.
"""

import sys, os, json, argparse, time
from pathlib import Path

# Add tf-fast directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from tffast.MyDatasets import getDataset
from tffast.tfData.SblGntAppNotes2 import SblGntAppNotes

# Standard 27 New Testament books
NT_BOOKS_MAP = {
    "Matthew": "Matt",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Romans": "Rom",
    "1_Corinthians": "1 Cor",
    "2_Corinthians": "2 Cor",
    "Galatians": "Gal",
    "Ephesians": "Eph",
    "Philippians": "Phil",
    "Colossians": "Col",
    "1_Thessalonians": "1 Thess",
    "2_Thessalonians": "2 Thess",
    "1_Timothy": "1 Tim",
    "2_Timothy": "2 Tim",
    "Titus": "Titus",
    "Philemon": "Phlm",
    "Hebrews": "Heb",
    "James": "Jas",
    "1_Peter": "1 Pet",
    "2_Peter": "2 Pet",
    "1_John": "1 John",
    "2_John": "2 John",
    "3_John": "3 John",
    "Jude": "Jude",
    "Revelation": "Rev",
}

GOSPELS = ["Matthew", "Mark", "Luke", "John"]

def build_app_notes_map():
    """Index apparatus notes by (book, f'{chap}:{v}') for O(1) lookup."""
    notes_map = {}
    for entry in SblGntAppNotes:
        book = entry.get("book", "")
        cv = entry.get("cv", "")
        note = entry.get("note", "").strip()
        if book and cv and note:
            key = f"{book} {cv}"
            if key not in notes_map:
                notes_map[key] = []
            notes_map[key].append(note)
    return notes_map

def extract_dataset(dbname, output_dir, app_notes_map=None):
    print(f"\n==========================================")
    print(f"Extracting Dataset: {dbname}")
    print(f"==========================================")
    start_time = time.time()

    tfData = getDataset(dbname)
    if not tfData:
        print(f"ERROR: Could not load dataset '{dbname}'!")
        return False

    api = tfData.api
    dest_dir = Path(output_dir) / dbname
    books_dir = dest_dir / "books"
    dest_dir.mkdir(parents=True, exist_ok=True)
    books_dir.mkdir(parents=True, exist_ok=True)

    # 1. Extract Lexemes Lexicon
    print("Extracting lexemes lexicon...")
    lexemes_dict = {}
    if hasattr(tfData, 'lexemes') and tfData.lexemes:
        for lemma_key, lex in tfData.lexemes.items():
            pos_val = lex.pos if hasattr(lex, 'pos') else None
            pos_str = ""
            if pos_val is not None:
                if isinstance(pos_val, list) and len(pos_val) > 0:
                    pos_str = str(pos_val[0])
                else:
                    pos_str = str(pos_val)

            lexemes_dict[str(lex.id)] = {
                "id": lex.id,
                "lemma": lex.lemma,
                "gloss": lex.gloss if lex.gloss else "",
                "pos": pos_str,
                "total": lex.total if hasattr(lex, 'total') else 0,
                "beta": lex.beta if hasattr(lex, 'beta') and lex.beta else "",
                "plain": lex.plain if hasattr(lex, 'plain') and lex.plain else lex.lemma
            }
    
    with open(dest_dir / "lexemes.json", "w", encoding="utf-8") as f:
        json.dump(lexemes_dict, f, ensure_ascii=False)
    print(f"  Saved {len(lexemes_dict)} lexemes to {dest_dir / 'lexemes.json'}")

    # 2. Extract Books, Chapters, Verses and build Concordance Index
    print("Extracting books, verses, and concordance...")
    concordance = {}
    seen_verse_per_lex = {}
    for lex_id in lexemes_dict.keys():
        concordance[lex_id] = {
            "total": 0,
            "bookcounts": {},
            "refs": []
        }
        seen_verse_per_lex[lex_id] = set()

    gospels_combined = {}
    books_meta = {}

    # Match NT books in tfData.booksDict
    for bookNode, bInfo in tfData.booksDict.items():
        raw_name = bInfo.get("name", "")
        std_name = None
        abbrev = None
        for nt_name, nt_abbrev in NT_BOOKS_MAP.items():
            syns = [s.lower().replace("_", " ") for s in bInfo.get("syn", [])] + [
                bInfo.get("name", "").lower().replace("_", " "),
                bInfo.get("abbrev", "").lower().replace("_", " "),
            ]
            check_name = nt_name.lower().replace("_", " ")
            check_abbrev = nt_abbrev.lower().replace("_", " ")
            if check_name in syns or check_abbrev in syns or raw_name == nt_name:
                std_name = nt_name
                abbrev = nt_abbrev
                break

        if not std_name:
            continue

        print(f"  Processing {std_name} ({abbrev}, node {bookNode})...")
        book_data = {
            "book": std_name,
            "abbrev": abbrev,
            "chapters": {}
        }

        # Iterate chapters
        chapter_nodes = api.L.d(bookNode, "chapter")
        for cNode in chapter_nodes:
            cNum = str(api.F.chapter.v(cNode))
            book_data["chapters"][cNum] = {}

            # Iterate verses
            verse_nodes = api.L.d(cNode, "verse")
            for vNode in verse_nodes:
                vNum = str(api.F.verse.v(vNode))
                ref_str = f"{abbrev} {cNum}:{vNum}"

                # Text
                raw_text = tfData.getText(vNode).strip()
                formatted_text = f"({vNum}) {raw_text}" if raw_text else ""

                # Words
                words_list = []
                word_nodes = api.L.d(vNode, "word")
                for wNode in word_nodes:
                    wText = tfData.getText(wNode).strip()
                    if not wText:
                        continue
                    lex_id = tfData.getLexID(wNode) if hasattr(tfData, 'getLexID') else 0
                    words_list.append({
                        "word": wText,
                        "id": lex_id
                    })

                    # Concordance update
                    str_lex_id = str(lex_id)
                    if str_lex_id in concordance:
                        concordance[str_lex_id]["total"] += 1
                        book_key = str(bookNode)
                        concordance[str_lex_id]["bookcounts"][book_key] = concordance[str_lex_id]["bookcounts"].get(book_key, 0) + 1
                        if ref_str not in seen_verse_per_lex[str_lex_id]:
                            seen_verse_per_lex[str_lex_id].add(ref_str)
                            concordance[str_lex_id]["refs"].append(ref_str)

                # Apparatus notes
                notes_list = []
                if app_notes_map and dbname == "sblgnt":
                    lookup_key = f"{std_name} {cNum}:{vNum}"
                    if lookup_key in app_notes_map:
                        notes_list = app_notes_map[lookup_key]

                book_data["chapters"][cNum][vNum] = {
                    "text": formatted_text,
                    "raw_text": raw_text,
                    "reference": ref_str,
                    "words": words_list,
                    "notes": notes_list
                }

        # Save individual book file
        book_file = books_dir / f"{abbrev.replace(' ', '_')}.json"
        with open(book_file, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False)

        if std_name in GOSPELS:
            gospels_combined[abbrev] = book_data

        books_meta[abbrev] = {
            "name": std_name,
            "abbrev": abbrev,
            "node": bookNode,
            "chapters": len(book_data["chapters"])
        }

    # Save gospels combined file for instant synopsis loading
    if gospels_combined:
        gospels_file = dest_dir / "gospels.json"
        with open(gospels_file, "w", encoding="utf-8") as f:
            json.dump(gospels_combined, f, ensure_ascii=False)
        print(f"  Saved gospels combined to {gospels_file}")

    # Save books index metadata
    with open(dest_dir / "books.json", "w", encoding="utf-8") as f:
        json.dump(books_meta, f, ensure_ascii=False, indent=2)

    # Save concordance
    with open(dest_dir / "concordance.json", "w", encoding="utf-8") as f:
        json.dump(concordance, f, ensure_ascii=False)
    print(f"  Saved concordance to {dest_dir / 'concordance.json'}")

    elapsed = time.time() - start_time
    print(f"Finished {dbname} in {elapsed:.2f} seconds.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Extract Text-Fabric datasets to static JSON for Synoptic-Viewer 2.0")
    parser.add_argument("--datasets", default="sblgnt,n1904,vulgate,web", help="Comma-separated dataset names")
    parser.add_argument("--output", default="../synoptic-viewer/static/data", help="Output directory for static data")
    args = parser.parse_args()

    datasets = [d.strip() for d in args.datasets.split(",") if d.strip()]
    output_path = Path(args.output).resolve()
    print(f"Starting extraction for datasets: {datasets}")
    print(f"Output directory: {output_path}")

    app_notes = build_app_notes_map()
    print(f"Loaded {len(app_notes)} apparatus notes for SBLGNT.")

    for ds in datasets:
        success = extract_dataset(ds, output_path, app_notes)
        if not success:
            print(f"Warning: Failed to extract dataset {ds}")

    print("\n==========================================")
    print("ALL DATASETS EXTRACTED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    main()
