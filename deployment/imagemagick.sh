#!/usr/bin/env bash
mkdir bin
wget -nc --no-check-certificate -O bin/magick https://imagemagick.org/download/binaries/magick
chmod +x bin/magick
export PATH="$PWD/bin:$PATH"
magick -version
