# 🔒 StegoPro: LSB Image Steganography Suite

A high-performance, GUI-based tool for hiding multiple secret files inside lossless images (PNG, BMP, TIFF) using **Least Significant Bit (LSB)** steganography.

Built with **Python**, **Tkinter**, and **NumPy**, this tool offers instant processing speeds, threading support to prevent freezing, and a built-in analysis suite to verify the security of your hidden data.

## ✨ Features

* **Multi-File Embedding:** Hide multiple files (TXT, DOCX, IMG, etc.) inside a single cover image.
* **High Performance:** Uses **NumPy** matrix operations for sub-second processing (no slow loops).
* **Modern GUI:** Dark-themed Tkinter interface with threading support (no "Not Responding" lag).
* **Lossless Support:** Works with PNG, BMP, and TIFF formats to ensure data integrity.
* **Analysis Tools:** Built-in tools to calculate **PSNR** (Peak Signal-to-Noise Ratio), histograms, and file size differences to ensure the steganography is undetectable.
* **Smart Parsing:** Automatically handles file delimiters and extensions.

🛠️ Prerequisites
Ensure you have Python installed. You will need to install the following libraries:

```Bash

pip install pillow numpy opencv-python matplotlib
```
Note: tkinter usually comes pre-installed with Python.

📥 Installation
You can download and run this tool directly from GitHub:

```Bash
# 1. Clone the repository
git clone https://github.com/FrhnIsml/StegoPro.git

# 2. Navigate to the project folder (Use the full folder name)
cd StegoPro

# 3. Run the tool
python stego_gui.py
```

*Note: `tkinter` usually comes pre-installed with Python.*

## 🚀 Usage

### 1. Launching the GUI

Run the main GUI script:

```bash
python stego_gui.py

```

### 2. Hiding Data (Encryption)

1. Go to the **"🔒 HIDE DATA"** tab.
2. **Select Cover Image:** Choose a PNG, BMP, or TIFF image.
3. **Add Secret Files:** Select one or more files you want to hide.
4. Click **"RUN EMBEDDING PROCESS"**.
5. Save the resulting "Stego Image".

### 3. Recovering Data (Decryption)

1. Go to the **"🔓 EXTRACT DATA"** tab.
2. **Select Stego Image:** Choose the image containing the hidden data.
3. Click **"DECRYPT & EXTRACT FILES"**.
4. Select a destination folder. The tool will automatically create a `Secret_files` folder with your recovered data.

### 4. Analyzing Quality

1. Go to the **"📊 ANALYSIS"** tab.
2. Select the **Original** image and the **Stego** image.
3. **Calculate PSNR:** Checks the quality. (A value > 60dB is considered Perfect/Indistinguishable).
4. **Show Histogram:** visualizes the pixel intensity distribution to check for statistical attacks.

## 🧠 Technical Details

### The Algorithm (LSB)

This tool uses **Least Significant Bit (LSB)** substitution.

1. The image is converted into a flattened NumPy array of pixel values (0-255).
2. The secret files are converted into a binary stream, separated by a delimiter (`####`).
3. The last bit of the image's RGB bytes is replaced with the secret data bits.
4. Since the change is only +/- 1 to a color value, it is invisible to the human eye.

### Performance Note

Unlike traditional Python steganography scripts that loop through pixels one by one, this tool uses **NumPy Vectorization**. This allows it to process millions of pixels instantly.

### Supported Formats

* **Supported:** PNG, BMP, TIFF (Lossless compression keeps data safe).
* **Not Supported:** JPG/JPEG (Lossy compression destroys the hidden bits).

## 📂 Project Structure

```text
.
├── stego_gui.py        # The main GUI application (Run this!)
├── steganography.py    # Core logic for LSB embedding/extracting (NumPy optimized)
├── analysis.py         # Tools for PSNR calculation and Histogram plotting
├── main.py             # CLI version for testing without GUI
├── cipher_logo.png     # (Optional) Logo for the GUI header
└── README.md           # This documentation

```

## 📊 Analysis Grading Scale

When using the Analysis tab, the tool grades the steganography quality based on PSNR:

| PSNR Value | Quality Level | Description |
| --- | --- | --- |
| **> 60 dB** | 🔵 **PERFECT** | Mathematically indistinguishable. |
| **40 - 60 dB** | 🟢 **GOOD** | Invisible to the human eye. |
| **30 - 40 dB** | 🟠 **ACCEPTABLE** | Slight noise may be detectable. |
| **< 30 dB** | 🔴 **POOR** | Visible distortion. |

## 👤 Author

**Farhan Ismail**
*Developed for Cryptography Lab*

## 📄 License


This project is open-source and free to use for educational purposes.










# 🔒 StegoPro: LSB Image Steganography Suite

