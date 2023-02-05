#!/bin/bash

# !!!!!!
# Don't run this script from the scripts/ directory. If you do, it won't
# be able to find ./print_tags.py. Instead, run it from .. (src/) via the
# softlink.
# !!!!!!

SEPARATOR="---"

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
  echo "published: '$TODAY'" >> $FILE
  echo "updated: '$TODAY'" >> $FILE
  echo "tags: [$TAGS]" >> $FILE
  echo $SEPARATOR >> $FILE

  vim $FILE

  git add $FILE && git commit -m 'first draft of $FILE'
}

main
