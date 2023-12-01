exec 3>&1
msg () {
    echo " [Log] $@" >&3
}

if [ ! -f App/entrypoint.py ]; then
    echo " [Error] PyMovie not found"
    echo " > Could not find entrypoint.py"
    echo " > Perhaps you are in the wrong directory?"
    echo " > "
    echo " > Script terminating..."
    exit 1
fi

msg "Running PyInstaller (this might take a while)..."
if pyinstaller App/entrypoint.py --onefile --name PyMovie &> setup.log ; then
    msg "Succesfully ran PyInstaller"
else
    msg "PyInstaller failed"
    msg "Check setup.log (generated by pyinstaller) for more information"
fi

msg "Cleaning up"
rm PyMovie.spec
msg "Wrote to dist/PyMovie"
exit 0