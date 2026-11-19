#!/bin/zsh

# One-click local owner-review launcher for AOC-002.
# It serves only the repository's public/ directory on the loopback interface.

set -u

SCRIPT_DIR="${0:A:h}"
REPOSITORY_DIR="${SCRIPT_DIR:h:h}"
PUBLIC_DIR="$REPOSITORY_DIR/public"
READER_FILE="$PUBLIC_DIR/review/aoc-002/index.html"
PORT=4174
READER_URL="http://127.0.0.1:${PORT}/review/aoc-002/index.html"
LOG_FILE="${TMPDIR:-/tmp}/aoc-002-owner-review-server.log"
PID_FILE="${TMPDIR:-/tmp}/aoc-002-owner-review-server.pid"

fail() {
  local message="$1"
  print -u2 -- "AOC-002 could not open."
  print -u2 -- "$message"
  /usr/bin/osascript -e "display alert \"AOC-002 could not open\" message \"$message\" as critical" >/dev/null 2>&1 || true
  print -- "You can close this window."
  read -k 1 "?Press any key to close."
  exit 1
}

reader_is_ready() {
  /usr/bin/curl --silent --show-error --fail --max-time 2 "$READER_URL" 2>/dev/null |
    /usr/bin/grep --quiet "AOC-002"
}

[[ -d "$PUBLIC_DIR" ]] || fail "The public reader folder is missing. Keep this launcher inside the Atlas of Consequences/content/AOC-002 folder."
[[ -f "$READER_FILE" ]] || fail "The AOC-002 reader file is missing from public/review/aoc-002."
[[ -x /usr/bin/python3 ]] || fail "This Mac cannot find the built-in Python needed to run the local reader."

if ! reader_is_ready; then
  if /usr/sbin/lsof -nP -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
    fail "Another application is already using local port ${PORT}. Close that application, then double-click this launcher again."
  fi

  (
    cd "$PUBLIC_DIR" || exit 1
    /usr/bin/nohup /usr/bin/python3 -m http.server "$PORT" --bind 127.0.0.1 >"$LOG_FILE" 2>&1 &
    print -- $! >"$PID_FILE"
  )

  for attempt in {1..40}; do
    reader_is_ready && break
    /bin/sleep 0.1
  done

  reader_is_ready || fail "The local reader server did not start. Details were saved in $LOG_FILE."
fi

/usr/bin/open "$READER_URL" || fail "The local reader started, but macOS could not open the browser. The reader address is $READER_URL."

print -- "AOC-002 is open in your browser."
print -- "You can close this window; the local reader will remain available."
exit 0
