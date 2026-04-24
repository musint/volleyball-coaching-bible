#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(git rev-parse --show-toplevel)
HOOK="$REPO_ROOT/.git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# Block commit if broken-wikilink count regresses or invariants are violated.
set -uo pipefail
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"
if ! command -v python >/dev/null 2>&1; then
  echo "pre-commit: python not found; skipping lint"
  exit 0
fi
python tools/lint.py >/dev/null 2>&1
EXIT=$?
if [ "$EXIT" -ne 0 ]; then
  echo "pre-commit: wiki lint failed (exit $EXIT). See wiki/lint-report.md."
  exit "$EXIT"
fi
exit 0
EOF
chmod +x "$HOOK"
echo "Installed $HOOK"
