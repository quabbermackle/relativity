#!/bin/bash

cd ~
termux-change-repo

# Install the x11-repo and update all packages
pkg i -y root-repo x11-repo tur-repo
pkg update
pkg upgrade

# Grant storage access - (cannot be ran prior to installing x11-repo)
termux-setup-storage

# install basic environment packages
pkg i -y build-essential git tmux termux-services wget which
pkg i -y gcc-default

# qucs-s dependencies (SPICE simulation)
pkg i -y ngspice qt6-qtbase qt6-qttools glu glfw
pkg i -y vulkan-tools vulkan-utility-libraries vulkan-headers
pkg i -y qt6-qtbase-gtk-platformtheme qt6-qtsvg

# code editor and python
pkg i -y code-oss code-is-code-oss
pkg i -y python3.11 python3.11-cross python3.11-static
pkg i -y python-is-python3.11

# Install hardware acceleration, xfce4 gui, sound, and browser
pkg i -y dbus pulseaudio virglrenderer-android
pkg i -y pavucontrol-qt librewolf xfce4

# Enable Sound
echo "
pulseaudio --start --exit-idle-time=-1
pacmd load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1
" > $HOME/.sound

echo "
source .sound" >> .bashrc

# Setup termux to allow x11 app
pkg i -y termux-x11
sleep 3
echo "allow-external-apps = true" >> ~/.termux/termux.properties 

# Enable PulseAudio over Network
pulseaudio --start --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" --exit-idle-time=-1

# Prepare termux-x11 session
export XDG_RUNTIME_DIR=${TMPDIR}

# Set Display to :2 since Ubuntu runs on :0 and Debian runs on :1
termux-x11 :2 >/dev/null &

# Wait a bit until termux-x11 gets started.
sleep 3

# Set an alias to load termux environment faster
echo 'alias termux="am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity >/dev/null 2>&1 && sleep 1 && termux-x11 :3 -xstartup '\''dbus-launch --exit-with-session xfce4-session'\'' && startxfce4"' >> $HOME/.bashrc
source ~/.bashrc

# Login to Environment
am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity > /dev/null 2>&1 && sleep 1 && termux-x11 :3 -xstartup "dbus-launch --exit-with-session xfce4-session" && startxfce4

exit 0
