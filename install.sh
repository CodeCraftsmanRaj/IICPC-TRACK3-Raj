#!/bin/bash

echo "================================================"
echo "VM Detection System - Installation Script"
echo "================================================"
echo ""

echo "Installing core dependencies..."
pip3 install psutil

echo ""
echo "Installing optional dependencies..."
pip3 install pynput

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Quick Start:"
echo "  python3 cli_detector.py           - Quick scan"
echo "  python3 cli_detector.py --full    - Full scan"
echo "  python3 cli_detector.py --monitor - Monitoring"
echo ""