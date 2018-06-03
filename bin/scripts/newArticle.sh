#!/bin/bash

ARTICLE=$1
AUTHOR=$2

if [ -z "$ARTICLE" ]; then
  echo "Error: Missing arg 1 (ARTICLE NAME)"
  exit
fi

if [ -z "$AUTHOR" ]; then
  echo "Error: Missing arg 1 (AUTHOR NAME)"
  exit 1
fi

if [ ! -d "../Work/Template/" ]; then
	echo "Error: Make sure you are in a seasonal directory (F2018M)"
	exit 1
fi

if [ ! -d "./images" ]; then
  mkdir images
fi

if [ ! -d "$AUTHOR" ]; then
  mkdir $AUTHOR;
fi

cp ../Work/Template/template.html $AUTHOR/$ARTICLE.html
mkdir images/$ARTICLE
