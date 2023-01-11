#!/bin/bash
VALID_ARGS=$(getopt -o hir -l help,install,remove -- "$@")
PREVIOUS_PWD=$(pwd)
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

helpscript() {
  echo "Usage: ./install.sh [ARG]"
  echo "Installs dd-etcher to /bin. Sudo is required"
  echo ""
  echo "Arguments:"
  echo "  -h, --help           show this help message"
  echo "  -i, --install        install dd-etcher to /bin"
  echo "  -r, --remove         removes dd-etcher from /bin"
}

installscript() {
  sudo mkdir /bin/dd-etcher-bin
  cd "${SCRIPT_DIR}" || exit
  sudo cp ./main.py /bin/dd-etcher-bin/
  sudo bash -c "echo '#!/bin/bash'>/bin/dd-etcher"
  sudo bash -c "echo 'python3 /bin/dd-etcher-bin/main.py'>>/bin/dd-etcher"
  sudo chmod -R 755 /bin/dd-etcher /bin/dd-etcher-bin
  cd "${PREVIOUS_PWD}" || exit
  echo "dd-etcher is installed"
}

removescript() {
  sudo rm -r /bin/dd-etcher-bin /bin/dd-etcher
  echo "dd-etcher is removed"
}

if [[ $1 == "" ]]; then
  helpscript
fi

eval set -- "${VALID_ARGS}"
while [ : ]; do
  case "$1" in
    -h | --help)
      helpscript
      shift
      ;;
    -i | --install)
      installscript
      shift
      ;;
    -r | --remove)
      removescript
      shift
      ;;
    --) shift;
      break
      ;;
  esac
done