A high-performance, GUI-based tool for hiding multiple secret files inside lossless images (PNG, BMP, TIFF) using **Least Significant Bit (LSB)** steganography.

Built with **Python**, **Tkinter**, and **NumPy**, this tool offers instant processing speeds, threading support to prevent freezing, and a built-in analysis suite to verify the security of your hidden data.

## ✨ Features

* **Multi-File Embedding:** Hide multiple files (TXT, DOCX, IMG, etc.) inside a single cover image.
* **High Performance:** Uses **NumPy** matrix operations for sub-second processing (no slow loops).
* **Modern GUI:** Dark-themed Tkinter interface with threading support (no "Not Responding" lag).
* **Lossless Support:** Works with PNG, BMP, and TIFF formats to ensure data integrity.
* **Analysis Tools:** Built-in tools to calculate **PSNR** (Peak Signal-to-Noise Ratio), histograms, and file size differences to ensure the steganography is undetectable.
* **Smart Parsing:** Automatically handles file delimiters and extensions.

🛠️ Prerequisites
Ensure you have Python installed. You will need to install the following libraries:

```Bash

pip install pillow numpy opencv-python matplotlib
```
Note: tkinter usually comes pre-installed with Python.

📥 Installation
You can download and run this tool directly from GitHub:

```Bash
# 1. Clone the repository
git clone https://github.com/FrhnIsml/StegoPro.git

# 2. Navigate to the project folder (Use the full folder name)
cd StegoPro

# 3. Run the tool
python stego_gui.py
```

*Note: `tkinter` usually comes pre-installed with Python.*

## 🚀 Usage

### 1. Launching the GUI

Run the main GUI script:

```bash
python stego_gui.py

```

### 2. Hiding Data (Encryption)

1. Go to the **"🔒 HIDE DATA"** tab.
2. **Select Cover Image:** Choose a PNG, BMP, or TIFF image.
3. **Add Secret Files:** Select one or more files you want to hide.
4. Click **"RUN EMBEDDING PROCESS"**.
5. Save the resulting "Stego Image".

### 3. Recovering Data (Decryption)

1. Go to the **"🔓 EXTRACT DATA"** tab.
2. **Select Stego Image:** Choose the image containing the hidden data.
3. Click **"DECRYPT & EXTRACT FILES"**.
4. Select a destination folder. The tool will automatically create a `Secret_files` folder with your recovered data.

### 4. Analyzing Quality

1. Go to the **"📊 ANALYSIS"** tab.
2. Select the **Original** image and the **Stego** image.
3. **Calculate PSNR:** Checks the quality. (A value > 60dB is considered Perfect/Indistinguishable).
4. **Show Histogram:** visualizes the pixel intensity distribution to check for statistical attacks.

## 🧠 Technical Details

### The Algorithm (LSB)

This tool uses **Least Significant Bit (LSB)** substitution.

1. The image is converted into a flattened NumPy array of pixel values (0-255).
2. The secret files are converted into a binary stream, separated by a delimiter (`####`).
3. The last bit of the image's RGB bytes is replaced with the secret data bits.
4. Since the change is only +/- 1 to a color value, it is invisible to the human eye.

### Performance Note

Unlike traditional Python steganography scripts that loop through pixels one by one, this tool uses **NumPy Vectorization**. This allows it to process millions of pixels instantly.

### Supported Formats

* **Supported:** PNG, BMP, TIFF (Lossless compression keeps data safe).
* **Not Supported:** JPG/JPEG (Lossy compression destroys the hidden bits).

## 📂 Project Structure

```text
.
├── stego_gui.py        # The main GUI application (Run this!)
├── steganography.py    # Core logic for LSB embedding/extracting (NumPy optimized)
├── analysis.py         # Tools for PSNR calculation and Histogram plotting
├── main.py             # CLI version for testing without GUI
├── cipher_logo.png     # (Optional) Logo for the GUI header
└── README.md           # This documentation

```

## 📊 Analysis Grading Scale

When using the Analysis tab, the tool grades the steganography quality based on PSNR:

| PSNR Value | Quality Level | Description |
| --- | --- | --- |
| **> 60 dB** | 🔵 **PERFECT** | Mathematically indistinguishable. |
| **40 - 60 dB** | 🟢 **GOOD** | Invisible to the human eye. |
| **30 - 40 dB** | 🟠 **ACCEPTABLE** | Slight noise may be detectable. |
| **< 30 dB** | 🔴 **POOR** | Visible distortion. |



*Tools*


<img width="739" height="966" alt="image" src="https://github.com/user-attachments/assets/ec824ccc-7549-4278-9d58-9bde213fb772" />



## 👤 Author

**Farhan Ismail**
*Developed for Steganography Tools*

## 📄 License


This project is open-source and free to use for educational purposes.






