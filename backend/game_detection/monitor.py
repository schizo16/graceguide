"""Game detection via process name monitoring using psutil."""

import psutil

GAME_PROCESSES = {
    "eldenring.exe": "eldenring",
    "elden_ring.exe": "eldenring",
    "darksouls3.exe": "darksouls3",
    "darksouls2.exe": "darksouls2",
    "darksouls1.exe": "darksouls1",
    "bloodborne.exe": "bloodborne",
}


def detect_current_game() -> str | None:
    """Return game_id if a supported game process is running, else None."""
    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"]
            if name and name.lower() in GAME_PROCESSES:
                return GAME_PROCESSES[name.lower()]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None
