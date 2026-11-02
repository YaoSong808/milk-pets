#!/usr/bin/env python3
"""Install Milk Pets into the local Codex custom-pet folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import tempfile


REPO = Path(__file__).resolve().parents[1]
PETS = {
    "naiwa": "0e2d141da1f7694bdf62eb8cb525886bd656bd0afe65292bbe10baee80f8af3d",
    "naiji": "663ff342a886056e5adf646fd5829f57e662b6cc9197658bf8e813d94e00390d",
    "naishu": "ca942241c817e6a27bb4b5b49b8251fe7844ec6251874548e366d4b66f5a96c3",
}


def install(name: str, destination: Path) -> dict:
    source = REPO / "pets" / name
    manifest = json.loads((source / "pet.json").read_text(encoding="utf-8"))
    sheet = source / manifest["spritesheetPath"]
    data = sheet.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", data[16:24]) != (1536, 2288):
        raise ValueError(f"{name}: expected a 1536x2288 PNG")
    if manifest.get("spriteVersionNumber") != 2:
        raise ValueError(f"{name}: expected spriteVersionNumber 2")
    digest = hashlib.sha256(data).hexdigest()
    if digest != PETS[name]:
        raise ValueError(f"{name}: sprite checksum does not match the approved file")
    pet_id = manifest["id"]
    if Path(pet_id).name != pet_id:
        raise ValueError("invalid pet id")
    target = destination / pet_id
    if target.exists():
        expected_manifest = target / "pet.json"
        expected_sheet = target / manifest["spritesheetPath"]
        if (expected_manifest.is_file() and expected_sheet.is_file()
                and json.loads(expected_manifest.read_text(encoding="utf-8")) == manifest
                and hashlib.sha256(expected_sheet.read_bytes()).hexdigest() == digest):
            return {"name": manifest["displayName"], "status": "already-installed", "path": str(target), "sha256": digest}
        raise FileExistsError(f"{target} already contains another version; no files were overwritten")
    destination.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".milk-{name}-", dir=destination))
    try:
        shutil.copy2(source / "pet.json", stage / "pet.json")
        shutil.copy2(sheet, stage / manifest["spritesheetPath"])
        stage.rename(target)
    except Exception:
        shutil.rmtree(stage)
        raise
    return {"name": manifest["displayName"], "status": "installed", "path": str(target), "sha256": digest}


def main() -> None:
    parser = argparse.ArgumentParser(description="Install local Codex desktop pets. Existing different versions are never overwritten.")
    parser.add_argument("--pet", choices=list(PETS), help="Install one pet; omit to install all three")
    parser.add_argument("--destination", type=Path, help="Override the Codex pets directory, useful for validation")
    parser.add_argument("--json", action="store_true", help="Print an installation report as JSON")
    args = parser.parse_args()
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    destination = (args.destination or codex_root / "pets").expanduser().resolve()
    report = [install(name, destination) for name in ([args.pet] if args.pet else PETS)]
    if args.json:
        print(json.dumps({"application": "Codex", "pets": report}, ensure_ascii=False, indent=2))
    else:
        for row in report:
            status = "已安装" if row["status"] == "already-installed" else "安装完成"
            print(f"{row['name']}：{status}")
        print("打开 Codex 的桌宠选择器即可选择；如果列表未刷新，请重新打开桌宠选择器或重启 Codex。")
        print("ChatGPT Work 用户请按 USAGE.md 中的上传方式导入。")


if __name__ == "__main__":
    main()
