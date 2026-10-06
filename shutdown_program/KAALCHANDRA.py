import os
import math
import random
import platform
import threading
import ctypes
import tkinter as tk
from ctypes import wintypes
from fractions import Fraction

# Pillow available ho to GIF smooth resize aur red tint ke saath chalegi.
# Optional command:
# pip install pillow

try:
    from PIL import Image, ImageTk, ImageOps, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# =========================================================
# CONFIGURATION
# =========================================================

TOTAL_SECONDS = 15
DO_SHUTDOWN = True

TOP_DOT_CLOCK = True
CENTER_RING = True
SHOW_HACKER_EFFECTS = True

# Program active hone par keyboard/mouse lock rahega.
# Sirf Ctrl + S countdown ko safely close karega.
LOCK_ALL_INPUT = True

# Supported Windows Precision Touchpad par hardware touchpad temporarily OFF.
# Ctrl + S ya program finish hone par previous state restore ho jayegi.
TOGGLE_PRECISION_TOUCHPAD = True

FOCUS_GUARD_INTERVAL_MS = 80

BACKGROUND_GIF = "KAALCHANDRA.gif"

BG = "#020000"

NEON_RED = "#FF1717"
BRIGHT_RED = "#FF3434"
DOT_RED = "#C91616"

DIM_RED = "#290303"
DARK_RED = "#130000"

GLOW_RED_1 = "#8D0808"
GLOW_RED_2 = "#420404"

TEXT_RED = "#FF4A4A"
SOFT_RED = "#8A1919"


# =========================================================
# OS SHUTDOWN
# =========================================================

def shutdown_now():
    if not DO_SHUTDOWN:
        return

    system_name = platform.system().lower()

    if "windows" in system_name:
        os.system('shutdown /s /t 0 /c "Countdown finished"')

    elif "linux" in system_name:
        os.system("systemctl poweroff || poweroff || shutdown -h now")

    elif "darwin" in system_name:
        os.system("osascript -e 'tell application \"System Events\" to shut down'")


# =========================================================
# 5x7 BITMAP FONT
# =========================================================

FONT_5X7 = {
    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110"
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110"
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111"
    ],
    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110"
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010"
    ],
    "5": [
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110"
    ],
    "6": [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110"
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000"
    ],
    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110"
    ],
    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00010",
        "01100"
    ],
    ":": [
        "00000",
        "00100",
        "00100",
        "00000",
        "00100",
        "00100",
        "00000"
    ],
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_hhmmss(seconds: int) -> str:
    seconds = max(0, int(seconds))

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_gif_path() -> str:
    if os.path.isabs(BACKGROUND_GIF):
        return BACKGROUND_GIF

    base_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_directory, BACKGROUND_GIF)


def draw_bitmap_dots(
    canvas,
    x,
    y,
    character,
    dot_radius,
    gap,
    color,
    tag
):
    bitmap = FONT_5X7.get(character)

    if not bitmap:
        return 0

    rows = len(bitmap)
    columns = len(bitmap[0])

    cell_size = (2 * dot_radius) + gap

    # Outer glow
    for row in range(rows):
        for column in range(columns):
            if bitmap[row][column] == "1":
                center_x = x + column * cell_size
                center_y = y + row * cell_size

                canvas.create_oval(
                    center_x - (dot_radius + 3),
                    center_y - (dot_radius + 3),
                    center_x + (dot_radius + 3),
                    center_y + (dot_radius + 3),
                    fill=GLOW_RED_2,
                    outline="",
                    tags=tag
                )

    # Main dots
    for row in range(rows):
        for column in range(columns):
            if bitmap[row][column] == "1":
                center_x = x + column * cell_size
                center_y = y + row * cell_size

                canvas.create_oval(
                    center_x - dot_radius,
                    center_y - dot_radius,
                    center_x + dot_radius,
                    center_y + dot_radius,
                    fill=color,
                    outline="",
                    tags=tag
                )

    width = columns * cell_size
    return width + cell_size


def draw_bitmap_pixels(
    canvas,
    x,
    y,
    character,
    pixel_size,
    gap,
    color,
    tag
):
    bitmap = FONT_5X7.get(character)

    if not bitmap:
        return 0

    rows = len(bitmap)
    columns = len(bitmap[0])

    cell_size = pixel_size + gap

    # Outer glow
    for row in range(rows):
        for column in range(columns):
            if bitmap[row][column] == "1":
                x1 = x + column * cell_size
                y1 = y + row * cell_size

                canvas.create_rectangle(
                    x1 - 4,
                    y1 - 4,
                    x1 + pixel_size + 4,
                    y1 + pixel_size + 4,
                    fill=GLOW_RED_1,
                    outline="",
                    tags=tag
                )

    # Main pixels
    for row in range(rows):
        for column in range(columns):
            if bitmap[row][column] == "1":
                x1 = x + column * cell_size
                y1 = y + row * cell_size

                canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + pixel_size,
                    y1 + pixel_size,
                    fill=color,
                    outline="",
                    tags=tag
                )

    width = columns * cell_size
    return width + pixel_size


