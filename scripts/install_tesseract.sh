#!/bin/bash
# Tesseract Setup Script for Linux/Mac

echo "Installing Tesseract OCR..."
if [ "$(uname)" == "Darwin" ]; then
    # Mac OS X platform        
    brew install tesseract
    brew install tesseract-lang
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # GNU/Linux platform
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr
    sudo apt-get install -y tesseract-ocr-hin
fi

echo "Tesseract installation complete!"
