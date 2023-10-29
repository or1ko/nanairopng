class Png:
    def __init__(self, png_file):
        self.png_file = png_file

    def readDimensions(self):
        with open(self.png_file, 'rb') as file:
            # skip magic_number + ihdr
            file.read(16)
            width = int.from_bytes(file.read(4), 'big')
            height = int.from_bytes(file.read(4), 'big')
            return (width,height)

    def color_palette(self, data, color_map):
        inner_color_map = bytearray(7)
        for i in range(0, 7):
            r = data[i*3]
            g = data[i*3+1]
            b = data[i*3+2]

            if (r == 0 and g == 0 and b == 0):
                # Black
                color = color_map[0]
            elif (r == 255 and g == 255 and b == 255):
                # White
                color = color_map[1]
            elif (r == 255 and g == 0 and b == 0):
                # Red
                color = color_map[4]
            elif (r == 0 and g == 255 and b == 0):
                # Green
                color = color_map[2]
            elif (r == 0 and g == 0 and b == 255):
                # Blue
                color = color_map[3]
            elif (r == 255 and g == 255 and b == 0):
                # Yello
                color = color_map[5]
            elif (r == 255 and g == 165 and b == 0):
                # Orange
                color = color_map[6]

            inner_color_map[i] = color
        return inner_color_map

    def convertAndWrite(self, output, color_map):
        with open(self.png_file, 'rb') as file:
            # skip magic_number + ihdr
            file.read(16)

            width = int.from_bytes(file.read(4), 'big')
            height = int.from_bytes(file.read(4), 'big')

            color_depth = int.from_bytes(file.read(1), 'big')
            color_type = int.from_bytes(file.read(1), 'big')

            compress_type = int.from_bytes(file.read(1), 'big')
            filter_type = int.from_bytes(file.read(1), 'big')
            interrace_type = int.from_bytes(file.read(1), 'big')

            # skip crc
            file.read(4)

            #print("width", width, "height", height, 
            #    "color type", color_type,
            #    "color depth", color_depth, 
            #    "compress type", compress_type, 
            #    "filter type", filter_type,
            #    "interrace type", interrace_type)

            idat_data = bytes()

            while(True):
                chunk_length = file.read(4)
                if not chunk_length :
                    break 
                chunk_length = int.from_bytes(chunk_length, 'big')
                chunk_name = file.read(4).decode()

                if (chunk_name == "PLTE"):
                    chunk_data = file.read(chunk_length)
                    palette = self.color_palette(chunk_data, color_map)
                    # skip crc
                    file.read(4)
                elif (chunk_name == "IDAT"):
                    # print("IDAT length:", chunk_length)
                    idat_data = idat_data + file.read(chunk_length)
                    #skip crc
                    file.read(4)
                else :
                    #skip chunk data and crc
                    file.read(chunk_length)
                    file.read(4)

            import deflate
            import io
            with deflate.DeflateIO(io.BytesIO(idat_data), deflate.ZLIB) as d:
                rowBitSize = width * color_depth + 8
                rowByteSize = int(rowBitSize / 8)

                #print("rowByteSize", rowByteSize)

                y = 0
                while(True):
                    row = d.read(rowByteSize)
                    if not row:
                        break
                    #if (y % 100 == 0):
                    #    print(y)
                    y = y + 1
                    for w in range(1, rowByteSize):
                        u = row[w] & 0b11110000 >> 4
                        l = row[w] & 0b00001111
                        output.write(bytes([palette[u]]))
                        output.write(bytes([palette[l]]))
