#!/usr/bin/env sh
set -eu

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
