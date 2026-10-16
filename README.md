# Alfred VSCode Workspace Explorer

Fork of [Acidham/alfred-vscode-workspace-explorer](https://github.com/Acidham/alfred-vscode-workspace-explorer), adding an allow-list so only chosen projects show up.

Alfred workfow to search, explore and open VSCode workspaces. 

<img src="README.assets/Screenshot%202022-10-14%20at%2008.50.08.png" alt="Screenshot 2022-10-14 at 08.50.08" style="zoom:50%;" />

<img src="README.assets/Screenshot%202022-10-14%20at%2008.50.15.png" alt="Screenshot 2022-10-14 at 08.50.15" style="zoom:50%;" />

## Requirements

* Python 3
* VSCode

## Setup

Alfred preferences (including these settings) sync as one file across every Mac a workflow is installed on (e.g. via Dropbox/iCloud), so Configure Workflow has two computer rows, each with its own folder and project filter:

| Field | Purpose |
|---|---|
| Computer 1 Name | Exact Mac name this row applies to. Leave blank to make this row the default (used on any computer not named in a row). |
| Computer 1 Workspaces | VS Code Workspaces folder used on that computer. |
| Computer 1 Allowed Projects | Optional comma separated list of top-level project/folder names to show, e.g. `mc-automation, mc-career, mc-product-*`. Supports `fnmatch` wildcards (`*`, `?`, `[seq]`). Leave empty to show everything in that computer's Workspaces folder. |
| Computer 1 Denied Projects | Optional comma separated list to hide, even if matched by Allowed Projects, e.g. `mc-secret`. Same wildcard support. Leave empty to deny nothing. |
| Computer 2 Name / Workspaces / Allowed Projects / Denied Projects | Same 4 fields, for a second computer. |

Find your Mac's name in System Settings > General > About > Name, or run `scutil --get ComputerName` in Terminal.

**Single computer / same settings everywhere:** just fill in Computer 1's Workspaces (and optionally Allowed Projects), leave Computer 1 Name and all of Computer 2 blank. That row becomes the default used on every machine.

**Two different computers:** set each row's Name to that Mac's exact computer name, plus its own Workspaces folder and Allowed Projects. Example:

- Computer 1 Name: `work-mbp`, Workspaces: `~/git-repos`, Allowed Projects: `mc-product-*, mc-career`
- Computer 2 Name: `home-mac`, Workspaces: `~/code`, Allowed Projects: `personal-*`

Filtering applies only at the top level of the Workspaces folder, not to subfolders inside an allowed project.
