#!/usr/bin/env bash
# Runs the service locally and saves the real command + output files the
# submission form asks for. Run it yourself in your lab terminal, from the
# repo root, then paste each file's contents into the matching question.
#
#   bash scripts/capture-outputs.sh
#
# Produces: rest-create-done rest-list-done rest-read-done rest-update-done
#           rest-delete-done security-headers-done kube-app-output
set -u
PORT="${PORT:-5000}"
BASE="http://localhost:${PORT}"
OUT="${OUT:-captured-outputs}"
H='Content-Type: application/json'
mkdir -p "$OUT"

rm -f instance/accounts.db
flask --app wsgi run --port "$PORT" >/dev/null 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null' EXIT
sleep 3

run() {  # run <outfile> <command...>: record the command, then its output
  local file="$OUT/$1"; shift
  { echo "\$ $*"; "$@"; echo; } > "$file" 2>&1
}

run rest-create-done curl -s -i -X POST "$BASE/accounts" -H "$H" \
  -d '{"name":"John Doe","email":"john@example.com","address":"1 Main St","phone_number":"555-1234"}'
run rest-list-done   curl -s -i "$BASE/accounts"
run rest-read-done   curl -s -i "$BASE/accounts/1"
run rest-update-done curl -s -i -X PUT "$BASE/accounts/1" -H "$H" \
  -d '{"name":"John Doe","email":"john@example.com","address":"2 Side St","phone_number":"555-1234"}'
run rest-delete-done curl -s -i -X DELETE "$BASE/accounts/1"

# Task 26: JSON from the root URL (use port 8080 in the lab browser/Docker run)
run kube-app-output  curl -s "$BASE/"

# Task 23: nosetests output (all tests passing)
{ echo '$ nosetests'; nosetests 2>&1; } > "$OUT/security-headers-done"

echo "Saved to $OUT/:"; ls -1 "$OUT"
