from PIL import Image
import numpy as np
import scipy.misc as smp
import binascii
import math

class hex_to_png():
    def main(filename):
        ITER_CNT=0
        ARRAY_HEX=[]
        ARRAY_RGB=[]
        ITER_CNT2=0
        WEIGHT=0
        HIGHT=0
        with open(filename, 'rb') as f:
            hexdata = binascii.hexlify(f.read())
            counts = len(hexdata) / 6
        while ITER_CNT<counts:
            ITER_CNT+=1
            dr= 6*ITER_CNT
            ARRAY_HEX.append(hexdata[(dr-6):dr])
        if np.mod(len(hexdata),6)!=0:
            nuad=(6-len(hexdata[dr-6:])) * '0'
            nq=ARRAY_HEX[ITER_CNT-1].decode("utf-8")
            asa=nq+nuad
            ARRAY_HEX[ITER_CNT-1]=(hexdata[dr:] + bytes(asa, 'utf-8'))
        while len(ARRAY_HEX)>ITER_CNT2:
            ARRAY_RGB.append(tuple(int(ARRAY_HEX[ITER_CNT2][i:i+2], 16) for i in (0, 2 ,4)))
            ITER_CNT2 += 1
        data = np.zeros((math.ceil(math.sqrt(len(ARRAY_RGB))/1),math.ceil(math.sqrt(len(ARRAY_RGB))/1),3), dtype=np.uint8 )
        ITER_CNT2=0
        while len(ARRAY_RGB)>ITER_CNT2:
            if HIGHT==math.ceil(math.sqrt(len(ARRAY_RGB))/1):
                WEIGHT+=1
                HIGHT=0
            data[WEIGHT,HIGHT] = ARRAY_RGB[ITER_CNT2]
            ITER_CNT2+=1
            HIGHT+=1
        img = smp.toimage( data )
        #img.show()
        img.save(filename+'.png')

class png_to_hex():
    def main(filename):
        HIGHT=0
        WIDTH=0
        HEX_ARRAY=[]
        INTER_CNT=0
        ITER_CNT2=0
        im = Image.open(filename)
        pix = im.load()
        #print (im.width*im.width)
        while (im.width*im.width)>INTER_CNT:
            if WIDTH==im.width:
                HIGHT+=1
                WIDTH=0
            HEX_ARRAY.append(bytes(('%02x%02x%02x' % pix[WIDTH,HIGHT]), 'utf-8'))
            WIDTH+=1
            INTER_CNT+=1
        search = bytes('000000', 'utf-8')
        while(len(HEX_ARRAY))!=HEX_ARRAY.index(search)+1:
            x=(HEX_ARRAY.index(search))
            HEX_ARRAY.pop(x)
        HEX_ARRAY.pop(HEX_ARRAY.index(search))
        with open(('_hexed_'+filename[:-4]), 'wb') as fout:
            while len(HEX_ARRAY)>ITER_CNT2:
                fout.write(binascii.unhexlify(HEX_ARRAY[ITER_CNT2]))
                ITER_CNT2 += 1

hex_to_png.main('test.txt')
png_to_hex.main('test.txt.png')
