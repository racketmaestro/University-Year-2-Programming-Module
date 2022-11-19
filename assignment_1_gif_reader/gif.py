def load_file(file_name):
    '''Reads the bytes content of a gif file or return an error if file is not found '''
    file_name = str(file_name)

    try:
        f = open(file_name,'rb')
        data = f.read()
        info = str(file_name)
    except:
        data = bytearray()
        info = 'file not found'
        print(info)

    return data, info

def extract_header(data):
    '''This function will return the GIF specification'''
    header = data[:6].decode('utf-8')
    
    return header

def extract_screen_descriptor(data):
    '''Returns the information about the Logical Screen Descriptor from the GIF data'''

    # Extract information by indexing
    bcolour_i = data[11]
    pxa_ratio = data[12]
    width = int.from_bytes([data[6],data[7]], 'little')
    height = int.from_bytes([data[8],data[9]], 'little')

    # Extract information form the packed field binary code using indexing
    packed_field_binary = format(int(data[10]),'b')
    gc_fl = packed_field_binary[0]
    cr = int(packed_field_binary[1:4],2)
    sort_fl = packed_field_binary[4]
    gc_size = int(packed_field_binary[5:],2)

    # Check pixel aspect ratio
    if pxa_ratio != 0:
        pxa_ratio = (pxa_ratio + 15)/64

    return width, height, gc_fl, cr, sort_fl, gc_size, bcolour_i, pxa_ratio

def extract_global_colour_table(data):
    '''Returns a global colour table of type list. The nested lists within correspond to the R,G,B
        values of each colour. The length of this table can be determined from the global colour table 
        binary code in the Logical Screen Descriptor '''

    # Get size of global colour table by calling previous function
    gc_size = extract_screen_descriptor(data)[5]
    
    # Get number of colours in the colour map. Multiply by 3 bytes to get length of bytes in data.
    n_colours = 2 ** (gc_size + 1)
    gc_table_length = 3 * n_colours  

    # Create a list containing the bytes of the global colour table
    gc_table_bytes = []
    for i in range(13,13 + gc_table_length):
        gc_table_bytes.append(data[i])
    
    # From the list of bytes, create 2D array
    gc_table = [gc_table_bytes[i:i+3] for i in range(0, gc_table_length, 3)]
    
    return gc_table

def extract_image_descriptor(data):
    '''Returns the coordinates of the image left and top position, the dimensions of the image,
    and information about the local colour table if it exists'''
    
    # Get number of bytes occupied by global colour table
    gc_table = extract_global_colour_table(data)
    gc_table_length = len(gc_table) * 3
    
    # Image descriptor comes after the global colour table
    img_descriptor_index = 13 + gc_table_length 

    # Create list of 10 bytes of image descriptor
    img_descriptor = [data[i] for i in range(img_descriptor_index,img_descriptor_index+10)]

    # Extract information from image descriptor
    left = int.from_bytes([img_descriptor[1],img_descriptor[2]],'little')
    top = int.from_bytes([img_descriptor[3],img_descriptor[4]],'little')
    width = int.from_bytes([img_descriptor[5],img_descriptor[6]],'little')
    height = int.from_bytes([img_descriptor[7],img_descriptor[8]],'little')
    packed_field_binary = format(int(img_descriptor[9]),'08b')

    # Extract Information from packed field binary
    lc_fl = packed_field_binary[0]
    itl_fl = packed_field_binary[1]
    sort_fl = packed_field_binary[2]
    res = int(packed_field_binary[3:5],2)
    lc_size = int(packed_field_binary[5:],2)

    return left, top, width, height, lc_fl, itl_fl, sort_fl, res, lc_size

