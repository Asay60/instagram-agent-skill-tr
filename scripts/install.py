#!/usr/bin/env python3
"""Install this checkout's skill directories without third-party dependencies.

Never overwrites an existing skill directory without --overwrite. Existing
directories are renamed to backups; personal voice/log data is never touched.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def install(destination, overwrite=False):
    destination = Path(destination).expanduser().resolve()
    sources = sorted((ROOT / 'skills').glob('ig-*')) + [ROOT / 'skills' / '_instagram_agent_shared']
    if destination == ROOT / 'skills' or (ROOT / 'skills') in destination.parents:
        raise ValueError('Installation target cannot be the source skill tree.')
    for src in sources:
        dst = destination / src.name
        if dst.exists() and not overwrite:
            raise FileExistsError(f'{dst} already exists; inspect it first, then use --overwrite if intended.')
        if dst.is_symlink():
            raise ValueError(f'Refusing to replace a symlink: {dst}')
    destination.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix='.instagram-install-', dir=destination))
    installed, backups = [], []
    try:
        # Prepare every file before touching any installed skill.
        for src in sources:
            shutil.copytree(src, staged / src.name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        for src in sources:
            dst = destination / src.name
            if dst.exists():
                # Backups sit outside the discovery directory: no duplicate skills.
                backup_root = destination.parent / 'instagram-agent-backups' / stamp
                backup_root.mkdir(parents=True, exist_ok=True)
                backup = backup_root / src.name
                dst.rename(backup)
                backups.append((dst, backup))
            (staged / src.name).rename(dst)
            installed.append(dst)
    except Exception:
        for dst in reversed(installed):
            shutil.rmtree(dst)
        for dst, backup in reversed(backups):
            backup.rename(dst)
        raise
    finally:
        shutil.rmtree(staged)
    return installed, backups


def main():
    p = argparse.ArgumentParser(description='Instagram Agent TR: Codex / Claude skill installer')
    p.add_argument('--agent', choices=('codex', 'claude'), default='codex')
    p.add_argument('--scope', choices=('user', 'project'), default='user')
    p.add_argument('--dest', type=Path, help='Explicit skills directory; overrides --agent/--scope')
    p.add_argument('--overwrite', action='store_true', help='Back up and replace existing pack folders')
    args = p.parse_args()
    host = '.agents' if args.agent == 'codex' else '.claude'
    base = Path.home() if args.scope == 'user' else Path.cwd()
    dest = args.dest or base / host / 'skills'
    try:
        files, backups = install(dest, args.overwrite)
    except (OSError, ValueError) as exc:
        p.exit(2, f'Installation stopped / Kurulum durdu: {exc}\n')
    print(f'Installed / Kuruldu: 13 skills + shared tools -> {dest}')
    for _, backup in backups:
        print(f'Backup / Yedek: {backup}')
    print('Codex: $ig-reel | Claude: /ig-reel')
    print('Brand data / Marka verileri: IG_AGENT_HOME or ~/.instagram-agent')


if __name__ == '__main__':
    main()
