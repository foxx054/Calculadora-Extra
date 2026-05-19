import tkinter as tk
from tkinter import ttk, messagebox


def calcular_inss(base):
    faixas = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14),
    ]
    teto = 908.85
    inss = 0
    faixa_anterior = 0
    for teto_faixa, aliquota in faixas:
        if base > teto_faixa:
            inss += (teto_faixa - faixa_anterior) * aliquota
        else:
            inss += (base - faixa_anterior) * aliquota
            break
        faixa_anterior = teto_faixa
    return min(inss, teto)


def calcular_irrf(base, dependentes=0):
    deducao_dependente = 189.59
    base_irrf = base - dependentes * deducao_dependente
    faixas = [
        (2259.20, 0, 0),
        (2826.65, 0.075, 158.40),
        (3751.05, 0.15, 370.40),
        (4664.68, 0.225, 651.73),
        (float("inf"), 0.275, 884.96),
    ]
    for teto, aliquota, deducao in faixas:
        if base_irrf <= teto:
            irrf = base_irrf * aliquota - deducao
            return max(irrf, 0)
    return 0


def formatar(valor):
    return f"R$ {valor:>9.2f}"


def calcular():
    try:
        salario_hora = float(entry_salario.get().replace(",", "."))
        horas_normais = float(entry_normais.get().replace(",", "."))
        horas_50 = float(entry_50.get().replace(",", "."))
        horas_100 = float(entry_100.get().replace(",", "."))
        dependentes = int(entry_dependentes.get())
    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos com valores validos.")
        return

    salario_base = salario_hora * horas_normais
    adicional_50 = salario_hora * 1.5 * horas_50
    adicional_100 = salario_hora * 2 * horas_100
    total_bruto = salario_base + adicional_50 + adicional_100

    inss = calcular_inss(total_bruto)
    irrf = calcular_irrf(total_bruto - inss, dependentes)
    total_liquido = total_bruto - inss - irrf

    lbl_base_val.config(text=formatar(salario_base))
    lbl_50_val.config(text=formatar(adicional_50))
    lbl_100_val.config(text=formatar(adicional_100))
    lbl_bruto_val.config(text=formatar(total_bruto))
    lbl_inss_val.config(text=formatar(inss))
    lbl_irrf_val.config(text=formatar(irrf))
    lbl_liquido_val.config(text=formatar(total_liquido))


def limpar():
    entry_salario.delete(0, tk.END)
    entry_normais.delete(0, tk.END)
    entry_50.delete(0, tk.END)
    entry_100.delete(0, tk.END)
    entry_dependentes.delete(0, tk.END)
    entry_dependentes.insert(0, "0")
    for lbl in [lbl_base_val, lbl_50_val, lbl_100_val, lbl_bruto_val,
                lbl_inss_val, lbl_irrf_val, lbl_liquido_val]:
        lbl.config(text="")


root = tk.Tk()
root.title("Calculadora de Horas Extras")
root.geometry("480x520")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("vista")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

mainframe = ttk.Frame(root, padding="20")
mainframe.pack(fill=tk.BOTH, expand=True)

ttk.Label(mainframe, text="Calculadora de Horas Extras", style="Header.TLabel").grid(
    row=0, column=0, columnspan=2, pady=(0, 20)
)

# Entradas
campos = [
    ("Salario por hora (R$):", "entry_salario"),
    ("Horas normais:", "entry_normais"),
    ("Horas extras 50%:", "entry_50"),
    ("Horas extras 100%:", "entry_100"),
    ("Dependentes:", "entry_dependentes"),
]

entry_salario = ttk.Entry(mainframe, width=25, font=("Segoe UI", 10))
entry_normais = ttk.Entry(mainframe, width=25, font=("Segoe UI", 10))
entry_50 = ttk.Entry(mainframe, width=25, font=("Segoe UI", 10))
entry_100 = ttk.Entry(mainframe, width=25, font=("Segoe UI", 10))
entry_dependentes = ttk.Entry(mainframe, width=25, font=("Segoe UI", 10))

entries = [entry_salario, entry_normais, entry_50, entry_100, entry_dependentes]
labels_text = [
    "Salario por hora (R$):",
    "Horas normais:",
    "Horas extras 50%:",
    "Horas extras 100%:",
    "Dependentes:",
]

for i, (text, ent) in enumerate(zip(labels_text, entries)):
    ttk.Label(mainframe, text=text).grid(row=i + 1, column=0, sticky=tk.W, pady=4)
    ent.grid(row=i + 1, column=1, sticky=tk.EW, pady=4, padx=(10, 0))

entry_dependentes.insert(0, "0")

# Botoes
btn_frame = ttk.Frame(mainframe)
btn_frame.grid(row=6, column=0, columnspan=2, pady=(15, 10))

ttk.Button(btn_frame, text="Calcular", command=calcular, width=15).pack(
    side=tk.LEFT, padx=5
)
ttk.Button(btn_frame, text="Limpar", command=limpar, width=15).pack(
    side=tk.LEFT, padx=5
)

# Resultados
sep = ttk.Separator(mainframe, orient="horizontal")
sep.grid(row=7, column=0, columnspan=2, sticky=tk.EW, pady=10)

ttk.Label(mainframe, text="RESULTADO", style="Header.TLabel").grid(
    row=8, column=0, columnspan=2, pady=(0, 10)
)

result_labels = [
    ("Salario base:", "lbl_base_val"),
    ("Adicional 50%:", "lbl_50_val"),
    ("Adicional 100%:", "lbl_100_val"),
    ("Total Bruto:", "lbl_bruto_val"),
    ("INSS:", "lbl_inss_val"),
    ("IRRF:", "lbl_irrf_val"),
    ("Total Liquido:", "lbl_liquido_val"),
]

lbl_base_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_50_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_100_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_bruto_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_inss_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_irrf_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))
lbl_liquido_val = ttk.Label(mainframe, text="", font=("Segoe UI", 10, "bold"))

val_labels = [
    lbl_base_val,
    lbl_50_val,
    lbl_100_val,
    lbl_bruto_val,
    lbl_inss_val,
    lbl_irrf_val,
    lbl_liquido_val,
]

for i, (text, _) in enumerate(result_labels):
    lbl = ttk.Label(mainframe, text=text)
    lbl.grid(row=9 + i, column=0, sticky=tk.W, pady=2)
    val_labels[i].grid(row=9 + i, column=1, sticky=tk.E, pady=2)

# total liquido em destaque
lbl_liquido_val.config(font=("Segoe UI", 12, "bold"), foreground="#006400")

root.mainloop()