# =========================================================
# WINDOWS PRECISION TOUCHPAD CONTROLLER
# =========================================================

class WindowsPrecisionTouchpadController:
    """
    Supported Windows Precision Touchpad ko Ctrl + Win + F24 ke through
    temporarily toggle karta hai. Program band hone par previous state restore
    karne ki koshish karta hai.

    Unsupported/OEM touchpad driver par ye silently fallback karega aur global
    mouse hook phir bhi pointer events block karega.
    """

    REGISTRY_PATH = (
        r"SOFTWARE\Microsoft\Windows\CurrentVersion"
        r"\PrecisionTouchPad\Status"
    )

    VK_CONTROL = 0x11
    VK_LWIN = 0x5B
    VK_F24 = 0x87
    KEYEVENTF_KEYUP = 0x0002

    def __init__(self):
        self.is_windows = platform.system().lower() == "windows"
        self.disabled_by_app = False
        self.original_state = None

    def _read_enabled_state(self):
        if not self.is_windows:
            return None

        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.REGISTRY_PATH,
                0,
                winreg.KEY_READ,
            ) as registry_key:
                value, _ = winreg.QueryValueEx(registry_key, "Enabled")
                return int(value)

        except Exception:
            return None

    def _send_toggle_hotkey(self):
        if not self.is_windows:
            return

        user32 = ctypes.windll.user32

        user32.keybd_event(self.VK_CONTROL, 0, 0, 0)
        user32.keybd_event(self.VK_LWIN, 0, 0, 0)
        user32.keybd_event(self.VK_F24, 0, 0, 0)

        user32.keybd_event(
            self.VK_F24,
            0,
            self.KEYEVENTF_KEYUP,
            0,
        )
        user32.keybd_event(
            self.VK_LWIN,
            0,
            self.KEYEVENTF_KEYUP,
            0,
        )
        user32.keybd_event(
            self.VK_CONTROL,
            0,
            self.KEYEVENTF_KEYUP,
            0,
        )

    def disable(self):
        if not self.is_windows or not TOGGLE_PRECISION_TOUCHPAD:
            return

        self.original_state = self._read_enabled_state()

        # Pehle se disabled touchpad ko toggle nahi karna.
        if self.original_state != 1:
            return

        try:
            self._send_toggle_hotkey()

            # Driver ko state update karne ke liye short poll.
            for _ in range(20):
                threading.Event().wait(0.05)

                if self._read_enabled_state() == 0:
                    self.disabled_by_app = True
                    return

            print(
                "[INFO] Touchpad hardware toggle supported nahi mila; "
                "mouse hook fallback active hai."
            )

        except Exception as error:
            print(f"[WARNING] Touchpad disable nahi hua: {error}")

    def restore(self):
        if not self.is_windows or not self.disabled_by_app:
            return

        try:
            current_state = self._read_enabled_state()

            if current_state == 0:
                self._send_toggle_hotkey()

            self.disabled_by_app = False

        except Exception as error:
            print(f"[WARNING] Touchpad restore nahi hua: {error}")


# =========================================================
# WINDOWS GLOBAL INPUT GUARD
# =========================================================

