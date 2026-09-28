"""Local-mode enforcement.

Call enforce_local() before importing mlx_lm / transformers / sentence_transformers.
It (1) sets the Hugging Face offline flags so libraries read only the local cache,
and (2) replaces socket connect/DNS with versions that refuse any non-loopback
address. If some library tried to reach the internet, the call fails loudly
instead of silently falling back to a cloud service.
"""

import os
import socket

BLOCKED: list[str] = []   # every refused attempt, reported by `wiki stats` and the tests

_LOOPBACK_NAMES = {"localhost", "127.0.0.1", "::1", ""}


class NetworkBlocked(OSError):
    pass


def _is_loopback(host) -> bool:
    if host is None:
        return True
    host = host.decode() if isinstance(host, bytes) else str(host)
    return host in _LOOPBACK_NAMES or host.startswith("127.")


def enforce_local() -> None:
    for var in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_DATASETS_OFFLINE"):
        os.environ[var] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    if getattr(socket, "_wiki_guarded", False):
        return

    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    real_getaddrinfo = socket.getaddrinfo

    def guarded_connect(self, address):
        if self.family in (socket.AF_INET, socket.AF_INET6) and not _is_loopback(address[0]):
            BLOCKED.append(f"connect {address[0]}:{address[1]}")
            raise NetworkBlocked(f"local mode: refused network connection to {address[0]}")
        return real_connect(self, address)

    def guarded_connect_ex(self, address):
        if self.family in (socket.AF_INET, socket.AF_INET6) and not _is_loopback(address[0]):
            BLOCKED.append(f"connect {address[0]}:{address[1]}")
            raise NetworkBlocked(f"local mode: refused network connection to {address[0]}")
        return real_connect_ex(self, address)

    def guarded_getaddrinfo(host, *args, **kwargs):
        if not _is_loopback(host):
            BLOCKED.append(f"dns {host}")
            raise NetworkBlocked(f"local mode: refused DNS lookup for {host}")
        return real_getaddrinfo(host, *args, **kwargs)

    socket.socket.connect = guarded_connect
    socket.socket.connect_ex = guarded_connect_ex
    socket.getaddrinfo = guarded_getaddrinfo
    socket._wiki_guarded = True
