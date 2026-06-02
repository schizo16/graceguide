"""XInput controller detection via ctypes (Windows only).

On non-Windows platforms, always returns disconnected.
"""

import sys
import ctypes
from ctypes import wintypes

# XInput constants
ERROR_SUCCESS = 0
ERROR_DEVICE_NOT_CONNECTED = 1167
XINPUT_GAMEPAD_LEFT_SHOULDER = 0x0400
XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0800
XINPUT_GAMEPAD_START = 0x0010
XINPUT_GAMEPAD_DPAD_UP = 0x0001
XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
XINPUT_GAMEPAD_DPAD_LEFT = 0x0004
XINPUT_GAMEPAD_DPAD_RIGHT = 0x0008
XINPUT_GAMEPAD_A = 0x1000
XINPUT_GAMEPAD_B = 0x2000


class XInputState(ctypes.Structure):
    _fields_ = [
        ("packet_number", wintypes.DWORD),
        ("buttons", wintypes.WORD),
        ("left_trigger", wintypes.BYTE),
        ("right_trigger", wintypes.BYTE),
        ("thumb_lx", wintypes.SHORT),
        ("thumb_ly", wintypes.SHORT),
        ("thumb_rx", wintypes.SHORT),
        ("thumb_ry", wintypes.SHORT),
    ]


def _load_xinput():
    """Load XInput1_4.dll (Windows 8+) or return None."""
    if sys.platform != "win32":
        return None
    for dll in ["XInput1_4.dll", "XInput9_1_0.dll"]:
        try:
            lib = ctypes.windll.LoadLibrary(dll)
            func = lib.XInputGetState
            func.argtypes = [wintypes.DWORD, ctypes.POINTER(XInputState)]
            func.restype = wintypes.DWORD
            return func
        except OSError:
            continue
    return None


_xinput_get_state = _load_xinput()


def is_controller_connected(index: int = 0) -> bool:
    """Check if a controller is connected at given port index."""
    if _xinput_get_state is None:
        return False
    state = XInputState()
    result = _xinput_get_state(index, ctypes.byref(state))
    return result == ERROR_SUCCESS


def get_controller_state(index: int = 0) -> dict | None:
    """Return current button state if controller connected, else None."""
    if _xinput_get_state is None:
        return None
    state = XInputState()
    result = _xinput_get_state(index, ctypes.byref(state))
    if result != ERROR_SUCCESS:
        return None
    buttons = state.buttons
    return {
        "connected": True,
        "buttons": buttons,
        "lb_held": bool(buttons & XINPUT_GAMEPAD_LEFT_SHOULDER),
        "rb_held": bool(buttons & XINPUT_GAMEPAD_RIGHT_SHOULDER),
        "start_held": bool(buttons & XINPUT_GAMEPAD_START),
        "a_pressed": bool(buttons & XINPUT_GAMEPAD_A),
        "b_pressed": bool(buttons & XINPUT_GAMEPAD_B),
        "dpad_up": bool(buttons & XINPUT_GAMEPAD_DPAD_UP),
        "dpad_down": bool(buttons & XINPUT_GAMEPAD_DPAD_DOWN),
        "dpad_left": bool(buttons & XINPUT_GAMEPAD_DPAD_LEFT),
        "dpad_right": bool(buttons & XINPUT_GAMEPAD_DPAD_RIGHT),
        "chord_active": (
            bool(buttons & XINPUT_GAMEPAD_LEFT_SHOULDER)
            and bool(buttons & XINPUT_GAMEPAD_RIGHT_SHOULDER)
            and bool(buttons & XINPUT_GAMEPAD_START)
        ),
    }
