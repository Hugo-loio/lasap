#!/bin/sh

pkg=$(dirname "$0")

pip uninstall --break-system-packages dapp
