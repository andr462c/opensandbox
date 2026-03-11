#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/bin"

mkdir -p "$INSTALL_DIR"
ln -sf "$SCRIPT_DIR/opensandbox.py" "$INSTALL_DIR/opensandbox"

echo "Installed opensandbox to $INSTALL_DIR/opensandbox (symlink to $SCRIPT_DIR/opensandbox.py)"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Add the following to your shell config:"
    echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
fi
