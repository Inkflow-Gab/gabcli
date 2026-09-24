#!/usr/bin/env sh
# Install GabCli from a downloaded source archive without requiring a package manager.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PREFIX=${GABCLI_PREFIX:-"$HOME/.local"}
LIB="$PREFIX/lib/gabcli"
BIN="$PREFIX/bin/gabcli"

mkdir -p "$LIB" "$PREFIX/bin"
cp "$ROOT/gabcli.py" "$ROOT/gabcli_ui.py" "$ROOT/gabcli_diff.py" "$LIB/"
cat > "$BIN" <<EOF
#!/usr/bin/env sh
exec python3 "$LIB/gabcli.py" "\$@"
EOF
chmod +x "$BIN"

echo "GabCli installed to $BIN"
case ":${PATH}:" in
  *":$PREFIX/bin:"*) ;;
  *) echo "Add this to your shell profile: export PATH=\"$PREFIX/bin:\$PATH\"" ;;
esac
