import argparse
import os
import struct
from PIL import Image

class Header:
    MAX_FORMAT_LENGTH=8
    size = 0
    fformat = "txt"


def encode_in_pixel(byte, pixel):
    """Encodes a byte in the two least significant bits of each channel.

    A 4-channel pixel is needed, which should be a tuple of 4 values from 0 to 255.
    """
    r = (byte&3)
    g = (byte&12)>>2
    b = (byte&48)>>4
    a = (byte&192)>>6

    color = (r+(pixel[0]&252), g+(pixel[1]&252), b+(pixel[2]&252), a+(pixel[3]&252))
    return color

def decode_from_pixel(pixel):
    """Retrieves an encoded byte from the pixel.

    The pixel should be a tuple of 4 values from 0 to 255.
    """
    r = pixel[0]&3
    g = pixel[1]&3
    b = pixel[2]&3
    a = pixel[3]&3

    result = r + (g<<2) + (b<<4) + (a<<6)
    return struct.pack("B", result)


def encode(image, fil):
    im = Image.open(image)
    px = im.load()

    with open(fil, 'rb') as inf:
        #Load the file
        filebytes = inf.read()

        #Ensure the image is large enough to hide the data
        if len(filebytes) > im.width*im.height:
            print "Image to small to encode the file. You can store 1 byte per pixel."
            exit()

        #Create a header
        header = Header()
        header.size = len(filebytes)
        header.fformat = fil.split(os.extsep)[1] if (len(fil.split(os.extsep))>0) else ""

        #Add the header to the file data
        headerdata = struct.pack("I"+str(Header.MAX_FORMAT_LENGTH)+"s", header.size, header.fformat)
        filebytes = headerdata + filebytes

        for i in range(len(filebytes)):
            coords = (i%im.width, i/im.width)

            byte = ord(filebytes[i])

            px[coords[0], coords[1]] = encode_in_pixel(byte, px[coords[0], coords[1]])

    im.save("output.png", "PNG")

def decode(image):
    im = Image.open(image)
    px = im.load()

    data = ""

    #Create the header for reading
    header = Header()

    index = 0
    headerdata = ""
    headercomplete = False
    for i in range(im.height):
        for j in range(im.width):

            if index < 4 + Header.MAX_FORMAT_LENGTH:
                headerdata += decode_from_pixel(px[j, i])
            elif index == 4 + Header.MAX_FORMAT_LENGTH:
                #decode header after reading is complete
                headerdata = struct.unpack("I"+str(Header.MAX_FORMAT_LENGTH)+"s", headerdata)
                header.size = headerdata[0]
                header.fformat = headerdata[1].strip("\x00")
                headercomplete = True
                data += decode_from_pixel(px[j, i])
            else:
                data += decode_from_pixel(px[j, i])

            #End reading if the entire file was read (according to the size from the header)
            if headercomplete and len(data) == header.size-1:
                break

            index+=1

        if headercomplete and len(data) == header.size-1:
                break


    print "Saving decoded output as {}".format("output"+os.extsep+header.fformat)
    with open("output"+os.extsep+header.fformat, 'wb') as outf:
        outf.write(data)


def main():
    parser = argparse.ArgumentParser(description="Process images")
    parser.add_argument("image", help="The name of the file to be encoded if encoding is chosen")
    parser.add_argument("--file")
    parser.add_argument("action")
    args = parser.parse_args()

    if args.action=="encode":
        if not args.file:
            print "You need to specify a file to encode."
            exit()
        encode(args.image, args.file)
    elif args.action=="decode":
        decode(args.image)
    else:
        print "Incorrect action selected (choose encode or decode)"

if __name__ == '__main__':
    main()
