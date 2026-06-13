import asyncio
from pathlib import Path

class SystemTools:
    @staticmethod
    async def run_cmd(command, cwd=None, timeout=30, admin=False):
        proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd)
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return proc.returncode, stdout.decode(errors="ignore"), stderr.decode(errors="ignore")
        except asyncio.TimeoutError:
            return -1, "", "Timeout"
        except Exception as e:
            return -1, "", str(e)

    @staticmethod
    def read_file(path):
        return Path(path).read_text(encoding="utf-8", errors="ignore")

    @staticmethod
    def write_file(path, content):
        Path(path).write_text(content, encoding="utf-8", errors="ignore")
