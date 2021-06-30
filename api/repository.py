import asyncio
import logging
import os
from os import path

from pyjavaproperties import Properties

from exceptions import ServerControlException
from models import Server

LOG = logging.getLogger(__name__)


class Repository:
    def __init__(self, minecraft_dir):
        self.minecraft_dir = minecraft_dir

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

    async def _get_server(self, server_name):
        async def get_is_running():
            p = await asyncio.create_subprocess_exec(
                "/usr/bin/systemctl", "status", "minecraft@" + server_name
            )
            await p.wait()
            return p.returncode == 0

        props = Properties()
        server_dir = path.join(self.minecraft_dir, server_name)
        with open(path.join(server_dir, "server.properties")) as f:
            props.load(f)
        return Server(
            name=server_name,
            description=props["motd"],
            port=int(str(props["server-port"])),
            is_running=await get_is_running(),
        )

    async def list_servers(self):
        """
        Return list of servers (directories under minecraft_dir that contain a serverstart.sh file)
        """
        for server_name in os.listdir(self.minecraft_dir):
            server_dir = path.join(self.minecraft_dir, server_name)
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
