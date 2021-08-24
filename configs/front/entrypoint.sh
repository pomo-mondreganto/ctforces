#!/bin/sh -e

cd /app

yarn install
yarn serve --host 0.0.0.0
