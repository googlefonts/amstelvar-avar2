#!/bin/sh

# cd amstelvar-avar2
# python3.11 -m pip install --user virtualenv
# python3.11 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# deactivate
# sh build.sh

source venv/bin/activate

echo "Building variable fonts..."

echo "  Building AmstelvarA2 Roman..."
fontmake -m Sources/Roman/AmstelvarA2-Roman.designspace -o variable --output-path Fonts/AmstelvarA2-Roman_avar2.ttf  --feature-writer None --no-generate-GDEF --keep-direction --verbose INFO

# echo "  Building AmstelvarA2 Italic..."
# fontmake -m Sources/Italic/AmstelvarA2-Italic.designspace -o variable --output-path Fonts/AmstelvarA2-Italic_avar2.ttf --feature-writer None --no-generate-GDEF --keep-direction --verbose WARNING

echo "done!"

deactivate