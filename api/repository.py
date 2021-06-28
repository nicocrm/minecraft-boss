import logging
import os
from os import path

from pyjavaproperties import Properties

from models import Server

LOG = logging.getLogger(__name__)


class Repository:
    def __init__(self, minecraft_dir):
        self.minecraft_dir = minecraft_dir

    def _get_server(self, server_dir):
        p = Properties()
        with open(path.join(server_dir, "server.properties")) as f:
            p.load(f)

        return Server(
            name=path.basename(server_dir),
            description=p["motd"],
            is_running=False,
        )

    def list_servers(self):
        """
        Return list of servers (directories under minecraft_dir that contain a serverstart.sh file)
        """
        for d in os.listdir(self.minecraft_dir):
            server_dir = path.join(self.minecraft_dir, d)
            if path.exists(path.join(server_dir, "server.properties")) and path.exists(
                path.join(server_dir, "serverstart.sh")
            ):
                try:
                    yield self._get_server(server_dir)
                except Exception:
                    LOG.warn("Error getting server", exc_info=True)
