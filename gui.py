import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import io
import contextlib
import os
import shutil
import subprocess


import chatbot


# ============================================================
# AI LAPTOP MANAGER - RESPONSIVE GUI
# ============================================================

class AILaptopManagerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("AI Laptop Manager")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg="#111827")

        self.busy = False
        self.result_windows = []

        self.build_ui()

        self.add_bot_message(
            "👋 Hello! I'm your AI Laptop Manager.\n\n"
            "You can search for any file and open it directly.\n\n"
            "Examples:\n"
            "• find resume\n"
            "• find movie\n"
            "• find certificate\n"
            "• open resume\n"
            "• open movie\n"
        )

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # HEADER
        header = tk.Frame(
            self.root,
            bg="#172033",
            height=75
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🤖",
            font=("Segoe UI Emoji", 28),
            bg="#172033",
            fg="white"
        ).pack(
            side="left",
            padx=(20, 10)
        )

        title_frame = tk.Frame(
            header,
            bg="#172033"
        )
        title_frame.pack(
            side="left",
            pady=10
        )

        tk.Label(
            title_frame,
            text="AI Laptop Manager",
            font=("Segoe UI", 20, "bold"),
            bg="#172033",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Your local Windows laptop assistant",
            font=("Segoe UI", 9),
            bg="#172033",
            fg="#9ca3af"
        ).pack(anchor="w")

        self.status_label = tk.Label(
            header,
            text="● Ready",
            font=("Segoe UI", 10, "bold"),
            bg="#172033",
            fg="#22c55e"
        )

        self.status_label.pack(
            side="right",
            padx=25
        )

        # MAIN
        main = tk.Frame(
            self.root,
            bg="#111827"
        )
        main.pack(
            fill="both",
            expand=True
        )

        # SIDEBAR
        sidebar = tk.Frame(
            main,
            bg="#151e2e",
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="QUICK ACTIONS",
            font=("Segoe UI", 9, "bold"),
            bg="#151e2e",
            fg="#6b7280"
        ).pack(
            anchor="w",
            padx=18,
            pady=(20, 12)
        )

        buttons = [
            ("💾  Storage", "analyze storage"),
            ("📥  Downloads", "analyze downloads"),
            ("🎬  Movies", "show my movies"),
            ("📄  Find Resume", "find resume"),
            ("♻️  Duplicates", "find duplicates"),
            ("🛡️  Security", "check suspicious files"),
            ("📅  Old Files", "show old files"),
            ("🧹  Cleanup", "clean my laptop"),
            ("📁  Organize", "organize downloads"),
        ]

        for text, command in buttons:
            self.create_button(
                sidebar,
                text,
                command
            )

        # CONTENT
        content = tk.Frame(
            main,
            bg="#111827"
        )

        content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # CHAT
        self.chat = scrolledtext.ScrolledText(
            content,
            wrap=tk.WORD,
            bg="#0f172a",
            fg="#e5e7eb",
            insertbackground="white",
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=18
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(12, 8)
        )

        self.chat.tag_config(
            "user",
            foreground="#60a5fa",
            font=("Segoe UI", 10, "bold")
        )

        self.chat.tag_config(
            "bot",
            foreground="#34d399",
            font=("Segoe UI", 10, "bold")
        )

        self.chat.tag_config(
            "system",
            foreground="#fbbf24",
            font=("Segoe UI", 9)
        )

        self.chat.configure(
            state="disabled"
        )

        # INPUT
        input_area = tk.Frame(
            content,
            bg="#111827"
        )

        input_area.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.command_entry = tk.Entry(
            input_area,
            bg="#1f2937",
            fg="white",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief="flat"
        )

        self.command_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 8)
        )

        self.command_entry.bind(
            "<Return>",
            lambda event: self.send_command()
        )

        self.send_button = tk.Button(
            input_area,
            text="Send",
            command=self.send_command,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2"
        )

        self.send_button.pack(
            side="right"
        )

    # ========================================================
    # SIDEBAR BUTTON
    # ========================================================

    def create_button(
        self,
        parent,
        text,
        command
    ):

        button = tk.Button(
            parent,
            text=text,
            command=lambda c=command: self.send_command(c),
            bg="#1f2937",
            fg="#e5e7eb",
            activebackground="#374151",
            activeforeground="white",
            font=("Segoe UI", 10),
            anchor="w",
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

    # ========================================================
    # CHAT
    # ========================================================

    def add_user_message(self, message):

        self.chat.configure(state="normal")

        self.chat.insert(
            tk.END,
            "\nYou\n",
            "user"
        )

        self.chat.insert(
            tk.END,
            message + "\n"
        )

        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def add_bot_message(self, message):

        self.chat.configure(state="normal")

        self.chat.insert(
            tk.END,
            "\nAI Laptop Manager\n",
            "bot"
        )

        self.chat.insert(
            tk.END,
            message + "\n"
        )

        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def add_system_message(self, message):

        self.chat.configure(state="normal")

        self.chat.insert(
            tk.END,
            "\n" + message + "\n",
            "system"
        )

        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    # ========================================================
    # STATUS
    # ========================================================

    def set_busy(self, text="Working..."):

        self.busy = True

        self.status_label.config(
            text="● " + text,
            fg="#fbbf24"
        )

        self.send_button.config(
            state="disabled"
        )

    def set_ready(self):

        self.busy = False

        self.status_label.config(
            text="● Ready",
            fg="#22c55e"
        )

        self.send_button.config(
            state="normal"
        )

        self.command_entry.focus_set()

    # ========================================================
    # MAIN COMMAND
    # ========================================================

    def send_command(self, command=None):

        if self.busy:
            return

        if command is None:
            command = self.command_entry.get().strip()

        if not command:
            return

        self.command_entry.delete(
            0,
            tk.END
        )

        self.add_user_message(
            command
        )

        cmd = command.lower().strip()

        # OPEN ANY FILE
        if cmd.startswith("open "):

            target = command[5:].strip()

            self.open_command(
                target
            )

            return

        # FIND ANY FILE
        if (
            cmd.startswith("find ")
            or cmd.startswith("search ")
            or cmd.startswith("where is ")
        ):

            self.search_command(
                command
            )

            return

        # CLEANUP
        if cmd in [
            "clean my laptop",
            "cleanup",
            "clean laptop"
        ]:

            self.start_cleanup()
            return

        # ORGANIZE
        if cmd in [
            "organize downloads",
            "organize my downloads",
            "organize download"
        ]:

            self.start_organizer()
            return

        # NORMAL CHATBOT COMMAND
        self.run_normal_command(
            command
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search_command(self, command):

        self.set_busy(
            "Searching..."
        )

        cmd = command.lower().strip()

        if cmd.startswith("where is "):

            keyword = command[9:].strip()

        elif cmd.startswith("search "):

            keyword = command[7:].strip()

        else:

            keyword = command[5:].strip()

        for word in [
            "my ",
            "the ",
            "a ",
            "an "
        ]:

            if keyword.lower().startswith(word):
                keyword = keyword[len(word):]

        thread = threading.Thread(
            target=self.perform_search,
            args=(keyword,),
            daemon=True
        )

        thread.start()

    def perform_search(self, keyword):

        try:

            results = self.find_files(
                keyword,
                40
            )

            if not results:

                self.root.after(
                    0,
                    lambda: self.finish_command(
                        f"❌ No files found for '{keyword}'."
                    )
                )

                return

            self.root.after(
                0,
                lambda: self.show_results(
                    results,
                    f"🔎 Found {len(results)} file(s)"
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.finish_command(
                    "❌ Search error:\n\n" + str(e)
                )
            )

    # ========================================================
    # FIND FILES
    # ========================================================

    def find_files(self, keyword, limit=40):

        keyword = keyword.lower().strip()

        home = os.path.expanduser("~")

        locations = [
            os.path.join(home, "Desktop"),
            os.path.join(home, "Documents"),
            os.path.join(home, "Downloads"),
            os.path.join(home, "OneDrive"),
            "D:\\"
        ]

        ignored_parts = [
            "\\windows\\",
            "\\program files\\",
            "\\program files (x86)\\",
            "\\appdata\\local\\temp\\",
            "\\node_modules\\",
            "\\.git\\",
            "\\venv\\",
            "\\__pycache__\\"
        ]

        ignored_extensions = {
            ".lnk",
            ".dat",
            ".tmp",
            ".log",
            ".sys"
        }

        results = []
        seen = set()

        for base in locations:

            if not os.path.exists(base):
                continue

            try:

                for root, dirs, files in os.walk(
                    base,
                    topdown=True
                ):

                    root_lower = root.lower()

                    if any(
                        part in root_lower
                        for part in ignored_parts
                    ):
                        dirs[:] = []
                        continue

                    new_dirs = []

                    for directory in dirs:

                        full_dir = os.path.join(
                            root,
                            directory
                        ).lower()

                        if not any(
                            part in full_dir
                            for part in ignored_parts
                        ):

                            new_dirs.append(
                                directory
                            )

                    dirs[:] = new_dirs

                    for filename in files:

                        full_path = os.path.join(
                            root,
                            filename
                        )

                        if full_path in seen:
                            continue

                        extension = os.path.splitext(
                            filename
                        )[1].lower()

                        if extension in ignored_extensions:
                            continue

                        if keyword in filename.lower():

                            seen.add(
                                full_path
                            )

                            results.append(
                                full_path
                            )

                            if len(results) >= limit:
                                return self.sort_results(
                                    results,
                                    keyword
                                )

            except (
                PermissionError,
                OSError
            ):
                continue

        return self.sort_results(
            results,
            keyword
        )

    def sort_results(
        self,
        results,
        keyword
    ):

        return sorted(
            results,
            key=lambda path: (
                0 if os.path.basename(
                    path
                ).lower().startswith(
                    keyword
                ) else 1,

                os.path.basename(
                    path
                ).lower()
            )
        )

    # ========================================================
    # OPEN COMMAND
    # ========================================================

    def open_command(self, target):

        self.set_busy(
            "Finding file..."
        )

        thread = threading.Thread(
            target=self.find_for_open,
            args=(target,),
            daemon=True
        )

        thread.start()

    def find_for_open(self, target):

        try:

            results = self.find_files(
                target,
                20
            )

            if not results:

                self.root.after(
                    0,
                    lambda: self.finish_command(
                        f"❌ File not found:\n{target}"
                    )
                )

                return

            exact = [
                path for path in results
                if os.path.basename(
                    path
                ).lower() == target.lower()
            ]

            if len(exact) == 1:

                self.root.after(
                    0,
                    lambda p=exact[0]: self.open_file(
                        p
                    )
                )

                return

            if len(results) == 1:

                self.root.after(
                    0,
                    lambda p=results[0]: self.open_file(
                        p
                    )
                )

                return

            self.root.after(
                0,
                lambda: self.show_results(
                    results,
                    f"🔎 Multiple matches for '{target}'"
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.finish_command(
                    "❌ Could not open file:\n\n"
                    + str(e)
                )
            )

    # ========================================================
    # RESULT WINDOW
    # ========================================================

    def show_results(
        self,
        paths,
        title
    ):

        self.set_ready()

        self.add_bot_message(
            title + "\n"
            "Choose a file from the result window."
        )

        # Make sure old result windows don't interfere
        popup = tk.Toplevel(
            self.root
        )

        self.result_windows.append(
            popup
        )

        popup.title(
            "File Results - AI Laptop Manager"
        )

        popup.geometry(
            "850x560"
        )

        popup.minsize(
            650,
            400
        )

        popup.configure(
            bg="#111827"
        )

        popup.protocol(
            "WM_DELETE_WINDOW",
            lambda p=popup: self.close_result_window(p)
        )

        tk.Label(
            popup,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg="#111827",
            fg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            popup,
            text="Click Open to launch the file.",
            font=("Segoe UI", 9),
            bg="#111827",
            fg="#9ca3af"
        ).pack(
            anchor="w",
            padx=20
        )

        container = tk.Frame(
            popup,
            bg="#111827"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        canvas = tk.Canvas(
            container,
            bg="#0f172a",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        list_frame = tk.Frame(
            canvas,
            bg="#0f172a"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=list_frame,
            anchor="nw"
        )

        def update_scroll(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

            canvas.itemconfigure(
                canvas_window,
                width=canvas.winfo_width()
            )

        list_frame.bind(
            "<Configure>",
            update_scroll
        )

        canvas.bind(
            "<Configure>",
            update_scroll
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for path in paths:

            self.create_file_row(
                list_frame,
                path,
                popup
            )

    def create_file_row(
        self,
        parent,
        path,
        popup
    ):

        row = tk.Frame(
            parent,
            bg="#172033"
        )

        row.pack(
            fill="x",
            padx=8,
            pady=5
        )

        filename = os.path.basename(
            path
        )

        directory = os.path.dirname(
            path
        )

        tk.Label(
            row,
            text="📄",
            font=("Segoe UI Emoji", 15),
            bg="#172033",
            fg="white"
        ).pack(
            side="left",
            padx=(10, 8)
        )

        info = tk.Frame(
            row,
            bg="#172033"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True,
            pady=8
        )

        tk.Label(
            info,
            text=filename,
            font=("Segoe UI", 10, "bold"),
            bg="#172033",
            fg="#e5e7eb",
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            info,
            text=directory,
            font=("Segoe UI", 8),
            bg="#172033",
            fg="#6b7280",
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Button(
            row,
            text="Open",
            command=lambda p=path: self.open_file(
                p
            ),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=7,
            cursor="hand2"
        ).pack(
            side="right",
            padx=10
        )

        tk.Button(
            row,
            text="Folder",
            command=lambda p=path: self.open_folder(
                p
            ),
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9),
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(
            side="right"
        )

    # ========================================================
    # FIXED FILE OPEN
    # ========================================================

    def open_file(self, path):

        if not os.path.exists(path):

            messagebox.showerror(
                "File Not Found",
                "This file no longer exists.",
                parent=self.root
            )

            return

        try:

            # Windows launches the file independently.
            # AI Laptop Manager does NOT wait for VLC,
            # Movies & TV, Adobe, etc.
            os.startfile(path)

            self.add_bot_message(
                "✅ Opened:\n"
                + path
            )

            # Bring AI Laptop Manager back to normal state.
            self.root.after(
                100,
                self.restore_gui
            )

        except Exception as e:

            messagebox.showerror(
                "Cannot Open File",
                str(e),
                parent=self.root
            )

            self.restore_gui()

    def restore_gui(self):

        try:

            self.root.deiconify()
            self.root.state("normal")

        except Exception:
            pass

        self.set_ready()

        try:
            self.root.lift()
        except Exception:
            pass

        try:
            self.command_entry.focus_set()
        except Exception:
            pass

    # ========================================================
    # OPEN FOLDER
    # ========================================================

    def open_folder(self, path):

        try:

            folder = os.path.dirname(
                path
            )

            if os.path.exists(folder):

                os.startfile(folder)

                self.root.after(
                    100,
                    self.restore_gui
                )

        except Exception as e:

            messagebox.showerror(
                "Cannot Open Folder",
                str(e),
                parent=self.root
            )

            self.restore_gui()

    # ========================================================
    # CLOSE RESULT WINDOW
    # ========================================================

    def close_result_window(self, popup):

        try:

            if popup in self.result_windows:
                self.result_windows.remove(popup)

            popup.destroy()

        except Exception:
            pass

        self.restore_gui()

    # ========================================================
    # NORMAL CHATBOT COMMAND
    # ========================================================

    def run_normal_command(self, command):

        self.set_busy(
            "Working..."
        )

        thread = threading.Thread(
            target=self.execute_normal_command,
            args=(command,),
            daemon=True
        )

        thread.start()

    def execute_normal_command(self, command):

        output = io.StringIO()

        try:

            with contextlib.redirect_stdout(
                output
            ):

                result = chatbot.handle_command(
                    command
                )

                if result is not None:
                    print(result)

            response = output.getvalue().strip()

            if not response:
                response = "✅ Command completed."

        except Exception as e:

            response = (
                "❌ Something went wrong.\n\n"
                + str(e)
            )

        self.root.after(
            0,
            lambda: self.finish_command(
                response
            )
        )

    def finish_command(self, response):

        self.add_bot_message(
            response
        )

        self.set_ready()

    # ========================================================
    # CLEANUP
    # ========================================================

    def start_cleanup(self):

        self.set_busy(
            "Checking cleanup..."
        )

        thread = threading.Thread(
            target=self.prepare_cleanup,
            daemon=True
        )

        thread.start()

    def prepare_cleanup(self):

        try:

            chatbot.get_cleanup_info()

            message = (
                "🧹 SAFE CLEANUP\n\n"
                "This will clean only safe temporary data "
                "and the Recycle Bin.\n\n"
                "It will NOT delete:\n\n"
                "❌ Downloads\n"
                "❌ Documents\n"
                "❌ Projects\n"
                "❌ Installed programs\n"
                "❌ Windows system files\n\n"
                "Do you want to continue?"
            )

            self.root.after(
                0,
                lambda: self.cleanup_confirmation(
                    message
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.finish_command(
                    "❌ Cleanup check failed:\n\n"
                    + str(e)
                )
            )

    def cleanup_confirmation(self, message):

        self.set_ready()

        answer = messagebox.askyesno(
            "Safe Cleanup",
            message,
            parent=self.root
        )

        if not answer:

            self.add_bot_message(
                "🛑 Cleanup cancelled."
            )

            return

        self.set_busy(
            "Cleaning..."
        )

        self.add_system_message(
            "✅ Cleanup approved."
        )

        thread = threading.Thread(
            target=self.perform_cleanup,
            daemon=True
        )

        thread.start()

    def perform_cleanup(self):

        output = io.StringIO()

        try:

            with contextlib.redirect_stdout(
                output
            ):

                chatbot.cleanup_temp()
                chatbot.empty_recycle_bin()

            response = output.getvalue().strip()

            if not response:

                response = (
                    "✅ Safe cleanup completed."
                )

        except Exception as e:

            response = (
                "❌ Cleanup error:\n\n"
                + str(e)
            )

        self.root.after(
            0,
            lambda: self.finish_command(
                response
            )
        )

    # ========================================================
    # ORGANIZER
    # ========================================================

    def start_organizer(self):

        self.set_busy(
            "Analyzing Downloads..."
        )

        thread = threading.Thread(
            target=self.prepare_organizer,
            daemon=True
        )

        thread.start()

    def prepare_organizer(self):

        downloads = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        categories = {

            "Movies": [
                ".mp4", ".mkv", ".avi",
                ".mov", ".wmv", ".flv",
                ".webm", ".m4v"
            ],

            "Documents": [
                ".pdf", ".doc", ".docx",
                ".txt", ".ppt", ".pptx",
                ".xls", ".xlsx", ".csv"
            ],

            "Images": [
                ".jpg", ".jpeg", ".png",
                ".gif", ".bmp", ".webp"
            ],

            "Audio": [
                ".mp3", ".wav", ".aac",
                ".flac", ".m4a", ".ogg"
            ],

            "Archives": [
                ".zip", ".rar", ".7z",
                ".tar", ".gz"
            ],

            "Software": [
                ".exe", ".msi", ".iso"
            ]
        }

        suggestions = []

        try:

            for name in os.listdir(
                downloads
            ):

                source = os.path.join(
                    downloads,
                    name
                )

                if not os.path.isfile(
                    source
                ):
                    continue

                extension = os.path.splitext(
                    name
                )[1].lower()

                for category, extensions in categories.items():

                    if extension in extensions:

                        suggestions.append(
                            (
                                name,
                                category,
                                source
                            )
                        )

                        break

            if not suggestions:

                self.root.after(
                    0,
                    lambda: self.finish_command(
                        "✅ Downloads is already organized."
                    )
                )

                return

            preview = suggestions[:15]

            message = (
                f"📁 DOWNLOAD ORGANIZER\n\n"
                f"Found {len(suggestions)} file(s).\n\n"
            )

            for name, category, source in preview:

                message += (
                    f"• {name}\n"
                    f"  → {category}\n\n"
                )

            if len(suggestions) > 15:

                message += (
                    f"...and "
                    f"{len(suggestions) - 15} more.\n\n"
                )

            message += (
                "Project folders will NOT be touched.\n"
                "Existing files will NOT be overwritten.\n\n"
                "Organize these files?"
            )

            self.root.after(
                0,
                lambda: self.organizer_confirmation(
                    message,
                    suggestions
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.finish_command(
                    "❌ Organizer error:\n\n"
                    + str(e)
                )
            )

    def organizer_confirmation(
        self,
        message,
        suggestions
    ):

        self.set_ready()

        answer = messagebox.askyesno(
            "Organize Downloads",
            message,
            parent=self.root
        )

        if not answer:

            self.add_bot_message(
                "🛑 Organization cancelled."
            )

            return

        self.set_busy(
            "Organizing..."
        )

        thread = threading.Thread(
            target=self.perform_organizer,
            args=(suggestions,),
            daemon=True
        )

        thread.start()

    def perform_organizer(
        self,
        suggestions
    ):

        moved = 0
        skipped = 0
        errors = 0

        for name, category, source in suggestions:

            try:

                folder = os.path.join(
                    os.path.dirname(source),
                    category
                )

                os.makedirs(
                    folder,
                    exist_ok=True
                )

                destination = os.path.join(
                    folder,
                    name
                )

                if os.path.exists(destination):

                    skipped += 1
                    continue

                shutil.move(
                    source,
                    destination
                )

                moved += 1

            except Exception:

                errors += 1

        response = (
            "📁 ORGANIZATION COMPLETED\n\n"
            f"✅ Moved: {moved}\n"
            f"⏭️ Skipped: {skipped}\n"
            f"❌ Errors: {errors}\n\n"
            "Project folders were not touched."
        )

        self.root.after(
            0,
            lambda: self.finish_command(
                response
            )
        )


# ============================================================
# START
# ============================================================

def main():

    root = tk.Tk()

    app = AILaptopManagerGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()