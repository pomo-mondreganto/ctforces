#!/bin/sh

echo "[+] Cleaning /react_build"
rm -rf /react_build/*

echo "[+] Running npm run build"
npm run build

echo "[+] Copying dist/* files to /react_build"
cp dist/* /react_build

echo "[+] Done, exiting"
