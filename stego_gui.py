import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
import io
import sys

# Import your modules
try:
    import steganography
    import analysis
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure steganography.py and analysis.py are in the same folder!")

class StegoProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LSB Steganography Pro v1.1 (Threaded)")
        self.root.geometry("600x750")
        
        # --- THEME COLORS ---
        self.colors = {
            "bg_dark": "#1E2028",      
            "bg_medium": "#2D2F3C",    
            "text_primary": "#DCDCEB", 
            "accent_gold": "#FFC850",  
            "btn_color": "#3C3F50",    
            "btn_hover": "#4C4F60",
            "success": "#4CAF50",
            "error": "#F44336"
        }

        self.root.configure(bg=self.colors["bg_dark"])
        
        # Setup Styles
        self.setup_styles()
        
        # --- VARIABLES ---
        self.cover_path = tk.StringVar()
        self.secret_files = []
        self.stego_input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.is_processing = False # Lock to prevent double clicks

        # --- LAYOUT ---
        self.create_header()
        self.create_notebook() 
        self.create_footer()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=self.colors["bg_dark"])
        style.configure("TLabel", background=self.colors["bg_dark"], foreground=self.colors["text_primary"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.colors["accent_gold"])
        
        style.configure("TNotebook", background=self.colors["bg_dark"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=self.colors["btn_color"], 
                        foreground=self.colors["text_primary"],
                        padding=[20, 10], 
                        font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", 
                  background=[("selected", self.colors["accent_gold"])],
                  foreground=[("selected", "#000000")])

    def create_header(self):
        header_h = 110
        self.header_canvas = tk.Canvas(self.root, height=header_h, bg=self.colors["bg_dark"], highlightthickness=0)
        self.header_canvas.pack(fill="x", side="top")
        
        self.header_canvas.create_rectangle(0, 0, 2000, header_h, fill="#282D46", outline="")
        self.header_canvas.create_oval(-50, -50, 150, 150, outline="white", width=2, stipple="gray25") 
        self.header_canvas.create_oval(500, 20, 650, 170, outline="white", width=1, dash=(4, 4))

        try:
            pil_img = Image.open("steganography_logo.png")
            pil_img = pil_img.resize((80, 80), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(pil_img)
            self.header_canvas.create_image(50, 55, image=self.logo_photo, anchor="center")
            text_x = 110
        except:
            text_x = 40 

        self.header_canvas.create_text(text_x, 45, text="IMAGE STEGANOGRAPHY", font=("Segoe UI", 24, "bold"), fill=self.colors["accent_gold"], anchor="w")
        self.header_canvas.create_text(text_x, 75, text="SECURE LSB EMBEDDING SUITE", font=("Segoe UI", 10), fill=self.colors["text_primary"], anchor="w")

    def create_notebook(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.tab_embed = ttk.Frame(notebook)
        notebook.add(self.tab_embed, text="  🔒 HIDE DATA  ")
        self.build_embed_tab()

        self.tab_extract = ttk.Frame(notebook)
        notebook.add(self.tab_extract, text="  🔓 EXTRACT DATA  ")
        self.build_extract_tab()
        
        self.tab_analysis = ttk.Frame(notebook)
        notebook.add(self.tab_analysis, text="  📊 ANALYSIS  ")
        self.build_analysis_tab()

    # ========================== TAB 1: EMBED ==========================
    def build_embed_tab(self):
        frame = tk.Frame(self.tab_embed, bg=self.colors["bg_dark"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        lbl = ttk.Label(frame, text="STEP 1: SELECT COVER IMAGE", style="Header.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        box1 = tk.Frame(frame, bg=self.colors["bg_medium"], padx=10, pady=10)
        box1.pack(fill="x", pady=(0, 20))
        
        self.lbl_cover_preview = tk.Label(box1, text="No Image Selected", bg=self.colors["bg_medium"], fg="#888")
        self.lbl_cover_preview.pack(side="left")
        
        self.create_button(box1, "Browse Image", self.select_cover_image).pack(side="right")

        lbl2 = ttk.Label(frame, text="STEP 2: ADD SECRET FILES", style="Header.TLabel")
        lbl2.pack(anchor="w", pady=(0, 5))
        
        box2 = tk.Frame(frame, bg=self.colors["bg_medium"], padx=10, pady=10)
        box2.pack(fill="both", expand=True, pady=(0, 20))
        
        self.list_secrets = tk.Listbox(box2, bg=self.colors["bg_dark"], fg="white", height=6, bd=0, highlightthickness=1, highlightbackground=self.colors["accent_gold"])
        self.list_secrets.pack(fill="both", expand=True, side="left", padx=(0, 10))
        
        btn_box = tk.Frame(box2, bg=self.colors["bg_medium"])
        btn_box.pack(side="right", fill="y")
        
        self.create_button(btn_box, "Add Files +", self.add_secret_files).pack(fill="x", pady=2)
        self.create_button(btn_box, "Clear List", self.clear_secret_files).pack(fill="x", pady=2)

        self.btn_run_embed = self.create_main_button(frame, "RUN EMBEDDING PROCESS", self.run_embed)
        self.btn_run_embed.pack(fill="x", side="bottom")

    # ========================== TAB 2: EXTRACT ==========================
    def build_extract_tab(self):
        frame = tk.Frame(self.tab_extract, bg=self.colors["bg_dark"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        lbl = ttk.Label(frame, text="STEP 1: SELECT STEGO IMAGE", style="Header.TLabel")
        lbl.pack(anchor="w", pady=(0, 5))
        
        box1 = tk.Frame(frame, bg=self.colors["bg_medium"], padx=10, pady=10)
        box1.pack(fill="x", pady=(0, 20))
        
        self.lbl_stego_preview = tk.Label(box1, text="No Image Selected", bg=self.colors["bg_medium"], fg="#888")
        self.lbl_stego_preview.pack(side="left")
        
        self.create_button(box1, "Browse Image", self.select_stego_image).pack(side="right")

        lbl2 = ttk.Label(frame, text="STEP 2: EXTRACTION", style="Header.TLabel")
        lbl2.pack(anchor="w", pady=(0, 5))
        
        info_lbl = tk.Label(frame, text="Files will be extracted to a 'Secret_files' folder in the selected location.", 
                            bg=self.colors["bg_dark"], fg="#666", font=("Segoe UI", 9, "italic"))
        info_lbl.pack(anchor="w", pady=(0, 20))
        
        # STATUS LABEL (To show "Processing..." when it freezes)
        self.lbl_status = tk.Label(frame, text="Ready", bg=self.colors["bg_dark"], fg=self.colors["accent_gold"], font=("Segoe UI", 10, "bold"))
        self.lbl_status.pack(side="bottom", pady=5)

        self.btn_run_extract = self.create_main_button(frame, "DECRYPT & EXTRACT FILES", self.run_extract)
        self.btn_run_extract.pack(fill="x", side="bottom")

    # ========================== TAB 3: ANALYSIS ==========================
    def build_analysis_tab(self):
        frame = tk.Frame(self.tab_analysis, bg=self.colors["bg_dark"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        lbl = ttk.Label(frame, text="COMPARE ORIGINAL VS STEGO", style="Header.TLabel")
        lbl.pack(anchor="w", pady=(0, 20))

        box1 = tk.Frame(frame, bg=self.colors["bg_medium"], padx=10, pady=10)
        box1.pack(fill="x", pady=5)
        self.path_ana_orig = tk.StringVar()
        tk.Label(box1, text="Original:", bg=self.colors["bg_medium"], fg="white", width=10, anchor="w").pack(side="left")
        tk.Entry(box1, textvariable=self.path_ana_orig, bg="#444", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        self.create_button(box1, "...", lambda: self.path_ana_orig.set(filedialog.askopenfilename())).pack(side="right")

        box2 = tk.Frame(frame, bg=self.colors["bg_medium"], padx=10, pady=10)
        box2.pack(fill="x", pady=5)
        self.path_ana_stego = tk.StringVar()
        tk.Label(box2, text="Stego Img:", bg=self.colors["bg_medium"], fg="white", width=10, anchor="w").pack(side="left")
        tk.Entry(box2, textvariable=self.path_ana_stego, bg="#444", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        self.create_button(box2, "...", lambda: self.path_ana_stego.set(filedialog.askopenfilename())).pack(side="right")

        btn_frame = tk.Frame(frame, bg=self.colors["bg_dark"])
        btn_frame.pack(fill="x", pady=30)
        
        self.create_main_button(btn_frame, "SHOW HISTOGRAM", lambda: self.run_analysis("hist")).pack(fill="x", pady=5)
        self.create_main_button(btn_frame, "CALCULATE PSNR & SIZE", lambda: self.run_analysis("stats")).pack(fill="x", pady=5)

    def create_footer(self):
        lbl = tk.Label(self.root, text="Developed for Cybersecurity Steganography", 
                       bg=self.colors["bg_dark"], fg="#666", font=("Segoe UI", 8))
        lbl.pack(side="bottom", pady=10)

    # ========================== WIDGET HELPERS ==========================
    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, 
                        bg=self.colors["btn_color"], fg=self.colors["text_primary"],
                        font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5)
        return btn
    
    def create_main_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, 
                        bg=self.colors["bg_dark"], fg=self.colors["accent_gold"],
                        font=("Segoe UI", 11, "bold"), relief="solid", bd=2, padx=10, pady=10)
        btn.config(highlightbackground=self.colors["accent_gold"], highlightthickness=1)
        return btn

    # ========================== LOGIC ==========================
    
    # --- EMBED LOGIC ---
    def select_cover_image(self):
        path = filedialog.askopenfilename(filetypes=[
            ("Lossless Images", "*.png *.bmp *.tiff *.tif"),
            ("PNG Images", "*.png"),
            ("BMP Images", "*.bmp"),
            ("TIFF Images", "*.tiff")
        ])
        if path:
            self.cover_path.set(path)
            self.lbl_cover_preview.config(text=os.path.basename(path), fg=self.colors["accent_gold"])

    def add_secret_files(self):
        paths = filedialog.askopenfilenames()
        for path in paths:
            self.secret_files.append(path)
            self.list_secrets.insert(tk.END, os.path.basename(path))

    def clear_secret_files(self):
        self.secret_files = []
        self.list_secrets.delete(0, tk.END)

    def run_embed(self):
        if self.is_processing: return
        
        cover = self.cover_path.get()
        secrets = self.secret_files
        
        if not cover or not secrets:
            messagebox.showerror("Error", "Please select a cover image and at least one secret file.")
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG Image", "*.png"), ("BMP Image", "*.bmp"), ("TIFF Image", "*.tiff")]
        )
        if not out_path:
            return

        # Disable button and set flag
        self.is_processing = True
        self.btn_run_embed.config(text="PROCESSING... PLEASE WAIT", state="disabled", bg="#555")

        # THREADED WORKER FUNCTION
        def worker():
            try:
                steganography.embed_multiple_files(cover, secrets, out_path)
                # Success Message (Must be scheduled back to main thread or called safely)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Data embedded successfully!\nSaved at: {out_path}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Embedding failed: {str(e)}"))
            finally:
                # Reset button state
                self.root.after(0, lambda: self.reset_embed_button())

        # Start the thread
        threading.Thread(target=worker, daemon=True).start()

    def reset_embed_button(self):
        self.is_processing = False
        self.btn_run_embed.config(text="RUN EMBEDDING PROCESS", state="normal", bg=self.colors["bg_dark"])

    # --- EXTRACT LOGIC ---
    def select_stego_image(self):
        path = filedialog.askopenfilename(filetypes=[
            ("Lossless Images", "*.png *.bmp *.tiff *.tif"),
            ("PNG Images", "*.png"),
            ("BMP Images", "*.bmp"),
            ("TIFF Images", "*.tiff")
        ])
        if path:
            self.stego_input_path.set(path)
            self.lbl_stego_preview.config(text=os.path.basename(path), fg=self.colors["accent_gold"])

    def run_extract(self):
        if self.is_processing: return

        stego = self.stego_input_path.get()
        if not stego:
            messagebox.showerror("Error", "Please select a steganography image first.")
            return
            
        out_dir = filedialog.askdirectory(title="Select Output Folder")
        if not out_dir:
            return
            
        final_dir = os.path.join(out_dir, "Secret_files")
        
        # Disable button and set flag
        self.is_processing = True
        self.btn_run_extract.config(text="EXTRACTING... PLEASE WAIT", state="disabled", bg="#555")
        self.lbl_status.config(text="Processing... (This may take a minute)", fg="white")

        # THREADED WORKER FUNCTION
        def worker():
            try:
                steganography.extract_multiple_files(stego, final_dir)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Files extracted successfully!\nCheck folder: {final_dir}"))
                self.root.after(0, lambda: self.lbl_status.config(text="Extraction Complete ✅", fg=self.colors["success"]))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Extraction failed: {str(e)}"))
                self.root.after(0, lambda: self.lbl_status.config(text="Extraction Failed ❌", fg=self.colors["error"]))
            finally:
                self.root.after(0, lambda: self.reset_extract_button())

        # Start the thread
        threading.Thread(target=worker, daemon=True).start()

    def reset_extract_button(self):
        self.is_processing = False
        self.btn_run_extract.config(text="DECRYPT & EXTRACT FILES", state="normal", bg=self.colors["bg_dark"])

    # --- ANALYSIS LOGIC ---
    def run_analysis(self, mode):
        orig = self.path_ana_orig.get()
        stego = self.path_ana_stego.get()
        
        if not orig or not stego:
            messagebox.showerror("Error", "Please select both Original and Stego images.")
            return

        # Simple tasks can run on main thread, but charts block too. 
        # Matplotlib blocks naturally, so we accept that, or we thread it.
        # Let's thread statistics at least.
        
        if mode == "stats":
            def worker():
                try:
                    buffer = io.StringIO()
                    original_stdout = sys.stdout
                    sys.stdout = buffer
                    
                    analysis.calculate_psnr(orig, stego)
                    print("-" * 30) 
                    analysis.compare_file_size(orig, stego)
                    
                    output_text = buffer.getvalue()
                    sys.stdout = original_stdout
                    
                    self.root.after(0, lambda: messagebox.showinfo("Analysis Results", output_text))
                except Exception as e:
                    if 'original_stdout' in locals(): sys.stdout = original_stdout
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))

            threading.Thread(target=worker, daemon=True).start()
            
        elif mode == "hist":
            # Matplotlib must run in main thread usually, or it crashes tkinter.
            # We keep this one on main thread.
            try:
                analysis.show_histogram(orig, stego)
            except Exception as e:
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoProGUI(root)
    root.mainloop()