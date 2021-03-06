#!/usr/bin/env bash
# coding: utf-8
#
# Interactive IQCHECK installer script. Run this script to download
# and install iqcheck, a TST CUSTOM COMMAND tool. Be sure that TST is
# already installed in your environment.
# This script can be invoked with these options:
#
# --pre-release
#       Download the latest pre-release version available.
#
# --installation-dir <dir>
#       Install the new version into <dir>.

# constants
INSTALL_DIR=~/.tst/iqcheck.install
TST_DIR=~/.tst
CONFIG_FILE=~/.tst/config.json
UPDATE="false"
BASHRC=~/.bashrc

# colors
RESET="\033[0m"
BLACK="\033[0;30m"
BLUE="\033[0;34m"
BROWN="\033[0;33m"
CYAN="\033[0;36m"
DGRAY="\033[1;30m"
GREEN="\033[0;32m"
LBLUE="\033[1;34m"
LCYAN="\033[1;36m"
LGRAY="\033[0;37m"
LGREEN="\033[1;32m"
LPURPLE="\033[1;35m"
LRED="\033[1;31m"
PURPLE="\033[0;35m"
RED="\033[0;31m"
WHITE="\033[1;37m"
YELLOW="\033[1;33m"

# semantic colors
NORMAL=$LGRAY
WARNING=$LRED
IMPORTANT=$LBLUE
QUESTION=$LGREEN

# read either 'y' or 'n' from keyboard
function get_yes_or_no {
    while true; do 
        read -s -n 1 answer
        [[ "$answer" == "y" ]] && break
        [[ "$answer" == "n" ]] && break
    done
    echo $answer
}

# print with color
function print {
    COLOR=$2
    if [ "$COLOR" == "" ]; then
        COLOR=$NORMAL
    fi
    echo -n -e $COLOR"$1"$RESET
}


# MAIN

print "Installing iqcheck scripts\n" $WARNING

# process options
while (( $# > 0 )); do
    case "$1" in
        --pre-release)
            DOWNLOAD_DEV_VERSION="true"
            ;;
        --installation-dir)
            INSTALLATION_DIR="true"
            TST_DIR=$2
            shift
            ;;
        --root)
            #INSTALL_DIR=~aluno/.tst/qcheck.install
            #TST_DIR=~aluno/.tst
            #CONFIG_FILE=~aluno/.tst/config.json
            root="true"
            ;;
        --*)
            print "invalid option $1\n" $WARNING
            exit 1
            ;;
    esac
    shift
done

# shoud run as root?
if [[ "$EUID" == "0" ]] && [[ "$root" != "true" ]]; then
   print "This script cannot be run as root\n" $WARNING
   exit 1
fi

# require tst or abort
if [ ! -d "$TST_DIR" ]; then
  print "Iqcheck requires tst\n" $WARNING
  print "Aborting installation\n"
  exit 1
fi

# require curl or abort
CURL=$(command -v curl)
if [ $? != 0 ]; then
    print "The installation script requires the curl command\n" $WARNING
    print "Aborting installation\n"
    exit 1
fi

# require nltk or abort
NLTK=$(python -c "import nltk;" 2> /dev/null)
if [ $? != 0 ]; then
    print "\nIqcheck requires nltk\n" $WARNING
    print "Get nltk and install it as superuser. Check: https://pypi.python.org/pypi/nltk.\n" $NORMAL
    print "* Tip: sudo pip install nltk\n" $IMPORTANT
    print "\nDon't have pip either?\n" $NORMAL
    print "* Tip: sudo apt-get install python-pip\n" $IMPORTANT
    print "\nAborting installation\n" $NORMAL
    exit 1
fi

# require unzip or abort
UNZIP=$(command -v unzip)
if [ $? != 0 ]; then
    print "The installation script requires the unzip command\n" $WARNING
    print "Aborting installation\n";
    exit 1
fi

# identify releases url
if [ "$DOWNLOAD_DEV_VERSION" == "true" ]; then
    RELEASES_URL='https://api.github.com/repos/marcosasn/tst-iqcheck/releases'
    print "* fetching development pre-release information\n"
else
    RELEASES_URL='https://api.github.com/repos/marcosasn/tst-iqcheck/releases/latest'
    print "* fetching latest release information\n"
fi

# download releases info: identify tag_name and zipball_url
RELEASES=$(curl -q $RELEASES_URL 2> /dev/null)
if [ $? != 0 ]; then
    print "Couldn't download release information\n" $WARNING
    print "Installation aborted\n"
    exit 1
fi
TAG_NAME=$(echo -e "$RELEASES" | grep "tag_name" | cut -f 4 -d '"' | head -1)
ZIPBALL_URL=$(echo -e "$RELEASES" | grep "zipball_url" | cut -f 4 -d '"' | head -1)


# cancel installation if there's no release available
if [ "$TAG_NAME" == "" ]; then
    print "No release available\n" $WARNING
    print "Installation canceled\n" $IMPORTANT
    exit 1
fi

# create new installation dir
if [ -d "$INSTALL_DIR" ]; then
    if [ "$UPDATE" == "false" ]; then
        print "* deleting failed attempt to install\n" $WARNING 
    fi
    rm -rf $INSTALL_DIR
fi
mkdir -p $INSTALL_DIR

# download latest release into INSTALL_DIR
cd $INSTALL_DIR

curl -q -Lko iqcheck.zip $ZIPBALL_URL 2> /dev/null
if [ $? != 0 ]; then
    rm -rf $INSTALL_DIR
    echo $ZIPBALL_URL
    print "Couldn't download release zip\n" $WARNING
    print "Installation aborted\n"
    print "Temporary files deleted\n"
    exit 1
fi

# unzip and install tst scripts within INSTALL_DIR
print "* unzipping and installing iqcheck scripts\n"
unzip -q iqcheck.zip
rm iqcheck.zip

# move files to TST_DIR
mv marcosasn-tst-iqcheck*/bin/* $TST_DIR/bin/
mv marcosasn-tst-iqcheck*/commands/* $TST_DIR/commands/
chmod +x $TST_DIR/commands/tst-iqcheck

# download third party dependencies
print "* installing nltk data\n"
## nltk
python -m nltk.downloader all 2> /dev/null
if [ $? != 0 ]; then
    print "Couldn't download dependency\n" $WARNING
    print "Installation aborted\n"
    exit 1
fi

# Move files to iqcheck dir
mkdir -p $TST_DIR/iqcheck
mv marcosasn-tst-iqcheck*/LICENSE $TST_DIR/iqcheck/
mv marcosasn-tst-iqcheck*/README.md $TST_DIR/iqcheck/
mv marcosasn-tst-iqcheck*/etc/* $TST_DIR/iqcheck/

# configure environment
python $TST_DIR/iqcheck/set_config.py
print "Finished environment configuration\n" $IMPORTANT

# Report activity
if [[ "$root" != "true" ]]; then
    print "\nReport activities for research purpose? (y/n) " $QUESTION
    get_yes_or_no
    if [[ "$answer" == "n" ]]; then
        # Dont report activities
        mv $TST_DIR/bin/iqchecklibs.py $TST_DIR/bin/iqchecklib.py
    else
        # Report activities
        rm $TST_DIR/bin/iqchecklibs.py
    fi
else
    # Report activities
    rm $TST_DIR/bin/iqchecklibs.py
fi

# end installation
cd $TST_DIR
rm -rf $INSTALL_DIR
print "Installation finished\n" $IMPORTANT