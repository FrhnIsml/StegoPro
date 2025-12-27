from steganography import embed_multiple_files, extract_multiple_files
from analysis import show_histogram, calculate_psnr, compare_file_size

# Embed multiple files into one cover image
secret_files = [
    "test_files/secret.txt",
    "test_files/secret.docx",
    "test_files/secret.png"
]

embed_multiple_files("test_files/cover.png", secret_files, "test_files/stego_multiple.png")

# Extract all files from the stego image
extract_multiple_files("test_files/stego_multiple.png", "test_files/Secret_files")

# Analysis
original = "test_files/cover.png"
stego = "test_files/stego_multiple.png"

show_histogram(original, stego)
calculate_psnr(original, stego)
compare_file_size(original, stego)