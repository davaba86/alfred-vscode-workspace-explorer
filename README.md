# Alfred VSCode Workspace Explorer

Fork of [Acidham/alfred-vscode-workspace-explorer](https://github.com/Acidham/alfred-vscode-workspace-explorer), adding an allow-list so only chosen projects show up.

Alfred workfow to search, explore and open VSCode workspaces. 

<img src="README.assets/Screenshot%202022-10-14%20at%2008.50.08.png" alt="Screenshot 2022-10-14 at 08.50.08" style="zoom:50%;" />

<img src="README.assets/Screenshot%202022-10-14%20at%2008.50.15.png" alt="Screenshot 2022-10-14 at 08.50.15" style="zoom:50%;" />

## Requirements

* Python 3
* VSCode

## Setup

Define path (`workspaces_home`) where VSCode workspaces are stored. The workflow also supports subdirectories in VSCode Workspace folder

Set `workspaces_home` e.g. to /Users/user/vscode-workspaces

Optionally set `Allowed Projects` to a comma or newline separated list of top-level project/folder names (e.g. `mc-automation, mc-career, mc-consulting`). Only those show up in the top-level list; leave empty to show everything in `workspaces_home` (original behaviour). Filtering applies only at the top level, not to subfolders inside an allowed project.
