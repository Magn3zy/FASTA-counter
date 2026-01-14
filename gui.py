import tkinter as tk
from tkinter import messagebox, filedialog, ttk

def base_count(fasta_file):
    bases = {'A': 0, 'G': 0, 'C': 0, 'T': 0, 'N': 0}
    total_length = 0

    try:
        with open(fasta_file, 'r') as file:
            for line in file:
                if not line.startswith('>'):  
                    line = line.strip().upper()  
                    total_length += len(line)
                    for base in bases:
                        bases[base] += line.count(base)  

    except FileNotFoundError:
        messagebox.showerror("Chyba", "Soubor nebyl nalezen!")
        return None, None

    return total_length, bases

def browse_file():
    file = filedialog.askopenfilename(
        title="Vyberte FASTA soubor",
        filetypes=[("FASTA soubory", "*.fasta *.fa"), ("Všechny soubory", "*.*")]
    )
    if file:  
        file_path.set(file)  
        length, base_counts = base_count(file)  
        if length is not None:
            result_label.config(text=f"Celkový počet bází: {length}")
            update_table(base_counts)
        else:
            result_label.config(text="Došlo k chybě při čtení souboru.")

def update_table(base_counts):
    for base, count in base_counts.items():
        tree.item(base, values=(base, count))

root = tk.Tk()
root.title("FASTA Base Counter")

file_path = tk.StringVar()

file_frame = ttk.LabelFrame(root, text="Výběr souboru", padding=5)
file_frame.pack(fill="x", padx=5, pady=5)

ttk.Entry(file_frame, textvariable=file_path, width=50).pack(side="left", padx=5)
ttk.Button(file_frame, text="Procházet", command=browse_file).pack(side="left", padx=5)

result_label = tk.Label(root, text="Celkový počet bází: N/A")
result_label.pack(pady=10)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("Báze", "Počet"), show="headings", height=5)
tree.heading("Báze", text="Báze")
tree.heading("Počet", text="Počet")
tree.column("Báze", width=100, anchor="center")
tree.column("Počet", width=100, anchor="center")

for base in ['A', 'G', 'C', 'T', 'N']:
    tree.insert("", "end", iid=base,values=(base, 0))
                
tree.pack()

root.mainloop()