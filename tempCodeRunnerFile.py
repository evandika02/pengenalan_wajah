import tkinter as tk
from tkinter import filedialog, messagebox

def lzw_compress(uncompressed):
    """Kompresi string menjadi daftar simbol output."""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

def lzw_decompress(compressed):
    """Dekompresi daftar output ke string."""
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    result = []
    w = chr(compressed[0])
    result.append(w)
    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Kode terkompresi salah: %s' % k)
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return "".join(result)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kompresi Media")
        self.geometry("400x300")

        # Menu
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        # Label dan Entry untuk menampilkan file yang dipilih
        self.file_label = tk.Label(self, text="File yang dipilih:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self, width=50)
        self.file_entry.pack()

        # Tombol kompresi
        self.compress_button = tk.Button(self, text="Kompresi", command=self.compress_file)
        self.compress_button.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def compress_file(self):
        file_path = self.file_entry.get()
        if file_path:
            try:
                file_extension = file_path.split('.')[-1].lower()
                with open(file_path, "rb") as f:
                    data = f.read()
                
                compressed_data = lzw_compress(data.decode('latin1'))
                compressed_data_bytes = bytearray()
                for num in compressed_data:
                    compressed_data_bytes.extend(num.to_bytes((num.bit_length() + 7) // 8, byteorder='big'))

                compressed_file_path = file_path + ".lzw"
                with open(compressed_file_path, "wb") as f:
                    f.write(compressed_data_bytes)
                
                if file_extension in ['png', 'jpg', 'jpeg', 'bmp']:
                    messagebox.showinfo("Success", f"Gambar berhasil dikompresi menjadi {compressed_file_path}")
                elif file_extension in ['mp3', 'wav', 'flac']:
                    messagebox.showinfo("Success", f"Audio berhasil dikompresi menjadi {compressed_file_path}")
                elif file_extension in ['mp4', 'avi', 'mov']:
                    messagebox.showinfo("Success", f"Video berhasil dikompresi menjadi {compressed_file_path}")
                else:
                    messagebox.showinfo("Success", f"File berhasil dikompresi menjadi {compressed_file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengompresi file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Harap pilih file terlebih dahulu")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
