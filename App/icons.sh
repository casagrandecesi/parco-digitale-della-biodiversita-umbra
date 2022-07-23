#!/usr/bin/env bash
#
# Creates the iOS and Android icons by resizing the resources/icon.png file
# whose dimension must be 1024x1024 pixels.
#

BASEDIR='resources'
BASEICON="$BASEDIR/icon.png"
IOS_ICONDIR="$BASEDIR/ios/icon"
ANDROID_ICONDIR="$BASEDIR/android/icon"
if [[ ! -f  "$BASEICON" ]]; then
    echo "Image $BASEICON not found"
    exit 1
fi
if [[ ! -d  "$IOS_ICONDIR" ]]; then
    mkdir -p "$IOS_ICONDIR"
fi
if [[ ! -d "$ANDROID_ICONDIR" ]]; then
    mkdir -p "$ANDROID_ICONDIR"
fi

XML=''

function resize {
    TARGET="$1"
    WIDTH="$2"
    HEIGHT="$3"
    echo "$TARGET..."
    convert -resize "${WIDTH}x${HEIGHT}" "$BASEICON" "$TARGET" 
    XML="$XML<icon src=\"$TARGET\" width=\"$WIDTH\" height=\"$HEIGHT\" />\n"
}

XML="$XML\n\n------ Android --------\n\n"
resize resources/ios/icon/drawable-mdpi-icon.png 48 48
resize resources/ios/icon/drawable-hdpi-icon.png 72 72
resize resources/ios/icon/drawable-xxxhdpi-icon.png 192 192
resize resources/ios/icon/drawable-playstore-512-icon.png 512 512
resize resources/ios/icon/drawable-xhdpi-icon.png 96 96
resize resources/ios/icon/drawable-xxhdpi-icon.png 144 144
resize resources/ios/icon/drawable-ldpi-icon.png 36 36

XML="$XML\n\n------ iOS --------\n\n"
resize resources/ios/icon/icon-20.png 20 20
resize resources/ios/icon/icon-24.png 24 24
resize resources/ios/icon/icon-27.5@2x.png 27 27
resize resources/ios/icon/icon-small.png 29 29
resize resources/ios/icon/icon-29.png 29 29
resize resources/ios/icon/icon-40.png 40 40
resize resources/ios/icon/icon-44.png 44 44
resize resources/ios/icon/icon-48.png 48 48
resize resources/ios/icon/icon-50.png 50 50
resize resources/ios/icon/icon-55.png 55 55
resize resources/ios/icon/icon.png 57 57
resize resources/ios/icon/icon-small@2x.png 58 58
resize resources/ios/icon/icon-60.png 60 60
resize resources/ios/icon/icon-66.png 66 66
resize resources/ios/icon/icon-72.png 72 72
resize resources/ios/icon/icon-76.png 76 76
resize resources/ios/icon/icon-40@2x.png 80 80
resize resources/ios/icon/icon-86.png 86 86
resize resources/ios/icon/icon-small@3x.png 87 87
resize resources/ios/icon/icon-88.png 88 88
resize resources/ios/icon/icon-92.png 92 92
resize resources/ios/icon/icon-50@2x.png 100 100
resize resources/ios/icon/icon-102.png 102 102
resize resources/ios/icon/icon@2x.png 114 114
resize resources/ios/icon/icon-40@3x.png 120 120
resize resources/ios/icon/icon-60@2x.png 120 120
resize resources/ios/icon/icon-72@2x.png 144 144
resize resources/ios/icon/icon-76@2x.png 152 152
resize resources/ios/icon/icon-83.5@2x.png 167 167
resize resources/ios/icon/icon-172.png 172 172
resize resources/ios/icon/icon-60@3x.png 180 180
resize resources/ios/icon/icon-196.png 196 196
resize resources/ios/icon/icon-216.png 216 216
resize resources/ios/icon/icon-234.png 234 234

echo -e "$XML"
echo '<icon src="resources/icon.png" width="1024" height="1024" />'
