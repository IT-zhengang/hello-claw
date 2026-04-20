#!/usr/bin/env python3
"""
Locate the latest webpage payload JSON from common temporary directories.
"""

import argparse
import json
from pathlib import Path


DEFAULT_DIRS = [
    Path.cwd(),
    Path('/tmp'),
    Path.home() / 'Downloads',
]


def iter_candidates(search_dirs, suffixes):
    seen = set()
    for directory in search_dirs:
        if not directory.exists() or not directory.is_dir():
            continue
        for path in directory.iterdir():
            if not path.is_file():
                continue
            if path in seen:
                continue
            seen.add(path)
            if any(path.name.endswith(suffix) for suffix in suffixes):
                yield path


def main():
    parser = argparse.ArgumentParser(
        description='Find the most recent webpage payload JSON file.'
    )
    parser.add_argument(
        '--dir',
        action='append',
        dest='dirs',
        help='Extra directory to search. Can be passed multiple times.',
    )
    parser.add_argument(
        '--suffix',
        action='append',
        dest='suffixes',
        help='Filename suffix to match. Defaults to _payload.json.',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Print a JSON object instead of a plain path.',
    )
    args = parser.parse_args()

    search_dirs = list(DEFAULT_DIRS)
    if args.dirs:
        search_dirs.extend(Path(d).expanduser() for d in args.dirs)

    suffixes = args.suffixes or ['_payload.json']

    candidates = list(iter_candidates(search_dirs, suffixes))
    if not candidates:
        raise SystemExit('No payload JSON files found')

    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    info = {
        'path': str(latest),
        'name': latest.name,
        'size': latest.stat().st_size,
        'mtime': latest.stat().st_mtime,
    }

    if args.json:
        print(json.dumps(info, ensure_ascii=False))
    else:
        print(info['path'])


if __name__ == '__main__':
    main()
