import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

def show_histogram(original, stego):
    img1 = cv2.imread(original)
    img2 = cv2.imread(stego)
    
    plt.figure(figsize=(12, 6))
    
    # Create x-axis values
    x = np.arange(256)
    
    for i, color in enumerate(['b','g','r']):
        hist1 = cv2.calcHist([img1], [i], None, [256], [0,256])
        hist2 = cv2.calcHist([img2], [i], None, [256], [0,256])
        
        # Plot original as semi-transparent bars
        plt.bar(x, hist1.flatten(), color=color, alpha=0.3, width=1.0, 
               label=f'Original {color}')
        
        # Plot stego as solid line with different line styles
        line_style = '-' if i == 0 else '--' if i == 1 else ':'
        plt.plot(hist2, color=color, linestyle=line_style, 
               linewidth=2, label=f'Stego {color}')
    
    plt.title('Histogram Comparison (Original: Bars, Stego: Lines)')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.xlim([0, 255])
    plt.tight_layout()
    plt.show()

def calculate_psnr(original, stego):
    img1 = cv2.imread(original)
    img2 = cv2.imread(stego)
    
    # Calculate PSNR
    psnr = cv2.PSNR(img1, img2)
    
    # Determine Level
    if psnr > 60:
        grade = "🔵 PERFECT (Indistinguishable)"
    elif psnr > 40:
        grade = "🟢 GOOD (Invisible to eye)"
    elif psnr > 30:
        grade = "🟠 ACCEPTABLE (Slight noise)"
    else:
        grade = "🔴 POOR (Visible distortion)"

    print(f"🔍 PSNR Value: {psnr:.2f} dB")
    print(f"📊 Quality Level: {grade}")

def compare_file_size(original, stego):
    size1 = os.path.getsize(original)
    size2 = os.path.getsize(stego)
    
    print(f"📂 Original size: {size1:,} bytes")
    print(f"📂 Stego size:    {size2:,} bytes")
    diff = size2 - size1
    print(f"📈 Size difference: {diff:,} bytes")