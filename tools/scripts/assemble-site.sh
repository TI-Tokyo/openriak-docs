#!/usr/bin/env sh
set -eu

for argument in "$@"; do
  case "$argument" in -h|--help)
    cat <<'OPENRIAK_HELP'
Validate and merge the core and archive Hugo outputs into one static site.
Archives may own only archived-technical-blog/ and archived-mailing-list/;
paths must not overlap with core. Replaces DESTINATION after validation.

Usage: assemble-site.sh CORE_OUTPUT ARCHIVE_OUTPUT DESTINATION

Arguments:
  CORE_OUTPUT       Existing core build directory (required).
  ARCHIVE_OUTPUT    Existing archive build directory (required).
  DESTINATION       Directory to replace with the assembled site (required).
  -h, --help        Show help and exit without validating or changing files.

Relative paths use the current directory.
OPENRIAK_HELP
    exit 0
    ;;
  esac
done

core=${1:-}
archives=${2:-}
destination=${3:-}

if [ ! -d "$core" ] || [ ! -d "$archives" ] || [ -z "$destination" ]; then
  echo 'Usage: assemble-site.sh CORE_OUTPUT ARCHIVE_OUTPUT DESTINATION' >&2
  exit 2
fi

case "$destination" in ''|/) echo 'Refusing unsafe assembly destination.' >&2; exit 2 ;; esac

# The archive build may only own its two URL subtrees. This catches accidental
# sitemaps, shared assets, or future content before they can overwrite core files.
find "$archives" -type f -print | while IFS= read -r source; do
  relative=${source#"$archives"/}
  case "$relative" in
    archived-technical-blog/*|archived-mailing-list/*) ;;
    *) echo "Archive build produced an unexpected path: $relative" >&2; exit 1 ;;
  esac
  if [ -e "$core/$relative" ]; then
    echo "Core and archive builds both own: $relative" >&2
    exit 1
  fi
done

rm -rf "$destination"
mkdir -p "$destination"
cp -a "$core/." "$destination/"
cp -a "$archives/." "$destination/"
