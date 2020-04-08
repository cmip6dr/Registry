
##
## convert pdf to png via svg
## used for latex output when pdf2ppm and "convert <>.pdf <>.png" fail
##
## the converstion to svg appears to be robust.

pdftocairo -svg $1.pdf $1.svg
convert $1.svg $1.png

