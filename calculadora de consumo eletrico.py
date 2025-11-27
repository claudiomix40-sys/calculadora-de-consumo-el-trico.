
"""Autor: Claudio Augusto R. Betoni"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def parse_float(txt: str, default=0.0) -> float:
    if txt is None:
        return default
    txt = txt.strip().replace(" ", "")
    if not txt:
        return default
    try:
        return float(txt.replace(",", "."))
    except Exception:
        return default

def fmt_moeda(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Consumo de Energia para atividade extencionista II")
        self.geometry("1150x600")
        self.minsize(1000, 560)
        self._build_ui()

    def _build_ui(self):
        self.editing_iid = None
        self.btn_label = tk.StringVar(value="Adicionar")
        root = ttk.Frame(self, padding=10)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        top = ttk.LabelFrame(root, text="Dados da Conta", padding=10)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(top, text="Tarifa C/Tributos (R$/kWh):").grid(row=0, column=0, sticky="w")
        self.tarifa_var = tk.StringVar(value="0,95")
        ttk.Entry(top, width=10, textvariable=self.tarifa_var, justify="right").grid(row=0, column=1, padx=(6, 16))
        ttk.Label(top, text="Bandeira + iluminação pub/kWh total da conta:").grid(row=0, column=2, sticky="w")
        self.bandeira_var = tk.StringVar(value="0,00")
        ttk.Entry(top, width=10, textvariable=self.bandeira_var, justify="right").grid(row=0, column=3, padx=(6, 16))

        mid = ttk.LabelFrame(root, text="Equipamentos", padding=10)
        mid.grid(row=1, column=0, sticky="nsew")
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(1, weight=1)

        form = ttk.Frame(mid)
        form.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(form, text="Nome").grid(row=0, column=0)
        self.nome_var = tk.StringVar()
        ttk.Entry(form, width=22, textvariable=self.nome_var).grid(row=1, column=0, padx=(0, 8))
        ttk.Label(form, text="Potência (W)").grid(row=0, column=1)
        self.pot_var = tk.StringVar()
        ttk.Entry(form, width=10, textvariable=self.pot_var, justify="right").grid(row=1, column=1, padx=(0, 8))
        ttk.Label(form, text="Qtd").grid(row=0, column=2)
        self.qtd_var = tk.StringVar(value="1")
        ttk.Entry(form, width=6, textvariable=self.qtd_var, justify="right").grid(row=1, column=2, padx=(0, 8))
        ttk.Label(form, text="Horas/dia").grid(row=0, column=3)
        self.horas_var = tk.StringVar(value="1")
        ttk.Entry(form, width=8, textvariable=self.horas_var, justify="right").grid(row=1, column=3, padx=(0, 8))
        ttk.Label(form, text="Dias/mês").grid(row=0, column=4)
        self.dias_var = tk.StringVar(value="30")
        ttk.Entry(form, width=8, textvariable=self.dias_var, justify="right").grid(row=1, column=4, padx=(0, 8))
        ttk.Button(form, textvariable=self.btn_label, command=self.add_item).grid(row=1, column=5, padx=(8,4))
        ttk.Button(form, text="Editar selecionado", command=self.start_edit).grid(row=1, column=6, padx=(4,4))
        ttk.Button(form, text="Cancelar edição", command=self.cancel_edit).grid(row=1, column=7, padx=(4,8))
        ttk.Button(form, text="Remover selecionado", command=self.del_item).grid(row=1, column=8, padx=(4, 8))

        cols = ("nome", "pot", "qtd", "h_dia", "d_mes", "wh_dia", "kwh", "custo")
        self.tv = ttk.Treeview(mid, columns=cols, show="headings", height=10)
        self.tv.grid(row=1, column=0, sticky="nsew")
        for col, w in zip(cols, (200, 80, 60, 80, 80, 100, 100, 110)):
            self.tv.column(col, width=w, anchor=tk.E if col not in ("nome",) else tk.W, stretch=True)
        self.tv.heading("nome", text="Nome")
        self.tv.heading("pot", text="Potência (W)")
        self.tv.heading("qtd", text="Qtd")
        self.tv.heading("h_dia", text="Horas/dia")
        self.tv.heading("d_mes", text="Dias/mês")
        self.tv.heading("wh_dia", text="Wh/dia")
        self.tv.heading("kwh", text="kWh/mês")
        self.tv.heading("custo", text="Custo (R$)")

        yscroll = ttk.Scrollbar(mid, orient=tk.VERTICAL, command=self.tv.yview)
        self.tv.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column=1, sticky="ns")

        bottom = ttk.Frame(root)
        bottom.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        for c in range(8):
            bottom.columnconfigure(c, weight=0)
        bottom.columnconfigure(7, weight=1)

        self.total_kwh_var = tk.StringVar(value="0,00 kWh/mês")
        self.total_rs_var = tk.StringVar(value=fmt_moeda(0.0))

        ttk.Button(bottom, text="Abrir lista…", command=self.load_list).grid(row=0, column=0, padx=(0,6))
        ttk.Button(bottom, text="Salvar lista…", command=self.save_list).grid(row=0, column=1, padx=(0,16))
        ttk.Button(bottom, text="Calcular", command=self.calcular).grid(row=0, column=2, sticky="w")

        ttk.Label(bottom, text="Total kWh/mês:").grid(row=0, column=3, sticky="e")
        ttk.Label(bottom, textvariable=self.total_kwh_var, font=("Segoe UI", 10, "bold")).grid(row=0, column=4, sticky="w", padx=(6, 16))
        ttk.Label(bottom, text="Custo total:").grid(row=0, column=5, sticky="e")
        ttk.Label(bottom, textvariable=self.total_rs_var, font=("Segoe UI", 11, "bold")).grid(row=0, column=6, sticky="w", padx=(6, 0))

    def add_item(self):
        """Insere um novo item ou atualiza o item em edição."""
        nome = self.nome_var.get().strip() or "Item"
        pot = parse_float(self.pot_var.get(), 0.0)
        qtd = int(parse_float(self.qtd_var.get(), 1))
        horas = parse_float(self.horas_var.get(), 0.0)
        dias = int(parse_float(self.dias_var.get(), 30))
        if pot <= 0 or horas < 0 or dias <= 0 or qtd <= 0:
            messagebox.showerror("Dados inválidos", "Verifique os valores.")
            return
        tarifa = parse_float(self.tarifa_var.get(), 0.0)
        bandeira = parse_float(self.bandeira_var.get(), 0.0)
        wh_dia = pot * horas * qtd
        kwh_mes = (wh_dia * dias) / 1000.0
        custo = kwh_mes * (tarifa + bandeira)

        if self.editing_iid:
            # Atualiza linha existente
            self.tv.item(self.editing_iid, values=(
                nome,
                f"{pot:.0f}",
                str(qtd),
                f"{horas:.2f}",
                str(dias),
                f"{wh_dia:.1f}",
                f"{kwh_mes:.3f}",
                fmt_moeda(custo)
            ))
            self.editing_iid = None
            self.btn_label.set("Adicionar")
        else:
            # Insere nova linha
            self.tv.insert("", tk.END, values=(
                nome,
                f"{pot:.0f}",
                str(qtd),
                f"{horas:.2f}",
                str(dias),
                f"{wh_dia:.1f}",
                f"{kwh_mes:.3f}",
                fmt_moeda(custo)
            ))

        # Limpa campos
        self.nome_var.set("")
        self.pot_var.set("")

    def del_item(self):
        for iid in self.tv.selection():
            # Se apagar o item em edição, sai do modo edição
            if self.editing_iid == iid:
                self.editing_iid = None
                self.btn_label.set("Adicionar")
            self.tv.delete(iid)

    def start_edit(self):
        """Carrega os dados do item selecionado para o formulário para edição."""
        sel = self.tv.selection()
        if not sel:
            messagebox.showinfo("Editar", "Selecione uma linha para editar.")
            return
        iid = sel[0]
        vals = self.tv.item(iid, "values")
        try:
            self.nome_var.set(vals[0])
            self.pot_var.set(str(vals[1]))
            self.qtd_var.set(str(vals[2]))
            self.horas_var.set(str(vals[3]))
            self.dias_var.set(str(vals[4]))
            self.editing_iid = iid
            self.btn_label.set("Atualizar")
        except Exception:
            messagebox.showerror("Editar", "Não foi possível carregar os dados para edição.")

    def cancel_edit(self):
        """Cancela o modo de edição e limpa os campos do formulário."""
        self.editing_iid = None
        self.btn_label.set("Adicionar")
        # opcional: limpar campos
        # self.nome_var.set("")
        # self.pot_var.set("")
        # self.qtd_var.set("1")
        # self.horas_var.set("1")
        # self.dias_var.set("30")

    def calcular(self):
        tarifa = parse_float(self.tarifa_var.get(), 0.0)
        bandeira = parse_float(self.bandeira_var.get(), 0.0)
        total_kwh = 0.0
        total_custo = 0.0
        for iid in self.tv.get_children():
            vals = self.tv.item(iid, "values")
            try:
                # Coluna 6 = kWh/mês
                kwh = float(str(vals[6]).replace(",", "."))
                custo = kwh * (tarifa + bandeira)
                total_kwh += kwh
                total_custo += custo
                self.tv.set(iid, "custo", fmt_moeda(custo))
            except Exception:
                pass
        self.total_kwh_var.set(f"{total_kwh:,.2f} kWh/mês".replace(",", "@").replace(".", ",").replace("@", "."))
        self.total_rs_var.set(fmt_moeda(total_custo))

    # ---------- Salvamento / Abertura de lista ----------
    def save_list(self):
        """Salva a lista em CSV (padrão ; como separador)."""
        if not self.tv.get_children():
            messagebox.showinfo("Salvar lista", "A lista está vazia.")
            return
        path = filedialog.asksaveasfilename(
            title="Salvar lista",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            initialfile="lista_consumo.csv"
        )
        if not path:
            return
        try:
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["nome","pot_w","qtd","horas_dia","dias_mes","wh_dia","kwh_mes","custo_rs"]) 
                for iid in self.tv.get_children():
                    vals = self.tv.item(iid, "values")
                    writer.writerow(list(vals))
            messagebox.showinfo("Salvar lista", "Lista salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    def load_list(self):
        """Abre uma lista CSV. Recalcula custo de acordo com a tarifa/bandeira atuais."""
        path = filedialog.askopenfilename(
            title="Abrir lista",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        if not path:
            return
        try:
            # Limpa itens atuais
            for iid in self.tv.get_children():
                self.tv.delete(iid)

            import csv
            # Detecta separador automaticamente
            with open(path, "r", encoding="utf-8") as f:
                sample = f.readline()
            delim = ';' if ';' in sample else ','

            tarifa = parse_float(self.tarifa_var.get(), 0.0)
            bandeira = parse_float(self.bandeira_var.get(), 0.0)

            with open(path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=delim)
                # Suporta arquivos com ou sem cabeçalho esperado
                for row in reader:
                    try:
                        nome = row.get('nome') or row.get('Nome') or ''
                        pot = parse_float(row.get('pot_w') or row.get('Potência (W)') or row.get('pot') or '0')
                        qtd = int(parse_float(row.get('qtd') or row.get('Qtd') or '1'))
                        horas = parse_float(row.get('horas_dia') or row.get('Horas/dia') or '0')
                        dias = int(parse_float(row.get('dias_mes') or row.get('Dias/mês') or '30'))
                        # Se o CSV já trouxer wh/kwh/custo, ignoramos e recalculamos
                        wh_dia = pot * horas * qtd
                        kwh_mes = (wh_dia * dias) / 1000.0
                        custo = kwh_mes * (tarifa + bandeira)
                        self.tv.insert("", tk.END, values=(
                            nome,
                            f"{pot:.0f}",
                            str(qtd),
                            f"{horas:.2f}",
                            str(dias),
                            f"{wh_dia:.1f}",
                            f"{kwh_mes:.3f}",
                            fmt_moeda(custo)
                        ))
                    except Exception:
                        continue
            # Atualiza totais
            self.calcular()
            messagebox.showinfo("Abrir lista", "Lista carregada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao abrir", str(e))

if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = App()
    app.mainloop()
