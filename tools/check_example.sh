#!/bin/sh

set -e

test -e setup.py || { echo 'must run from repo root' >&2; exit 1; }

cd example/
outfile=$( mktemp --tmpdir XXX.out )

# In Django before 1.10, ``manage.py check`` does not support ``--fail-level``,
# so we have to process its output manually.
./manage.py check >"$outfile" 2>&1
cat "$outfile"      # Show to the user.
grep -q 'identified no issues' "$outfile"

./manage.py test >"$outfile" 2>&1 || true
cat "$outfile"      # Show to the user.
grep -q 'E 1038' "$outfile"
grep -q 'FAILED' "$outfile"

rm "$outfile"
