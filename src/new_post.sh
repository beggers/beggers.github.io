#!/bin/bash

SEPARATOR="---"


function main () {
  read -p "Title: " TITLE
  read -p "Slug: " SLUG
  read -p "Tags: " TAGS
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
