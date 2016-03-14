# hide.py
A steganographic program that encodes files in pictures.

You will need Pillow library. To install just do `pip install Pillow` in the terminal.

Usage:

`hide.py [-h] [--file FILE] image action`

"Image" specifies the image you want to decode or encode. Currently only png files are supported.
"Action" must be either encode or decode.
"File" is only required when encoding. It specifies the file you want to hide in the image.

The program separates the file (any file will work) into bytes, which are then separated into 2-bit sequences. Those two bit sequences forming a byte are then used to modify the colors of the pixels of the image. Since every pixel has four channels (RGBA), and each channel uses 8 bits for its value (giving a range of 0-255), the channels are only modified by at most 3 (`11` bit sequence). In other words, no one will be able to tell the image contains any hidden data without this tool or a tool that reverse-engineers this functionality.

The program adds a small header to the beginning of the stream before encoding, which consists of 4 bytes (signed int) to encode the size in bytes and a sequence of 8 characters storing the original file extension. You can hide any file, including exe and zip. In fact it is advisable to compress your files before hiding to reduce their size, bundle many files into one package or encrypt them before hiding. If you use encryption the decoded file will be indistinguishable from random noise.

The side effect of the program is that it can also decode files out of any image, even ones that don't have any hidden data, but the result will be meaningless.

If you use "encode" the program will save a new image called `output.png` which will be the image with encoded data.
If you use "decode", the program will save the decoded data to a file called `output.xxx` where xxx is the file extension read from the header.

Here's an example of a text file hidden in the image:

![hidden data](http://i.imgur.com/eZCmJEe.png)

Be sure to use pngs with alpha channel, otherwise it won't work.
