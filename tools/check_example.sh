#!/bin/sh

set -e

test -e setup.py || { echo 'must run from repo root' >&2; exit 1; }

cd example/

./manage.py check --fail-level WARNING

outfile=$(mktemp --tmpdir XXX.out)

./manage.py test >"$outfile" 2>&1 || true
cat "$outfile"      # Show to the user.
grep -q 'E 1038' "$outfile"
grep -q 'FAILED' "$outfile"

rm "$outfile"