def extract_image(data):
    '''Decompresses a GIF by decoding the byte stream of the gif file using LZW Algorithm.
    
    Args: 
        data: the bytes data of the gif file
    
    Returns:
        img: a 3D array containing the decompressed data. First dimension corresponds to rows, second dimension
            corresponds to columns and third dimension corresponds to the R,G and B values of each pixel '''

    # Get number of bytes occupied by global colour 
    gc_table = extract_global_colour_table(data)
    gc_table_length = len(gc_table) * 3
    
    # Get LZW Minimum code
    img_descriptor_index = 13 + gc_table_length 
    LZW_min_index = img_descriptor_index + 10
    LZW_min_code = data[LZW_min_index]
   
    # Initialize the decompression size for decoding
    decompression_size = LZW_min_code + 1
    
    # Get the initial colour number of colour codes.
    n_colour_codes = (1<<LZW_min_code) -1

    # Initialize a code table dictionary, where keys represent code number, and value represents the colour code.
    colour_table = dict()
    for i in range(n_colour_codes+1):
        colour_table[i] = i
        
    colour_table[n_colour_codes + 1 ] = 'CC' # Clear Code 
    colour_table[n_colour_codes + 2] = 'EOI' # End of Information

    # Get number of bytes of data sub block, which comes after LZW Minimum Code size
    n_bytes = data[LZW_min_index + 1]

    # Get data sub-blocks, where sub blocks is a list of decimals of the corresponding bytes
    sub_blocks =  []
    for j in range(LZW_min_index + 1, LZW_min_index + 1 + n_bytes + 1):
        sub_blocks.append(data[j])
    
    # Convert sub blocks elements into 8 bit binary. Remove NN byte label
    sub_blocks_binary = [bin(list_item)[2:] for list_item in sub_blocks ]
    sub_blocks_binary = [j.zfill(8) for j in sub_blocks_binary][1:]
    
    # Due to Little Endian reading format, reverse the list before concatenating together
    sub_blocks_binary.reverse()
    code_stream = ''.join(sub_blocks_binary)

    # Initialize the index of the bits being read
    idx = decompression_size * -1

    # Read the first set of bits and add to output stream
    output = []
    binary_code = code_stream[idx:]
    code = int(binary_code,2)
    output.append(code)
    
    # Initialize the last entry key in the dictionary and the end code
    last_entry = len(colour_table) - 1 
    end_code = last_entry

    # Start reading the code_stream.
    # Break out of loop when the end code is read.
    decoded_value = 0
    while decoded_value != end_code:
            
        idx = idx - decompression_size
        binary_code = code_stream[idx: idx + decompression_size]
        decoded_value = int(binary_code,2)
        output.append(decoded_value)
        last_entry += 1
        
        # Increase decompression size by 1 bit when next (hypothetical) table entry
        # exceed maximum possible value read by current decompression size
        if last_entry == (2 ** (decompression_size)):
            decompression_size += 1
        
        # Reset last entry and decompression size to 3 bits if it exceeds 12 bits
        if decompression_size == 13:
            decompression_size = 3
            last_entry = end_code
        
    # Intialize decoded first value into index stream
    index_stream = []
    k = 1
    index_stream.append(colour_table[output[k]])

    # Initialize next dictionary entry, which would be after the EOI entry 
    next_table_key = len(colour_table) 

    # Start decoding the output stream
    for k in range(2, len(output)-1):
        code = output[k]
        prev_code = output[k-1]
        
        if code in colour_table:
            prev_sequence = colour_table[prev_code]
            current_sequence = colour_table[code]
            
            if type(current_sequence) == list:
                k_value = current_sequence[0]
            else:
                k_value = current_sequence
            
            # Create new index sequence
            new_index_sequence=[]
            if type(prev_sequence) == list:
                for i in prev_sequence:
                    new_index_sequence.append(i)
                new_index_sequence.append(k_value)
            else:
                new_index_sequence = [prev_sequence,k_value]

            # Output the index sequence of the current code index to stream 
            index_stream.append(current_sequence)

        else:
            prev_sequence = colour_table[prev_code]

            # Create new index sequence
            if type(prev_sequence) == list:
                k_value = prev_sequence[0]
                new_index_sequence = []
                for j in prev_sequence:
                    new_index_sequence.append(j)
                new_index_sequence.append(k_value)

            else:
                k_value = prev_sequence
                new_index_sequence = [prev_sequence,k_value]
            
            # Add the new index sequence to the stream
            index_stream.append(new_index_sequence)

        # Update colour table dictionary
        new_table_entry = {next_table_key: new_index_sequence}
        colour_table.update(new_table_entry) 
        next_table_key += 1

    # Flatten the nested lists in index stream to get one continous list
    final_index_stream = []
    def recursion(x):
        for n in x:
            if type(n) == list:
                recursion(n)
            else:
                final_index_stream.append(n)
    recursion(index_stream)

    # Create a global colour table
    gc_table = extract_global_colour_table(data)
    
    # Index stream values correspond to colour code on global colour table. 
    # Iterate accordingly to get RGB values at each pixel coordinate
    for i in range(len(final_index_stream)):
        final_index_stream[i] = gc_table[final_index_stream[i]]

    # Get image width and height 
    width, height = extract_image_descriptor(data)[2:4]

    # Convert 2D final index stream into 3D
    img = []
    img = [final_index_stream[i:i+width] for i in range(0, height*width, width)]

    return img

