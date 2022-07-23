#!/usr/bin/env bash
#
# Creates the screenshots required by AppStore Connect by resizing the
# image files in the 'media/App Store/Screenshot/Original' directory.
#

BASEDIR='media/App Store/Screenshot'
if [[ ! -d  "$BASEDIR/Original-iPhone" ]]; then
    echo "Directory $BASEDIR/Original-iPhone not found"
    exit 1
fi
if [[ ! -d  "$BASEDIR/Original-iPad" ]]; then
    echo "Directory $BASEDIR/Original-iPad not found"
    exit 1
fi

function resize {
    MODEL="$1"
    SIZE="$2"
    SOURCE="$3"
    echo "$MODEL ($SIZE)"
    if [[ ! -d  "$BASEDIR/$MODEL" ]]; then
        mkdir "$BASEDIR/$MODEL"
    fi
    for f in $(ls "$BASEDIR/$SOURCE/"); do
        echo "   $f..."
        convert -resize $SIZE! "$BASEDIR/$SOURCE/$f" "$BASEDIR/$MODEL/$f" 
    done
}

resize iPhone55 1242x2208 Original-iPhone
resize iPhone65 1242x2688 Original-iPhone
resize iPad129-2gen 2048x2732 Original-iPad
resize iPad129-3gen 2048x2732 Original-iPad
