#!/bin/bash

# !!!!!!
# Don't run this script from the scripts/ directory. If you do, it won't
# be able to find ./print_tags.py. Instead, run it from .. (src/) via the
# softlink.
# !!!!!!

SEPARATOR="---"
STUBFILE="./stub.mdx"

function main () {
  read -p "Title: " TITLE
  read -p "Slug: " SLUG
  TAGS=$(python $(pwd)/scripts/print_tags.py)
  read -p "Tags ($TAGS): " TAGS
  TODAY=$(date +"%Y %b %d")

  FILE="_posts/$SLUG.mdx"

  touch $FILE
  echo $SEPARATOR >> $FILE
  echo "title: $TITLE" >> $FILE
  echo "slug: $SLUG" >> $FILE
  echo "publish: false" >> $FILE
  echo "published: '$TODAY'" >> $FILE
  echo "updated:" >> $FILE
  echo "tags: [$TAGS]" >> $FILE
  echo $SEPARATOR >> $FILE
  cat $STUBFILE >> $FILE

  git add $FILE && git commit -m "stub for $FILE"
}

main
