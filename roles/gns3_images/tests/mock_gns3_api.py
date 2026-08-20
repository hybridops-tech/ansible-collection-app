#!/usr/bin/env python3
"""Small local GNS3 API fixture for the image-role acceptance test."""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


IMAGE_BYTES = b"HYBRIDOPS_IOU_TEST\n"


class Handler(BaseHTTPRequestHandler):
    templates: list[dict[str, Any]] = []

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def _json(self, status: int, value: object) -> None:
        payload = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/v2/templates":
            self._json(200, self.templates)
            return
        if self.path in {"/router.bin", "/test.qcow2"}:
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(IMAGE_BYTES)))
            self.end_headers()
            self.wfile.write(IMAGE_BYTES)
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/shutdown":
            self._json(200, {"status": "stopping"})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        if self.path != "/v2/templates":
            self._json(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length))
        required = {"name", "template_type", "compute_id"}
        valid_type = body.get("template_type") in {"iou", "qemu"}
        valid_image = (
            body.get("template_type") == "iou" and "path" in body
        ) or (
            body.get("template_type") == "qemu"
            and ("hda_disk_image" in body or "cdrom_image" in body)
        )
        if not required.issubset(body) or not valid_type or not valid_image:
            self._json(400, {"error": "invalid template"})
            return
        body["template_id"] = "00000000-0000-4000-8000-000000000001"
        self.templates.append(body)
        self._json(201, body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
