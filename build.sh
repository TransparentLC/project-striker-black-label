set -e

commitHash=$(git rev-parse HEAD)
commitHash="${commitHash:-????????????????????????????????????????}"
buildTime=$(date "+%Y-%m-%d %H:%M:%S")
echo $commitHash > build-info.txt
echo -n $buildTime >> build-info.txt

tar cf resources.tar assets font/LXGWWenKai-Regular.ttf scriptfiles sound

pyiSeparator="${pyiSeparator:-:}"
libExtension="${libExtension:-.so}"

pyinstaller \
    --name striker-bl \
    --icon icon.ico \
    --onedir \
    --noconsole \
    --clean \
    --log-level WARN \
    --add-data "build-info.txt${pyiSeparator}." \
    --add-data "resources.tar${pyiSeparator}." \
    --add-data "libstgnative${libExtension}${pyiSeparator}." \
    main.py