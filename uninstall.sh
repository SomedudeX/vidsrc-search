#!/bin/sh

if [ ! -f ~/.config/pymovie ]; then
	echo " [Error] PyMovie configuration not found"
	echo " > Could not find ~/.config/pymovie"
	echo " > PyMovie is not installed"
	echo " > "
	echo " > Script terminating..."
	exit 1
fi

read -r -p " [Log] This script will uninstall the entirety of PyMovie and its config. Continue? [Y/n]?" CONT
if [ "$CONT" = "Y" ]; then
	sudo rm -rf ~/.config/pymovie
	echo " [Log] PyMovie succesfully uninstalled"
	echo " [Log] Removed ~/.config/pymovie"
	exit 0
else
	echo " [Log] Terminated per user request"
	exit 0
fi
