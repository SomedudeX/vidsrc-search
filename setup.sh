#!/bin/bash

exec 3>&1
msg () {
    echo "$@" >&3
}

cd "$(dirname "$0")" || return

if [ ! -f App/entrypoint.py ]; then
    msg " [Error] PyMovie not found"
    msg " > Could not find entrypoint.py"
    msg " > Is the repository still intact?"
    msg " > "
    msg " > Script terminating..."
    exit 1
fi

msg " [Log] Running PyInstaller (this might take a while)..."
if pyinstaller App/entrypoint.py --onefile --name PyMovie &> setup.log ; then
    msg " [Log] Succesfully ran PyInstaller"
else
    msg " [Log] PyInstaller failed"
    msg " [Log] Check setup.log (generated by pyinstaller) for more information"
    exit 1
fi

msg " [Log] Cleaning up"
rm PyMovie.spec
msg " [Log] Wrote to dist/PyMovie"
exit 0