from glob import glob
from os import path
from tempfile import mkdtemp
from typing import List
from urllib.parse import parse_qs, urlparse

from steamctl.commands.workshop.gcmds import cmd_workshop_download

from nfcli import STEAM_API_KEY, STEAM_USERNAME


def download_workshop(id: int) -> List[str]:
    args = get_args(id)
    cmd_workshop_download(args)
    return get_files(args.output)


def get_args(id: int) -> object:
    args = type("", (), {})()
    args.anonymous = False
    args.apikey = STEAM_API_KEY
    args.cell_id = None
    args.id = id
    args.output = mkdtemp()
    args.user = STEAM_USERNAME
    args.no_progress = True
    args.no_directories = False
    return args


def get_files(directory: str) -> List[str]:
    return glob(path.join(directory, "*.fleet")) + glob(path.join(directory, "*.ship"))


def get_workshop_id(link_data: List[str]) -> int:
    url = urlparse(link_data[0])
    if url.hostname != "steamcommunity.com" or url.path != "/sharedfiles/filedetails/":
        return 0
    params = parse_qs(url.query)
    if "id" not in params:
        return 0
    return int(params["id"][0])