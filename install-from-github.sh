#!/usr/bin/env sh
# Public-release installer. No GitHub token is needed for a public repository.
set -eu

REPO=${1:-${GABCLI_REPO:-}}
VERSION=${2:-${GABCLI_VERSION:-v0.3.0}}

if [ -z "$REPO" ]; then
  echo "Usage: install-from-github.sh OWNER/REPOSITORY [TAG]" >&2
  echo "Example: install-from-github.sh yourname/gabcli v0.3.0" >&2
  exit 2
fi

PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 is required. Install Python 3.9+ first." >&2
  exit 2
fi

VERSION_NUMBER=${VERSION#v}
URL="https://github.com/$REPO/releases/download/$VERSION/gabcli-${VERSION_NUMBER}-py3-none-any.whl"
TMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t gabcli)
trap 'rm -rf "$TMP_DIR"' EXIT
WHEEL="$TMP_DIR/gabcli-${VERSION_NUMBER}-py3-none-any.whl"

echo "Downloading GabCli $VERSION from github.com/$REPO ..."
if command -v curl >/dev/null 2>&1; then
  curl -fL --retry 3 --progress-bar "$URL" -o "$WHEEL"
elif command -v wget >/dev/null 2>&1; then
  wget -q --show-progress "$URL" -O "$WHEEL"
else
  echo "curl or wget is required to download GabCli." >&2
  exit 2
fi

"$PYTHON" -m pip install --user "$WHEEL"
echo "GabCli installed. Put the user Python bin directory on PATH if needed."
echo "Run: gabcli"
