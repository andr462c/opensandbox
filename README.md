# opensandbox

A CLI tool to manage podman-based development sandboxes with OpenCode.

## Features

- Build Arch Linux-based container images with OpenCode pre-installed
- Create persistent sandboxes with mounted directories
- Start/attach to existing sandboxes
- List and remove sandboxes
- Uses crun with krun annotation for isolated KVM environments
- OpenCode configured to ask permission before running bash commands

## Installation

```bash
./install.sh
```

Add `~/.local/bin` to your PATH if needed.

## Usage

```bash
# Build the container image
opensandbox build

# Create a new sandbox (requires tag and mount path)
opensandbox create <tag> <mount>

# Start/attach to an existing sandbox
opensandbox start <tag>

# List all sandboxes
opensandbox list

# Remove a sandbox
opensandbox remove <tag>
```

## Configuration

Edit `opencode.jsonc` to customize OpenCode settings:
- `permission.bash`: Set to "ask" to require approval for bash commands
- `enabled_providers`: Uncomment and set to `["github-copilot"]` to restrict to Copilot models

## Requirements

- podman
- crun (with krun support)
- python3
