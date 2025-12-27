import numpy as np
from PIL import Image
import os

def embed_multiple_files(cover_path, secret_paths, output_path):
    # Load image and convert to numpy array (Fast Matrix)
    img = Image.open(cover_path).convert("RGB")
    arr = np.array(img)
    
    # Flatten the array to a long line of numbers (R, G, B, R, G, B...)
    flat_arr = arr.flatten()
    
    # Prepare all secret data as bytes first
    payload_bytes = bytearray()
    for secret_path in secret_paths:
        # Read file
        with open(secret_path, 'rb') as f:
            secret_data = f.read()
        
        # Prepare Extension (8 bytes, padded with #)
        ext = os.path.splitext(secret_path)[1].encode()
        # If no extension, default to .txt or empty
        if not ext: ext = b'.txt'
        ext = ext.ljust(8, b'#')
        
        # Add to payload: [EXT] + [DATA] + [DELIMITER]
        payload_bytes.extend(ext)
        payload_bytes.extend(secret_data)
        payload_bytes.extend(b'####')

    # Convert the payload bytes directly to bits using NumPy
    # (Much faster than formatting strings "010101")
    payload_arr = np.frombuffer(payload_bytes, dtype=np.uint8)
    payload_bits = np.unpackbits(payload_arr)
    
    # Check if image is big enough
    if len(payload_bits) > len(flat_arr):
        raise ValueError(f"❌ Not enough space! Need {len(payload_bits)} pixels, but image only has {len(flat_arr)}.")

    # Embed bits:
    # 1. Clear the LSB of the image pixels (bitwise AND with ~1)
    # 2. Add the secret bits (bitwise OR)
    # We only modify the part of the image needed to hold the data
    flat_arr[:len(payload_bits)] = (flat_arr[:len(payload_bits)] & ~1) | payload_bits
    
    # Reshape back to image and save
    new_arr = flat_arr.reshape(arr.shape)
    Image.fromarray(new_arr).save(output_path)
    print(f"✅ Secret data embedded into: {output_path}")

def extract_multiple_files(stego_path, output_dir):
    # Load image
    img = Image.open(stego_path).convert("RGB")
    arr = np.array(img)
    
    # Extract LSBs instantly using NumPy
    bits = arr.flatten() & 1
    
    # Pack bits back into bytes
    bytes_data = np.packbits(bits).tobytes()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the bytes to find files
    idx = 0
    file_count = 0
    total_len = len(bytes_data)
    
    print("🔍 Scanning for hidden files...")

    while idx < total_len:
        # We need at least 8 bytes for an extension
        if idx + 8 > total_len:
            break
            
        # 1. Read the Extension (First 8 bytes)
        ext_block = bytes_data[idx:idx+8]
        
        # Check if this looks like valid data (simple check)
        # If we reached the empty part of the image, the extension will likely be noise or 0s/255s
        # Our protocol pads extensions with '#'.
        try:
            ext_str = ext_block.replace(b'#', b'').decode('utf-8', errors='ignore')
        except:
            # If decoding fails, we probably hit the end of real data
            break
            
        # Move index past extension
        idx += 8
        
        # 2. Find the Delimiter (####)
        # This searches for the next '####' starting from current position
        delimiter_pos = bytes_data.find(b'####', idx)
        
        if delimiter_pos == -1:
            # No delimiter found, stop scanning
            break
            
        # 3. Extract the actual file data
        file_data = bytes_data[idx:delimiter_pos]
        
        # 4. Save the file
        # Clean up extension (remove dots if present to avoid double dots)
        clean_ext = ext_str.lstrip('.')
        if not clean_ext or len(clean_ext) > 4: 
            # Fallback if extension looks weird
            clean_ext = "bin"
            
        out_name = f"secret_{file_count}.{clean_ext}"
        out_path = os.path.join(output_dir, out_name)
        
        with open(out_path, 'wb') as f:
            f.write(file_data)
            
        print(f"✅ Extracted file {file_count+1}: {out_path}")
        
        # Move index past the delimiter (4 bytes) to look for next file
        idx = delimiter_pos + 4
        file_count += 1

    if file_count == 0:
        print("⚠️ No hidden files found or header corrupted.")