import asyncio
import glob
import logging
import os
from os import path

from fastapi import UploadFile
from pyjavaproperties import Properties

from exceptions import ServerControlException
from models import Server

LOG = logging.getLogger(__name__)


class Repository:
    def __init__(self, minecraft_dir):
        self.minecraft_dir = minecraft_dir

    def _server_dir(self, server_name: str):
        assert "/" not in server_name
        return path.join(self.minecraft_dir, server_name)

    async def _control_server(self, operation, server_name):
        p = await asyncio.create_subprocess_exec(
            path.join(self.minecraft_dir, "serverctl"),
            operation,
            server_name,
            cwd=self.minecraft_dir,
        )
        _, stderr = await p.communicate()
        if p.returncode != 0:
            LOG.warning("Error in server %s [%s]: %s", operation, server_name, stderr)
            raise ServerControlException("Error in server operation")
        await asyncio.sleep(1)
        return await self._get_server(server_name)

    def _get_mods(self, server_dir: str):
        return [
            path.splitext(path.basename(f))[0]
            for f in glob.glob(path.join(server_dir, "mods", "*.jar"))
        ]

    async def _get_server(self, server_name: str):
        async def get_is_running():
            p = await asyncio.create_subprocess_exec(
                "/usr/bin/systemctl", "status", "minecraft@" + server_name
            )
            await p.wait()
            return p.returncode == 0

        props = Properties()
        server_dir = self._server_dir(server_name)
        with open(path.join(server_dir, "server.properties")) as f:
            props.load(f)
        return Server(
            name=server_name,
            description=props["motd"],
            port=int(str(props["server-port"])),
            is_running=await get_is_running(),
            mods=self._get_mods(server_dir),
        )

    async def list_servers(self):
        """
        Return list of servers (directories under minecraft_dir that contain a serverstart.sh file)
        """
        for server_name in os.listdir(self.minecraft_dir):
            server_dir = self._server_dir(server_name)
            if path.exists(path.join(server_dir, "server.properties")) and path.exists(
                path.join(server_dir, "serverstart.sh")
            ):
                try:
                    yield await self._get_server(server_name)
                except Exception:
                    LOG.warning("Error getting server", exc_info=True)

    async def start_server(self, server_name):
        return await self._control_server("start", server_name)

    async def stop_server(self, server_name):
        return await self._control_server("stop", server_name)

    async def remove_mod(self, server_name: str, mod_name: str):
        assert "/" not in mod_name
        server_dir = self._server_dir(server_name)
        mod_path = path.join(server_dir, "mods", mod_name + ".jar")
        os.unlink(mod_path)
        return await self._get_server(server_name)

    async def add_mod(self, server_name: str, filename: str, data: bytes):
        assert "/" not in filename
        server_dir = self._server_dir(server_name)
        with open(path.join(server_dir, "mods", filename), "wb") as outf:
            outf.write(data)
        return await self._get_server(server_name)
