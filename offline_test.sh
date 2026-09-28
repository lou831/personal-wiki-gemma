#!/bin/zsh
# Offline acceptance run. Verifies the Mac is disconnected, then runs the CLI fresh:
# help, stats, a full local-Gemma ingest, a duplicate-check ingest of vault/raw,
# search, ask, a real chat session with a follow-up, the full test suite, and the
# vault check. Everything is saved to outputs/runs/<date time> Offline Run/.
cd "$(dirname "$0")"
export RUN_DIR="outputs/runs/$(date '+%Y-%m-%d %H%M') Offline Run"
mkdir -p "$RUN_DIR"
LOG="$RUN_DIR/Terminal Log.txt"
SOURCE="vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf"
step() { echo "\n\$ $*"; "$@" 2>&1 | grep -v "Loading weights\|fontTools"; }

{
  echo "=== Offline run $(date) ==="
  echo "--- OS network check"
  networksetup -getairportpower en0
  for i in {1..10}; do route -n get default >/dev/null 2>&1 || break; sleep 2; done
  if route -n get default >/dev/null 2>&1; then
    echo "note: a default route is still present"
  else
    echo "no default route"
  fi
  for host in https://huggingface.co https://www.google.com https://pypi.org; do
    if curl -s --max-time 5 -o /dev/null "$host"; then
      echo "ABORT: $host is reachable — the Mac is online (check Wi-Fi, Ethernet/dock, iPhone hotspot)."
      exit 1
    fi
  done
  echo "offline confirmed: huggingface.co, google.com and pypi.org are all unreachable"
  echo "device: $(sysctl -n machdep.cpu.brand_string), $(( $(sysctl -n hw.memsize) / 1073741824 )) GB unified memory, macOS $(sw_vers -productVersion)"

  echo "\n=== 1. help (fresh CLI process)"
  step ./wiki --help

  echo "\n=== 2. stats before ingest"
  step ./wiki stats

  echo "\n=== 3. ingest: full local-Gemma re-draft of one source (offline)"
  echo "\$ /usr/bin/time -l ./wiki ingest \"$SOURCE\" --force"
  /usr/bin/time -l ./wiki ingest "$SOURCE" --force 2>&1 | grep -v "Loading weights\|fontTools" \
    | grep -v "average\|block \|messages \|signals \|swaps\|page \|context switches\|instructions\|cycles"

  echo "\n=== 4. ingest the whole raw folder again: must report 'already ingested', no duplicates"
  step ./wiki ingest ./vault/raw

  echo "\n=== 5. search: original passages, no model"
  step ./wiki search "platform screen doors safety" -k 3

  echo "\n=== 6. ask: standalone cited answer"
  step ./wiki ask "What percentage of the grade is the final group presentation in the Business of Energy Transition course?" --mode local

  echo "\n=== 7. chat: a real session (capabilities, draft, follow-up, /ask, /exit)"
  echo "\$ ./wiki chat   (typed input below)"
  printf '%s\n' "what can you help me with?" \
    "Draft a three-sentence message to my study group proposing we meet Thursday at 7 to review for the energy transition memo." \
    "make that shorter" \
    "/ask What is the maximum length of each written memo in the Business of Energy Transition course?" \
    "/exit" | tee /dev/stderr | ./wiki chat 2>&1 | grep -v "Loading weights"

  echo "\n=== 8. full test suite (4 ask tests + mode checks), evidence written to $RUN_DIR"
  step ./wiki test

  echo "\n=== 9. vault check"
  step ./wiki check
  echo "\n=== done $(date) ==="
} 2>&1 | tee "$LOG"
echo "\nSaved: $RUN_DIR"
