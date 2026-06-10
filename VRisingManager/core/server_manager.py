import os
import subprocess
import threading


class ServerManager:
    def __init__(self, server_dir):
        self.server_dir = server_dir
        self.proc = None
        self.steamid = ""

    def start(self, server_name, on_line=None, on_status=None):
        if self.proc:
            return self.proc

        if not self.server_dir:
            raise FileNotFoundError("Diretório do servidor não encontrado.")

        exe = os.path.join(self.server_dir, "VRisingServer.exe")
        if not os.path.isfile(exe):
            raise FileNotFoundError("VRisingServer.exe não encontrado.")

        env = os.environ.copy()
        env["SteamAppId"] = "1604030"

        self.proc = subprocess.Popen(
            [exe, "-persistentDataPath", ".\\save-data", "-serverName", server_name, "-saveName", "world1"],
            cwd=self.server_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        threading.Thread(target=self._reader, args=(on_line, on_status), daemon=True).start()
        return self.proc

    def _reader(self, on_line=None, on_status=None):
        try:
            for line in iter(self.proc.stdout.readline, ""):
                if on_line:
                    on_line(line)

                if "SteamID:" in line:
                    steamid = line.split("SteamID:")[1].strip()
                    self.steamid = steamid
                    if on_status:
                        on_status(f"Online | SteamID: {steamid}", "#00CC66")

            if self.proc and self.proc.poll() is not None:
                if on_status:
                    on_status("Status: Offline", "#FF4444")

        except Exception as exc:
            if on_line:
                on_line(f"\nERRO READER:\n{exc}\n")

    def stop(self):
        if self.proc:
            self.proc.kill()
            self.proc = None
            return True
        return False