class WindowsInputGuard:
    """
    Windows par low-level keyboard aur mouse hooks install karta hai.

    - Saare keyboard buttons block hote hain.
    - Saare mouse/touchpad pointer events block hote hain.
    - Sirf Ctrl + S ko internal unlock signal ke roop me accept karta hai.

    Important:
    Ctrl + Alt + Delete Windows ka secure shortcut hai; normal application
    usko block nahi kar sakti aur safety ke liye block karna bhi nahi chahiye.
    """

    WH_KEYBOARD_LL = 13
    WH_MOUSE_LL = 14

    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101
    WM_SYSKEYDOWN = 0x0104
    WM_SYSKEYUP = 0x0105
    WM_QUIT = 0x0012

    VK_CONTROL = 0x11
    VK_LCONTROL = 0xA2
    VK_RCONTROL = 0xA3
    VK_S = 0x53

    HC_ACTION = 0

    class KBDLLHOOKSTRUCT(ctypes.Structure):
        _fields_ = [
            ("vkCode", wintypes.DWORD),
            ("scanCode", wintypes.DWORD),
            ("flags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_void_p),
        ]

    class MSLLHOOKSTRUCT(ctypes.Structure):
        _fields_ = [
            ("pt", wintypes.POINT),
            ("mouseData", wintypes.DWORD),
            ("flags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_void_p),
        ]

    def __init__(self):
        self.is_windows = platform.system().lower() == "windows"
        self.unlock_requested = threading.Event()
        self.ready = threading.Event()
        self.running = False

        self.thread = None
        self.thread_id = 0

        self.keyboard_hook = None
        self.mouse_hook = None

        self.keyboard_callback = None
        self.mouse_callback = None

        self.ctrl_pressed = False

    def start(self):
        if not self.is_windows or self.running:
            return

        self.running = True
        self.ready.clear()

        self.thread = threading.Thread(
            target=self._message_loop,
            name="WindowsInputGuard",
            daemon=True,
        )
        self.thread.start()

        # Hook thread initialize hone ka short wait.
        self.ready.wait(timeout=2.0)

    def _message_loop(self):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        self.thread_id = kernel32.GetCurrentThreadId()

        lresult_type = ctypes.c_ssize_t

        keyboard_proc_type = ctypes.WINFUNCTYPE(
            lresult_type,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )

        mouse_proc_type = ctypes.WINFUNCTYPE(
            lresult_type,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )

        def keyboard_proc(n_code, w_param, l_param):
            if n_code == self.HC_ACTION:
                keyboard_data = ctypes.cast(
                    l_param,
                    ctypes.POINTER(self.KBDLLHOOKSTRUCT),
                ).contents

                virtual_key = int(keyboard_data.vkCode)
                is_key_down = int(w_param) in (
                    self.WM_KEYDOWN,
                    self.WM_SYSKEYDOWN,
                )
                is_key_up = int(w_param) in (
                    self.WM_KEYUP,
                    self.WM_SYSKEYUP,
                )

                if virtual_key in (
                    self.VK_CONTROL,
                    self.VK_LCONTROL,
                    self.VK_RCONTROL,
                ):
                    if is_key_down:
                        self.ctrl_pressed = True
                    elif is_key_up:
                        self.ctrl_pressed = False

                if (
                    is_key_down
                    and virtual_key == self.VK_S
                    and self.ctrl_pressed
                ):
                    self.unlock_requested.set()

                # Keyboard event ko kisi aur application tak nahi jaane dena.
                return 1

            return user32.CallNextHookEx(
                self.keyboard_hook,
                n_code,
                w_param,
                l_param,
            )

        def mouse_proc(n_code, w_param, l_param):
            if n_code == self.HC_ACTION:
                # Click, movement, wheel aur touchpad pointer event block.
                return 1

            return user32.CallNextHookEx(
                self.mouse_hook,
                n_code,
                w_param,
                l_param,
            )

        self.keyboard_callback = keyboard_proc_type(keyboard_proc)
        self.mouse_callback = mouse_proc_type(mouse_proc)

        hook_handle_type = ctypes.c_void_p

        kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        kernel32.GetModuleHandleW.restype = wintypes.HMODULE

        user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.HINSTANCE,
            wintypes.DWORD,
        ]
        user32.SetWindowsHookExW.restype = hook_handle_type

        user32.CallNextHookEx.argtypes = [
            hook_handle_type,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        user32.CallNextHookEx.restype = lresult_type

        user32.UnhookWindowsHookEx.argtypes = [hook_handle_type]
        user32.UnhookWindowsHookEx.restype = wintypes.BOOL

        module_handle = kernel32.GetModuleHandleW(None)

        self.keyboard_hook = user32.SetWindowsHookExW(
            self.WH_KEYBOARD_LL,
            ctypes.cast(self.keyboard_callback, ctypes.c_void_p),
            module_handle,
            0,
        )

        self.mouse_hook = user32.SetWindowsHookExW(
            self.WH_MOUSE_LL,
            ctypes.cast(self.mouse_callback, ctypes.c_void_p),
            module_handle,
            0,
        )

        if not self.keyboard_hook:
            print("[WARNING] Global keyboard lock start nahi hua.")

        if not self.mouse_hook:
            print("[WARNING] Global mouse lock start nahi hua.")

        self.ready.set()

        message = wintypes.MSG()

        while self.running:
            result = user32.GetMessageW(
                ctypes.byref(message),
                None,
                0,
                0,
            )

            if result <= 0:
                break

            user32.TranslateMessage(ctypes.byref(message))
            user32.DispatchMessageW(ctypes.byref(message))

        self._remove_hooks()

    def _remove_hooks(self):
        if not self.is_windows:
            return

        try:
            user32 = ctypes.windll.user32

            if self.keyboard_hook:
                user32.UnhookWindowsHookEx(self.keyboard_hook)
                self.keyboard_hook = None

            if self.mouse_hook:
                user32.UnhookWindowsHookEx(self.mouse_hook)
                self.mouse_hook = None

        except Exception as error:
            print(f"[WARNING] Input hooks remove nahi hue: {error}")

    def stop(self):
        if not self.is_windows:
            return

        self.running = False

        try:
            if self.thread_id:
                ctypes.windll.user32.PostThreadMessageW(
                    self.thread_id,
                    self.WM_QUIT,
                    0,
                    0,
                )
        except Exception:
            pass

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

        self._remove_hooks()

    def consume_unlock_request(self) -> bool:
        if not self.unlock_requested.is_set():
            return False

        self.unlock_requested.clear()
        return True


# =========================================================
# MAIN APPLICATION
# =========================================================

class HackerCountdown:

    def __init__(self, total_seconds: int):
        self.total = max(1, int(total_seconds))
        self.left = self.total
        self.cancelled = False

        self.root = tk.Tk()
        self.root.configure(bg=BG)
        self.root.title("System Shutdown Protocol")

        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        # Window manager ke close request ko ignore karo.
        self.root.protocol("WM_DELETE_WINDOW", self.block_event)

        self.input_guard = WindowsInputGuard()
        self.touchpad_controller = WindowsPrecisionTouchpadController()
        self.focus_guard_after_id = None
        self.unlock_poll_after_id = None

        # Tkinter level par bhi sab input block rahega.
        self.install_tk_input_bindings()

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.minimum_dimension = min(self.width, self.height)

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=BG,
            highlightthickness=0,
            cursor="none"
        )

        self.canvas.pack(fill="both", expand=True)

        self.center_x = self.width // 2
        self.center_y = self.height // 2

        self.segment_count = 160
        self.ring_ids = []

        self.ring_outer_radius = int(self.minimum_dimension * 0.27)
        self.ring_inner_radius = int(self.minimum_dimension * 0.225)

        # GIF variables
        self.gif_path = get_gif_path()
        self.gif_source = None
        self.gif_frame_index = 0
        self.gif_frame_count = 0
        self.gif_photo = None
        self.gif_item = None

        # Native Tk GIF fallback
        self.tk_gif_frame_index = 0
        self.tk_gif_zoom = 1
        self.tk_gif_subsample = 1

        self.start_background_gif()
        self.create_dark_overlay()
        self.create_static_hacker_design()

        if CENTER_RING:
            self.build_ring()

        self.render()
        self.animate_hacker_effects()

        # Window visible hone ke baad global input lock start karo.
        self.root.after(100, self.enable_input_lock)
        self.root.after(1000, self.tick)


    # =====================================================
    # INPUT LOCK
    # =====================================================

    def block_event(self, event=None):
        return "break"


    def handle_ctrl_s(self, event=None):
        self.stop()
        return "break"


    def handle_any_key(self, event):
        # Non-Windows fallback ke liye Ctrl + S allow karo.
        ctrl_pressed = bool(event.state & 0x0004)

        if ctrl_pressed and str(event.keysym).lower() == "s":
            return self.handle_ctrl_s(event)

        return "break"


    def install_tk_input_bindings(self):
        # Keyboard: sirf Ctrl + S allowed.
        self.root.bind_all("<KeyPress>", self.handle_any_key)
        self.root.bind_all("<KeyRelease>", self.block_event)
        self.root.bind_all("<Control-s>", self.handle_ctrl_s)
        self.root.bind_all("<Control-S>", self.handle_ctrl_s)

        # Mouse/touchpad events ko application ke andar block karo.
        blocked_events = (
            "<ButtonPress>",
            "<ButtonRelease>",
            "<Motion>",
            "<B1-Motion>",
            "<B2-Motion>",
            "<B3-Motion>",
            "<MouseWheel>",
            "<Shift-MouseWheel>",
            "<Control-MouseWheel>",
            "<Enter>",
            "<Leave>",
            "<Escape>",
            "<Alt-F4>",
        )

        for event_name in blocked_events:
            self.root.bind_all(event_name, self.block_event)

        # Minimize/unmap hone ki koshish par window ko turant restore karo.
        self.root.bind("<Unmap>", self.restore_locked_window)


    def enable_input_lock(self):
        if self.cancelled:
            return

        if LOCK_ALL_INPUT:
            # Hook se pehle supported Precision Touchpad ko hardware level par OFF.
            self.touchpad_controller.disable()
            self.input_guard.start()

        self.keep_window_locked()
        self.poll_unlock_request()


    def poll_unlock_request(self):
        if self.cancelled:
            return

        if self.input_guard.consume_unlock_request():
            self.stop()
            return

        self.unlock_poll_after_id = self.root.after(
            25,
            self.poll_unlock_request,
        )


    def keep_window_locked(self):
        if self.cancelled:
            return

        try:
            if self.root.state() == "iconic":
                self.root.deiconify()

            self.root.attributes("-fullscreen", True)
            self.root.attributes("-topmost", True)
            self.root.lift()
            self.root.focus_force()

            try:
                self.root.grab_set_global()
            except tk.TclError:
                self.root.grab_set()

        except tk.TclError:
            return

        self.focus_guard_after_id = self.root.after(
            FOCUS_GUARD_INTERVAL_MS,
            self.keep_window_locked,
        )


    def restore_locked_window(self, event=None):
        if self.cancelled:
            return "break"

        self.root.after(0, self.keep_window_locked)
        return "break"


    def release_input_lock(self):
        # Pehle hooks hatao, phir touchpad ki previous state restore karo.
        self.input_guard.stop()
        self.touchpad_controller.restore()

        try:
            if self.focus_guard_after_id:
                self.root.after_cancel(self.focus_guard_after_id)
        except Exception:
            pass

        try:
            if self.unlock_poll_after_id:
                self.root.after_cancel(self.unlock_poll_after_id)
        except Exception:
            pass

        try:
            self.root.grab_release()
        except Exception:
            pass


    # =====================================================
    # BACKGROUND GIF
    # =====================================================

    def start_background_gif(self):
        if not os.path.isfile(self.gif_path):
            print(f"[WARNING] Background GIF not found: {self.gif_path}")
            return

        if PIL_AVAILABLE:
            try:
                self.gif_source = Image.open(self.gif_path)
                self.gif_frame_count = getattr(
                    self.gif_source,
                    "n_frames",
                    1
                )

                self.animate_background_with_pillow()
                return

            except Exception as error:
                print(f"[WARNING] Pillow GIF error: {error}")

        self.animate_background_with_tkinter()


    def resize_image_to_cover(self, image):
        image_width, image_height = image.size

        if image_width <= 0 or image_height <= 0:
            return image

        scale = max(
            self.width / image_width,
            self.height / image_height
        )

        new_width = max(1, int(image_width * scale))
        new_height = max(1, int(image_height * scale))

        try:
            resampling = Image.Resampling.LANCZOS
        except AttributeError:
            resampling = Image.LANCZOS

        image = image.resize(
            (new_width, new_height),
            resampling
        )

        left = max(0, (new_width - self.width) // 2)
        top = max(0, (new_height - self.height) // 2)

        right = left + self.width
        bottom = top + self.height

        return image.crop((left, top, right, bottom))


    def create_red_hacker_frame(self, frame):
        frame = frame.convert("RGB")

        grayscale = ImageOps.grayscale(frame)

        red_frame = ImageOps.colorize(
            grayscale,
            black="#000000",
            white="#690000"
        )

        red_frame = ImageEnhance.Contrast(
            red_frame
        ).enhance(1.35)

        red_frame = ImageEnhance.Brightness(
            red_frame
        ).enhance(0.55)

        red_frame = self.resize_image_to_cover(red_frame)

        return red_frame


    def animate_background_with_pillow(self):
        if self.cancelled or not self.gif_source:
            return

        try:
            self.gif_source.seek(self.gif_frame_index)

            duration = self.gif_source.info.get("duration", 80)
            duration = max(40, int(duration))

            current_frame = self.gif_source.copy()
            current_frame = self.create_red_hacker_frame(current_frame)

            self.gif_photo = ImageTk.PhotoImage(current_frame)

            if self.gif_item is None:
                self.gif_item = self.canvas.create_image(
                    0,
                    0,
                    anchor="nw",
                    image=self.gif_photo,
                    tags="background"
                )
            else:
                self.canvas.itemconfig(
                    self.gif_item,
                    image=self.gif_photo
                )

            self.canvas.tag_lower("background")

            self.gif_frame_index += 1

            if self.gif_frame_index >= self.gif_frame_count:
                self.gif_frame_index = 0

            self.root.after(
                duration,
                self.animate_background_with_pillow
            )

        except Exception as error:
            print(f"[WARNING] GIF frame error: {error}")

            self.gif_frame_index = 0
            self.root.after(
                100,
                self.animate_background_with_pillow
            )


    def animate_background_with_tkinter(self):
        if self.cancelled:
            return

        try:
            frame = tk.PhotoImage(
                file=self.gif_path,
                format=f"gif -index {self.tk_gif_frame_index}"
            )

            if self.tk_gif_frame_index == 0:
                gif_width = max(1, frame.width())
                gif_height = max(1, frame.height())

                scale = max(
                    self.width / gif_width,
                    self.height / gif_height
                )

                fraction = Fraction(scale).limit_denominator(8)

                self.tk_gif_zoom = max(1, fraction.numerator)
                self.tk_gif_subsample = max(1, fraction.denominator)

            frame = frame.zoom(
                self.tk_gif_zoom,
                self.tk_gif_zoom
            )

            frame = frame.subsample(
                self.tk_gif_subsample,
                self.tk_gif_subsample
            )

            self.gif_photo = frame

            if self.gif_item is None:
                self.gif_item = self.canvas.create_image(
                    self.center_x,
                    self.center_y,
                    anchor="center",
                    image=self.gif_photo,
                    tags="background"
                )
            else:
                self.canvas.itemconfig(
                    self.gif_item,
                    image=self.gif_photo
                )

            self.canvas.tag_lower("background")

            self.tk_gif_frame_index += 1

            self.root.after(
                80,
                self.animate_background_with_tkinter
            )

        except tk.TclError:
            if self.tk_gif_frame_index == 0:
                print(f"[WARNING] Could not load GIF: {self.gif_path}")
                return

            self.tk_gif_frame_index = 0

            self.root.after(
                80,
                self.animate_background_with_tkinter
            )


    # =====================================================
    # DARK RED OVERLAY
    # =====================================================

    def create_dark_overlay(self):
        self.canvas.create_rectangle(
            0,
            0,
            self.width,
            self.height,
            fill="#080000",
            stipple="gray50",
            outline="",
            tags="overlay"
        )

        # Scan lines
        for y_position in range(0, self.height, 8):
            self.canvas.create_line(
                0,
                y_position,
                self.width,
                y_position,
                fill="#180000",
                width=1,
                tags="overlay"
            )

        # Screen border glow
        self.canvas.create_rectangle(
            10,
            10,
            self.width - 10,
            self.height - 10,
            outline="#5B0808",
            width=2,
            tags="overlay"
        )

        self.canvas.create_rectangle(
            18,
            18,
            self.width - 18,
            self.height - 18,
            outline="#250303",
            width=1,
            tags="overlay"
        )


    # =====================================================
    # STATIC HACKER DESIGN
    # =====================================================

    def create_static_hacker_design(self):
        title_font_size = max(
            14,
            int(self.minimum_dimension * 0.022)
        )

        small_font_size = max(
            9,
            int(self.minimum_dimension * 0.012)
        )

        self.canvas.create_text(
            self.width // 2,
            int(self.height * 0.035),
            text="[ 𝚂𝚈𝚂𝚃𝙴𝙼 𝚃𝙴𝚁𝙼𝙸𝙽𝙰𝚃𝙸𝙾𝙽 𝙿𝚁𝙾𝚃𝙾𝙲𝙾𝙻 ]",
            fill=TEXT_RED,
            font=("Consolas", title_font_size, "bold"),
            tags="static"
        )

        self.canvas.create_text(
            35,
            35,
            anchor="nw",
            text="ROOT ACCESS: GRANTED\nNODE: LOCALHOST\nPROTOCOL: ACTIVE",
            fill=SOFT_RED,
            font=("Consolas", small_font_size, "bold"),
            justify="left",
            tags="static"
        )

        self.canvas.create_text(
            self.width - 35,
            35,
            anchor="ne",
            text="SECURITY LEVEL: CRITICAL\nENCRYPTION: ENABLED\nSTATUS: COUNTDOWN",
            fill=SOFT_RED,
            font=("Consolas", small_font_size, "bold"),
            justify="right",
            tags="static"
        )

        bottom_y = self.height - 35

        self.canvas.create_text(
            35,
            bottom_y,
            anchor="sw",
            text="",
            fill="#9C2020",
            font=("Consolas", small_font_size, "bold"),
            tags="static"
        )

        self.canvas.create_text(
            self.width - 35,
            bottom_y,
            anchor="se",
            text="",
            fill="#9C2020",
            font=("Consolas", small_font_size, "bold"),
            tags="static"
        )

        line_y = int(self.height * 0.078)

        self.canvas.create_line(
            int(self.width * 0.05),
            line_y,
            int(self.width * 0.35),
            line_y,
            fill="#720A0A",
            width=2,
            tags="static"
        )

        self.canvas.create_line(
            int(self.width * 0.65),
            line_y,
            int(self.width * 0.95),
            line_y,
            fill="#720A0A",
            width=2,
            tags="static"
        )


    # =====================================================
    # CENTER RING
    # =====================================================

    def build_ring(self):
        self.ring_ids.clear()

        glow_width = max(
            5,
            int(self.minimum_dimension * 0.010)
        )

        main_width = max(
            3,
            int(self.minimum_dimension * 0.006)
        )

        for index in range(self.segment_count):
            angle = (
                (2 * math.pi) *
                (index / self.segment_count)
            ) - (math.pi / 2)

            x1 = (
                self.center_x +
                self.ring_inner_radius * math.cos(angle)
            )

            y1 = (
                self.center_y +
                self.ring_inner_radius * math.sin(angle)
            )

            x2 = (
                self.center_x +
                self.ring_outer_radius * math.cos(angle)
            )

            y2 = (
                self.center_y +
                self.ring_outer_radius * math.sin(angle)
            )

            glow_id = self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=GLOW_RED_2,
                width=glow_width,
                capstyle="round",
                tags="ring"
            )

            main_id = self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=DIM_RED,
                width=main_width,
                capstyle="round",
                tags="ring"
            )

            self.ring_ids.append(
                (glow_id, main_id)
            )


    # =====================================================
    # COUNTDOWN
    # =====================================================

    def stop(self):
        if self.cancelled:
            return

        self.cancelled = True
        self.release_input_lock()

        try:
            self.root.destroy()
        except Exception:
            pass


    def finish_countdown(self):
        if self.cancelled:
            return

        self.cancelled = True
        self.release_input_lock()

        try:
            self.root.destroy()
        except Exception:
            pass

        shutdown_now()


    def tick(self):
        if self.cancelled:
            return

        self.left -= 1

        if self.left <= 0:
            self.left = 0
            self.render()

            self.root.after(
                150,
                self.finish_countdown
            )

            return

        self.render()

        self.root.after(
            1000,
            self.tick
        )


    # =====================================================
    # DYNAMIC HACKER EFFECTS
    # =====================================================

    def random_hex_string(self, length=28):
        characters = "0123456789ABCDEF"
        return "".join(
            random.choice(characters)
            for _ in range(length)
        )


    def animate_hacker_effects(self):
        if self.cancelled:
            return

        self.canvas.delete("effects")

        if SHOW_HACKER_EFFECTS:
            small_font_size = max(
                8,
                int(self.minimum_dimension * 0.010)
            )

            # Left-side hacker data
            for index in range(7):
                y_position = int(
                    self.height * 0.22 +
                    index * self.height * 0.065
                )

                data_text = (
                    f"0x{self.random_hex_string(10)} "
                    f"::{self.random_hex_string(8)}"
                )

                self.canvas.create_text(
                    30,
                    y_position,
                    anchor="w",
                    text=data_text,
                    fill="#5A1111",
                    font=("Consolas", small_font_size),
                    tags="effects"
                )

            # Right-side hacker data
            for index in range(7):
                y_position = int(
                    self.height * 0.22 +
                    index * self.height * 0.065
                )

                data_text = (
                    f"{self.random_hex_string(8)}"
                    f"//{random.randint(1000, 9999)}"
                )

                self.canvas.create_text(
                    self.width - 30,
                    y_position,
                    anchor="e",
                    text=data_text,
                    fill="#5A1111",
                    font=("Consolas", small_font_size),
                    tags="effects"
                )

            # Moving scan line
            scan_y = random.randint(
                int(self.height * 0.12),
                int(self.height * 0.90)
            )

            self.canvas.create_rectangle(
                0,
                scan_y,
                self.width,
                scan_y + random.randint(1, 3),
                fill="#580707",
                outline="",
                tags="effects"
            )

            # Random glitch blocks
            for _ in range(random.randint(3, 7)):
                block_width = random.randint(25, 180)
                block_height = random.randint(1, 4)

                x_position = random.randint(
                    0,
                    max(0, self.width - block_width)
                )

                y_position = random.randint(
                    0,
                    max(0, self.height - block_height)
                )

                self.canvas.create_rectangle(
                    x_position,
                    y_position,
                    x_position + block_width,
                    y_position + block_height,
                    fill=random.choice([
                        "#5A0505",
                        "#800A0A",
                        "#A30E0E"
                    ]),
                    outline="",
                    tags="effects"
                )

        self.root.after(
            140,
            self.animate_hacker_effects
        )


    # =====================================================
    # RENDER COUNTDOWN
    # =====================================================

    def render(self):
        self.canvas.delete("top_clock")
        self.canvas.delete("center_digits")
        self.canvas.delete("dynamic_text")

        self.render_top_clock()
        self.render_center_ring()
        self.render_center_text()


    def render_top_clock(self):
        if not TOP_DOT_CLOCK:
            return

        time_text = format_hhmmss(self.left)

        dot_radius = max(
            2,
            int(self.minimum_dimension * 0.007)
        )

        gap = max(
            1,
            int(dot_radius * 0.55)
        )

        cell_size = (2 * dot_radius) + gap

        character_width = (
            5 * cell_size
        ) + cell_size

        total_width = (
            len(time_text) *
            character_width
        )

        start_x = (
            self.width -
            total_width
        ) // 2

        start_y = int(self.height * 0.105)

        current_x = start_x

        for character in time_text:
            current_x += draw_bitmap_dots(
                self.canvas,
                current_x,
                start_y,
                character,
                dot_radius,
                gap,
                DOT_RED,
                "top_clock"
            )


    def render_center_ring(self):
        if not CENTER_RING or not self.ring_ids:
            return

        fraction_left = self.left / self.total

        active_segments = int(
            math.ceil(
                fraction_left *
                self.segment_count
            )
        )

        for index, ring_pair in enumerate(self.ring_ids):
            glow_id, main_id = ring_pair

            if index < active_segments:
                self.canvas.itemconfig(
                    glow_id,
                    fill=GLOW_RED_1
                )

                self.canvas.itemconfig(
                    main_id,
                    fill=NEON_RED
                )

            else:
                self.canvas.itemconfig(
                    glow_id,
                    fill=GLOW_RED_2
                )

                self.canvas.itemconfig(
                    main_id,
                    fill=DIM_RED
                )

        number_text = str(self.left)

        pixel_size = max(
            6,
            int(self.minimum_dimension * 0.030)
        )

        gap = max(
            2,
            int(pixel_size * 0.25)
        )

        single_digit_width = (
            5 * (pixel_size + gap)
        ) + pixel_size

        total_number_width = (
            len(number_text) *
            single_digit_width
        )

        start_x = (
            self.center_x -
            total_number_width // 2
        )

        start_y = (
            self.center_y -
            int(self.minimum_dimension * 0.10)
        )

        current_x = start_x

        for character in number_text:
            current_x += draw_bitmap_pixels(
                self.canvas,
                current_x,
                start_y,
                character,
                pixel_size,
                gap,
                BRIGHT_RED,
                "center_digits"
            )


    def render_center_text(self):
        label_font_size = max(
            11,
            int(self.minimum_dimension * 0.015)
        )

        status_font_size = max(
            9,
            int(self.minimum_dimension * 0.011)
        )

        self.canvas.create_text(
            self.center_x,
            self.center_y - int(self.minimum_dimension * 0.165),
            text="𝚂𝚈𝚂𝚃𝙴𝙼 𝚃𝙴𝚁𝙼𝙸𝙽𝙰𝚃𝙸𝙾𝙽 𝙿𝚁𝙾𝚃𝙾𝙲𝙾𝙻 ",
            fill="#A91D1D",
            font=("Consolas", label_font_size, "bold"),
            tags="dynamic_text"
        )

        percentage = int(
            (self.left / self.total) * 100
        )

        self.canvas.create_text(
            self.center_x,
            self.center_y + int(self.minimum_dimension * 0.16),
            text=(
                f"CORE STATUS: CRITICAL  //  "
                f"REMAINING: {percentage:03d}%"
            ),
            fill="#8D1818",
            font=("Consolas", status_font_size, "bold"),
            tags="dynamic_text"
        )

        warning_text = (
            "DO NOT INTERRUPT SYSTEM PROCESS"
            if self.left > 3
            else "FINAL SHUTDOWN SEQUENCE"
        )

        warning_color = (
            "#8D1818"
            if self.left > 3
            else "#FF3333"
        )

        self.canvas.create_text(
            self.center_x,
            self.center_y + int(self.minimum_dimension * 0.205),
            text=warning_text,
            fill=warning_color,
            font=("Consolas", status_font_size, "bold"),
            tags="dynamic_text"
        )


    # =====================================================
    # START APPLICATION
    # =====================================================

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.input_guard.stop()
            self.touchpad_controller.restore()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    HackerCountdown(TOTAL_SECONDS).run()