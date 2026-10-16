#!/usr/bin/python3

import fnmatch
import os
import platform
import subprocess
import sys
from pathlib import PurePath

from Alfred3 import Items, Tools


def get_files(r_path):
    file_list = list()
    for root, dirs, files in os.walk(r_path):
        f_lst = ["{0}/{1}".format(root, f) for f in files]
        file_list.extend(f_lst)
    return file_list


def get_dirs(r_path):
    dir_list = list()
    for p in os.listdir(r_path):
        if os.path.isdir(r_path):
            d = "{0}/{1}".format(r_path, p)
            dir_list.append(d)
    return dir_list


def get_allowed(raw):
    if not raw:
        return set()
    parts = [p.strip().lower() for chunk in raw.splitlines() for p in chunk.split(",")]
    return set(p for p in parts if p)


def get_computer_name():
    try:
        name = (
            subprocess.check_output(["scutil", "--get", "ComputerName"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
        if name:
            return name
    except Exception:
        pass
    return platform.node()


def resolve_for_computer(computer_name):
    """Pick (workspaces_home, allowed_projects, denied_projects) for the current Mac.

    Two fixed computer rows are configurable (Computer 1/2 Name, Workspaces,
    Allowed Projects, Denied Projects). A row whose Name matches computer_name
    wins; a row with an empty Name is the default, used when no row's name
    matches. Alfred preferences (and these settings) sync as one file across
    every Mac a workflow is installed on, so this lets one synced config hold
    different values per machine instead of clobbering the setting on
    whichever machine saved last.
    """
    rows = [
        (
            Tools.getEnv("computer1_name"),
            Tools.getEnv("computer1_workspaces_home"),
            Tools.getEnv("computer1_allowed_projects"),
            Tools.getEnv("computer1_denied_projects"),
        ),
        (
            Tools.getEnv("computer2_name"),
            Tools.getEnv("computer2_workspaces_home"),
            Tools.getEnv("computer2_allowed_projects"),
            Tools.getEnv("computer2_denied_projects"),
        ),
    ]
    computer_name_l = computer_name.lower()
    match = None
    default = None
    for name, home, allowed, denied in rows:
        if not (name.strip() or home.strip() or allowed.strip() or denied.strip()):
            continue  # row left entirely blank, not in use
        if name.strip():
            if name.strip().lower() == computer_name_l:
                match = (home, allowed, denied)
        else:
            default = (home, allowed, denied)
    return match or default or (str(), str(), str())


Tools.logPyVersion()

f_path = Tools.getEnv("mypath")
# TODO: Debugging line below
Tools.log(f"this is f_path: {f_path}")
computer_name = get_computer_name()
resolved_home, resolved_allowed, resolved_denied = resolve_for_computer(computer_name)

ws_home_cfg = os.path.expanduser(resolved_home or str())
ws_home = f_path if f_path else ws_home_cfg
at_root = (not f_path) or (os.path.normpath(f_path) == os.path.normpath(ws_home_cfg))
p_path = str(PurePath(f_path).parent) if f_path and not at_root else str()

query = Tools.getArgv(1)
if not ws_home or not os.path.isdir(ws_home):
    wf = Items()
    wf.setItem(
        title="No VS Code Workspaces configured for this computer",
        subtitle=f"Computer name: {computer_name}. Add a row for it in Configure Workflow.",
        valid=False,
    )
    wf.addItem()
    wf.write()
    sys.exit()

if query == str():
    it = sorted(get_dirs(ws_home))
else:
    it = sorted(get_files(ws_home))

allowed = get_allowed(resolved_allowed)
denied = get_allowed(resolved_denied)
if at_root and allowed:
    it = [i for i in it if any(fnmatch.fnmatch(PurePath(i).stem.lower(), pat) for pat in allowed)]
if at_root and denied:
    it = [i for i in it if not any(fnmatch.fnmatch(PurePath(i).stem.lower(), pat) for pat in denied)]

wf = Items()
if p_path:
    wf.setItem(title="Back", arg=p_path)
    wf.setIcon(m_path="back.png", m_type="image")
    wf.addItem()
if len(it) > 0:
    for i in it:
        # TODO: Remove just for debugging
        pp = PurePath(i).stem.lower()
        if (query == str() or query.lower() in PurePath(i).stem.lower()) and not (
            os.path.basename(i).startswith(".")
        ):
            ic = "folder.png" if os.path.isdir(i) else "workspace.png"
            sub = "Folder" if os.path.isdir(i) else "Workspace in VSCode"
            title = os.path.basename(i).replace(".code-workspace", "")
            wf.setItem(title=title, subtitle=f"\u23ce to open {sub}", arg=i)
            wf.setIcon(m_path=ic, m_type="image")
            wf.addItem()
    if len(wf.getItems(response_type="dict").get("items")) == 0:
        wf.setItem(title="Search does not match a workspace", subtitle="...try again", valid=False)
        wf.addItem()
else:
    wf.setItem(title="No Workspace files or Folders found", valid=False)
    wf.addItem()
wf.write()
