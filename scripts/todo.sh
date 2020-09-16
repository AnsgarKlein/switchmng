#!/bin/bash


EXPRESSION="#( )*TODO[:| |\n]"
FILES="*.py"
FILES=`find . -path './env' -prune -o -type f -iname '*.py' -print`


# Check what file name is the longest
MAXFILELENGTH=0
for FILE in $FILES ; do
  # Check if it contains a match at all
  if [[ -z `grep -n -E "$EXPRESSION" "$FILE"` ]]; then
    continue
  fi

  if [[ ${#FILE} -gt $MAXFILELENGTH ]]; then
    MAXFILELENGTH=${#FILE}
  fi
done


# Go through all files
for FILE in $FILES ;do
  # Grep for todos in file
  OUT=`grep -n -E "$EXPRESSION" "$FILE"`

  # Check if there was a match at all
  if [[ -z "$OUT" ]]; then
    continue
  fi

  # Add padding to file name
  PAD='......................................'
  PADNUM=$(($MAXFILELENGTH-${#FILE}))
  FILE=`printf "%${MAXFILELENGTH}s\n" "$FILE"`

  # Go through each match
  while read -r LINE; do
    # Extract line number and add padding to the right
    LINENUMBER=`echo "$LINE" | cut -d: -f1`
    LINENUMBER=`printf "%-4d" "$LINENUMBER"`

    # Extract match and remove leading whitespaces
    LINEMATCH=`echo "$LINE" | cut -d: -f2-`
    LINEMATCH=`echo "$LINEMATCH" | sed 's/^[ \t]*//'`

    printf "%s:%s    %s\n" "$FILE" "$LINENUMBER" "$LINEMATCH"
  done <<< "$OUT"
done
