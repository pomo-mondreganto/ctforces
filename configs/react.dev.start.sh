#!/bin/sh

echo "[+] Cleaning /react_build"
rm -rf /react_build/*

echo "[+] Running webpack docker-dev"
webpack --config config/webpack.docker-dev.js

echo "[+] Copying dist/* files to /react_build"
cp dist/* /react_build

echo "[+] Done, exiting"
