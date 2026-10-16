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

Optionally set `Allowed Projects` to a comma separated list of top-level project/folder names (e.g. `mc-automation, mc-career, mc-product-*`). Entries support `fnmatch` wildcards (`*`, `?`, `[seq]`), so `mc-product-*` matches `mc-product-compass-flow`, `mc-product-fluent-steps`, etc. Only matching entries show up in the top-level list; leave empty to show everything in `workspaces_home` (original behaviour). Filtering applies only at the top level, not to subfolders inside an allowed project.

### Per-computer settings

Alfred preferences (including these settings) sync as one file across every Mac they're installed on (e.g. via Dropbox/iCloud). If your Macs need different values, both `VS Code Workspaces` and `Allowed Projects` support per-computer overrides in the same field:

```
ComputerName: value-for-that-computer; OtherComputerName: value-for-that-one
```

- Segments are separated by `;`.
- A segment with no `ComputerName:` prefix is the default, used on any computer not explicitly listed.
- Find your Mac's name in System Settings > General > About > Name, or run `scutil --get ComputerName` in Terminal.

Example `Allowed Projects`:

```
mc-automation; work-mbp: mc-product-*, mc-career; home-mac: personal-*
```

This shows only `mc-automation` on any unlisted computer, `mc-product-*`/`mc-career` on `work-mbp`, and `personal-*` on `home-mac`. If you don't need per-computer overrides, just use a plain value as before, no `;` or `:` needed.
