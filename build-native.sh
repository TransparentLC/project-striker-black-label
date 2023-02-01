set -e

CC="${CXX:-gcc}"
CXX="${CXX:-g++}"
libExtension="${libExtension:-.so}"

$CXX \
    -std=c++17 \
    -Wall \
    -Ofast \
    -flto \
    -fPIC \
    -fvisibility=hidden \
    -s \
    -shared \
    ${useStatic:+-static} \
    -o libstgnative${libExtension} \
    native/xbrz/xbrz.h \
    native/xbrz/xbrz.cpp
