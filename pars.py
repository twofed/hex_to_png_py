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
        LENS=str(len(ARRAY_HEX))
        if len(LENS)<7:
            LENS = hex(int(LENS))
            LENS=LENS[2:len(LENS)]
            zero=6-len(LENS)
            LENS='0'*zero + LENS
            ARRAY_HEX.insert(0, bytes(LENS, 'utf-8'))
        else:
            LENS=hex(int(LENS))
            ARRAY_HEX.insert(0,bytes(LENS[2:8],'utf-8'))
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
        outsum = ''
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
        chsum=(HEX_ARRAY[0]).decode("utf-8")
        chsum=str(int(chsum.upper(),16))
        INTER_CNT=0
        while len(chsum)>INTER_CNT:
            outsum=outsum+chsum[INTER_CNT]
            INTER_CNT += 1
        HEX_ARRAY.pop(0)
        while len(HEX_ARRAY)!=int(outsum):
            x=len(HEX_ARRAY)-1
            HEX_ARRAY.pop(x)
        #HEX_ARRAY.pop(HEX_ARRAY.index(search))
        with open((filename[:-8]+'_hexed'+filename[-8:-4]), 'wb') as fout:
            while len(HEX_ARRAY)>ITER_CNT2:
                if (len(HEX_ARRAY)-ITER_CNT2)==1:
                    INTER_CNT=2 # def 0 
                    while str(HEX_ARRAY[ITER_CNT2].decode("utf-8")).rfind('00',0,len((HEX_ARRAY[ITER_CNT2]).decode("utf-8")))!=-1:
                        if str(HEX_ARRAY[ITER_CNT2].decode("utf-8"))=='000000':
                            break
                        HEX_ARRAY[ITER_CNT2] = HEX_ARRAY[ITER_CNT2][0:6 - INTER_CNT]
                        INTER_CNT+=2
                fout.write(binascii.unhexlify(HEX_ARRAY[ITER_CNT2]))
                ITER_CNT2 += 1

hex_to_png.main('tau.tgz')
png_to_hex.main('tau.tgz.png')
