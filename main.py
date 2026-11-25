"""Coinage builder for Invent a Word We Need."""
import json
import os
import time
from pathlib import Path

MAX_CHARS = 140


class Coinage:
    def __init__(self, home):
        self.home = home
        self.raw = (home / "entry.txt").read_bytes()
        self.text = self.raw.decode("utf-8")

    def sweep(self):
        body = self.text.strip()
        if not (0 < len(body) <= MAX_CHARS):
            raise ValueError(f"coinage length out of gate range: {len(body)}")
        if "\n" in body:
            raise ValueError("coinage must stay on one line")
        return body

    def emit(self, out_dir, body):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "entry.txt").write_bytes(body.encode("utf-8"))
        return {"word_len": len(body.split()[0]), "chars": len(body)}


def main():
    home = Path(__file__).resolve().parent
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    coin = Coinage(home)
    body = coin.sweep()
    stats = coin.emit(target, body)
    receipt = {"status": "COINAGE_OK", "gate_max": MAX_CHARS,
               "stamp": time.strftime("%Y%m%dT%H%M%SZ"), **stats}
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
