import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

def calculate_growth(principal, monthly_savings, annual_rate, years):
    """Berechnet das jährliche Wachstum mit Zinseszins."""
    balance = []
    total = principal
    for year in range(1, years + 1):
        total = total * (1 + annual_rate / 100) + monthly_savings * 12
        balance.append(total)
    return balance

def find_intersections(y1, y2):
    """Finde Schnittpunkte zweier Kurven."""
    intersections = []
    for i in range(len(y1)):
        if i > 0:
            # Prüfen ob die Kurven zwischen den Jahren geschnitten werden
            if (y1[i-1] - y2[i-1]) * (y1[i] - y2[i]) < 0:
                intersections.append(i)
    return intersections

def plot_graph():
    try:
        # Werte aus den Eingabefeldern auslesen
        p1 = float(s1_principal.get())
        m1 = float(s1_monthly.get())
        r1 = float(s1_rate.get())
        y1 = int(s1_years.get())

        p2 = float(s2_principal.get())
        m2 = float(s2_monthly.get())
        r2 = float(s2_rate.get())
        y2 = int(s2_years.get())

        years = max(y1, y2)

        # Zinseszinsberechnung
        growth1 = calculate_growth(p1, m1, r1, years)
        growth2 = calculate_growth(p2, m2, r2, years)

        # Plot vorbereiten
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(range(1, years+1), growth1, label="Szenario 1", marker='o')
        ax.plot(range(1, years+1), growth2, label="Szenario 2", marker='s')

        # Schnittpunkte markieren
        intersections = find_intersections(growth1, growth2)
        for i in intersections:
            ax.plot(i+1, growth1[i], 'ro')
            ax.annotate(f'Schnittpunkt\nJahr {i+1}', xy=(i+1, growth1[i]), xytext=(i+1, growth1[i]*1.05),
                        arrowprops=dict(facecolor='red', arrowstyle='->'))

        ax.set_xlabel("Jahre")
        ax.set_ylabel("Kapital (€)")
        ax.set_title("Zinseszinsrechner")
        ax.legend()
        ax.grid(True)

        # Canvas aktualisieren
        for widget in plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Toolbar für Zoom und Pan
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Button zum Speichern der Grafik
        save_btn = ttk.Button(plot_frame, text="Grafik herunterladen", command=lambda: save_plot(fig))
        save_btn.pack(pady=5)

    except ValueError:
        messagebox.showerror("Fehler", "Bitte alle Felder korrekt ausfüllen.")

def save_plot(fig):
    """Speichert die aktuelle Grafik als PNG."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Dateien", "*.png")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Erfolg", f"Grafik gespeichert unter:\n{file_path}")

# Hauptfenster
root = tk.Tk()
root.title("Zinseszinsrechner mit zwei Szenarien")
root.geometry("900x700")

# Frames für Szenario 1 und 2
s1_frame = ttk.LabelFrame(root, text="Szenario 1")
s1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

s2_frame = ttk.LabelFrame(root, text="Szenario 2")
s2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

plot_frame = ttk.LabelFrame(root, text="Grafik")
plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Eingabefelder Szenario 1
s1_principal = tk.StringVar()
s1_monthly = tk.StringVar()
s1_rate = tk.StringVar()
s1_years = tk.StringVar()

ttk.Label(s1_frame, text="Anfangskapital (€)").pack()
ttk.Entry(s1_frame, textvariable=s1_principal).pack()

ttk.Label(s1_frame, text="Monatliche Sparrate (€)").pack()
ttk.Entry(s1_frame, textvariable=s1_monthly).pack()

ttk.Label(s1_frame, text="Jährlicher Zinssatz (%)").pack()
ttk.Entry(s1_frame, textvariable=s1_rate).pack()

ttk.Label(s1_frame, text="Ansparzeit (Jahre)").pack()
ttk.Entry(s1_frame, textvariable=s1_years).pack()

# Eingabefelder Szenario 2
s2_principal = tk.StringVar()
s2_monthly = tk.StringVar()
s2_rate = tk.StringVar()
s2_years = tk.StringVar()

ttk.Label(s2_frame, text="Anfangskapital (€)").pack()
ttk.Entry(s2_frame, textvariable=s2_principal).pack()

ttk.Label(s2_frame, text="Monatliche Sparrate (€)").pack()
ttk.Entry(s2_frame, textvariable=s2_monthly).pack()

ttk.Label(s2_frame, text="Jährlicher Zinssatz (%)").pack()
ttk.Entry(s2_frame, textvariable=s2_rate).pack()

ttk.Label(s2_frame, text="Ansparzeit (Jahre)").pack()
ttk.Entry(s2_frame, textvariable=s2_years).pack()

# Button zum Berechnen
ttk.Button(root, text="Berechnen", command=plot_graph).pack(pady=10)

root.mainloop()



# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# """
# Zinseszins-Rechner mit Zwei Szenarien (Tkinter + Matplotlib)

# Funktion:
# - Zwei getrennte Szenarien mit Eingabefeldern:
#   Anfangskapital, monatliche Sparrate, jährlicher Zinssatz (%), Ansparzeit (Jahre),
#   optional gewünschtes Endkapital.
# - Berechnung: monatliche & jährliche Verzinsung, Entwicklung über Zeit.
# - Falls Endkapital vorgegeben: Berechnung erforderlicher monatlicher Sparrate.
# - Visualisierung beider Szenarien in einem gemeinsamen Diagramm (Matplotlib).
# - Export der Zeitreihen als CSV, Reset-Funktion.
# - Robuste Eingabevalidierung und Fehlerbehandlung.
# """

# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# import math
# import csv
# from dataclasses import dataclass
# from typing import List, Tuple, Optional

# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np

# # ---------- Hilfsfunktionen / Finanzformeln ----------

# def fv_monthly_compound(P: float, monthly: float, r_annual_pct: float, years: float) -> float:
#     """Endkapital bei monatlicher Verzinsung mit monatlichen Einzahlungen."""
#     n = 12
#     r = r_annual_pct / 100.0
#     periods = n * years
#     if r == 0:
#         return P + monthly * periods
#     monthly_rate = r / n
#     fv_principal = P * (1 + monthly_rate) ** periods
#     fv_rentes = monthly * (((1 + monthly_rate) ** periods - 1) / monthly_rate)
#     return fv_principal + fv_rentes

# def fv_annual_compound(P: float, annual_contribution: float, r_annual_pct: float, years: float) -> float:
#     """Endkapital bei jährlicher Verzinsung mit jährlichen Einzahlungen."""
#     r = r_annual_pct / 100.0
#     t = int(math.floor(years))
#     leftover = years - t
#     if r == 0:
#         return P + annual_contribution * years
#     fv = P * (1 + r) ** years
#     if t == 0:
#         fv += annual_contribution * years
#     else:
#         fv += annual_contribution * (((1 + r) ** years - 1) / r)
#     return fv

# def required_monthly_for_target(P: float, r_annual_pct: float, years: float, target_FV: float) -> Optional[float]:
#     """Berechnet die benötigte monatliche Sparrate für ein Zielkapital."""
#     n = 12
#     r = r_annual_pct / 100.0
#     periods = n * years
#     if periods <= 0:
#         return None
#     if r == 0:
#         return (target_FV - P) / periods
#     monthly_rate = r / n
#     factor = (1 + monthly_rate) ** periods
#     denom = (factor - 1) / monthly_rate
#     if denom == 0:
#         return None
#     return (target_FV - P * factor) / denom

# def timeseries_monthly(P: float, monthly: float, r_annual_pct: float, years: float):
#     """Zeitreihe monatlicher Vermögensentwicklung."""
#     n = 12
#     r = r_annual_pct / 100.0
#     total_months = int(round(years * n))
#     times = np.linspace(0, years, total_months + 1)
#     balances = np.zeros_like(times)
#     monthly_rate = r / n
#     bal = P
#     balances[0] = bal
#     for i in range(1, total_months + 1):
#         bal = bal * (1 + monthly_rate)
#         bal += monthly
#         balances[i] = bal
#     return times, balances

# def timeseries_annual(P: float, monthly: float, r_annual_pct: float, years: float):
#     """Zeitreihe jährlicher Vermögensentwicklung."""
#     annual_contrib = monthly * 12.0
#     total_years = int(math.ceil(years))
#     times = np.linspace(0, years, total_years + 1)
#     balances = np.zeros_like(times)
#     r = r_annual_pct / 100.0
#     bal = P
#     balances[0] = bal
#     for y in range(1, len(times)):
#         delta = times[y] - times[y - 1]
#         bal = bal * (1 + r) ** delta
#         bal += annual_contrib * delta
#         balances[y] = bal
#     return times, balances

# # ---------- GUI App Definition ----------

# @dataclass
# class ScenarioInput:
#     principal: float = 0.0
#     monthly: float = 0.0
#     annual_rate_pct: float = 0.0
#     years: float = 0.0
#     target: Optional[float] = None

# class ZinseszinsApp:
#     def __init__(self, root: tk.Tk):
#         self.root = root
#         self.root.title("Zinseszins-Rechner - 2 Szenarien")
#         self.root.geometry("1100x720")
#         self._build_ui()

#     def _build_ui(self):
#         mainframe = ttk.Frame(self.root, padding=(10, 10, 10, 10))
#         mainframe.pack(fill=tk.BOTH, expand=True)

#         input_frame = ttk.Frame(mainframe)
#         input_frame.pack(side=tk.TOP, fill=tk.X)

#         self.scenario_frames = []
#         self.entries = []

#         for i in range(2):
#             frame = ttk.LabelFrame(input_frame, text=f"Szenario {i+1}", padding=(10, 10))
#             frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
#             self.scenario_frames.append(frame)
#             ent = self._build_scenario_inputs(frame)
#             self.entries.append(ent)

#         control_frame = ttk.Frame(mainframe)
#         control_frame.pack(fill=tk.X, pady=(0, 10))

#         ttk.Button(control_frame, text="Berechnen", command=self.on_calculate).pack(side=tk.LEFT, padx=5)
#         ttk.Button(control_frame, text="Zurücksetzen", command=self.on_reset).pack(side=tk.LEFT, padx=5)
#         ttk.Button(control_frame, text="Exportieren (CSV)", command=self.on_export).pack(side=tk.LEFT, padx=5)

#         result_frame = ttk.Frame(mainframe)
#         result_frame.pack(fill=tk.X, pady=(5, 10))
#         self.result_text = tk.Text(result_frame, height=6, wrap=tk.WORD)
#         self.result_text.pack(fill=tk.BOTH, expand=True)
#         self.result_text.insert(tk.END, "Bitte Eingaben tätigen und 'Berechnen' klicken.\n")
#         self.result_text.config(state=tk.DISABLED)

#         fig_frame = ttk.Frame(mainframe)
#         fig_frame.pack(fill=tk.BOTH, expand=True)

#         self.fig = Figure(figsize=(8, 5), dpi=100)
#         self.ax = self.fig.add_subplot(111)
#         self.ax.set_xlabel("Jahre")
#         self.ax.set_ylabel("Kapital")
#         self.ax.set_title("Vermögensentwicklung - beide Szenarien")
#         self.ax.grid(True)

#         self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
#         self.canvas_widget = self.canvas.get_tk_widget()
#         self.canvas_widget.pack(fill=tk.BOTH, expand=True)

#         self._set_default_values()

#     def _build_scenario_inputs(self, parent):
#         labels = {
#             "principal": "Anfangskapital (€):",
#             "monthly": "Monatliche Sparrate (€):",
#             "annual_rate": "Jährlicher Zinssatz (%):",
#             "years": "Ansparzeit (Jahre):",
#             "target": "Gewünschtes Endkapital (optional €):"
#         }
#         entries = {}
#         for key, text in labels.items():
#             row = ttk.Frame(parent)
#             row.pack(fill=tk.X, pady=4)
#             ttk.Label(row, text=text, width=28, anchor=tk.W).pack(side=tk.LEFT)
#             ent = ttk.Entry(row)
#             ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
#             entries[key] = ent
#         ttk.Label(parent, text="Hinweis: Komma oder Punkt als Dezimaltrenner möglich.", foreground="gray").pack(anchor=tk.W)
#         return entries

#     def _set_default_values(self):
#         defaults = [
#             {"principal": "10000", "monthly": "200", "annual_rate": "5", "years": "20", "target": ""},
#             {"principal": "5000", "monthly": "300", "annual_rate": "6", "years": "15", "target": ""}
#         ]
#         for ent, d in zip(self.entries, defaults):
#             for k, v in d.items():
#                 ent[k].delete(0, tk.END)
#                 ent[k].insert(0, v)

#     # --- BUTTONS ---

#     def on_reset(self):
#         for ent in self.entries:
#             for widget in ent.values():
#                 widget.delete(0, tk.END)
#         self._set_default_values()
#         self._clear_results()
#         self.ax.clear()
#         self.ax.set_xlabel("Jahre")
#         self.ax.set_ylabel("Kapital")
#         self.ax.set_title("Vermögensentwicklung - beide Szenarien")
#         self.ax.grid(True)
#         self.canvas.draw()

#     def _clear_results(self):
#         self.result_text.config(state=tk.NORMAL)
#         self.result_text.delete(1.0, tk.END)
#         self.result_text.config(state=tk.DISABLED)

#     def on_export(self):
#         filename = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV-Datei", "*.csv"), ("Alle Dateien", "*.*")],
#             title="Zeitreihen als CSV speichern"
#         )
#         if not filename:
#             return
#         if not hasattr(self, "export_data"):
#             messagebox.showinfo("Export", "Keine Daten zum Exportieren.")
#             return
#         try:
#             with open(filename, "w", newline="", encoding="utf-8") as f:
#                 writer = csv.writer(f, delimiter=";")
#                 times = self.export_data["times"]
#                 writer.writerow([
#                     "Jahr",
#                     "Szenario 1 (monatlich)", "Szenario 1 (jährlich)",
#                     "Szenario 2 (monatlich)", "Szenario 2 (jährlich)"
#                 ])
#                 m1, m2 = self.export_data["monthly_vals"]
#                 a1, a2 = self.export_data["annual_vals"]
#                 for i in range(len(times)):
#                     row = [
#                         f"{times[i]:.4f}",
#                         f"{m1[i]:.2f}", f"{a1[i]:.2f}",
#                         f"{m2[i]:.2f}", f"{a2[i]:.2f}",
#                     ]
#                     writer.writerow(row)
#             messagebox.showinfo("Export", "Export erfolgreich!")
#         except Exception as e:
#             messagebox.showerror("Fehler", str(e))

#     def on_calculate(self):
#         scenarios = []
#         for idx, ent in enumerate(self.entries):
#             try:
#                 principal = self._parse_float(ent["principal"].get())
#                 monthly = self._parse_float(ent["monthly"].get())
#                 annual_rate = self._parse_float(ent["annual_rate"].get())
#                 years = self._parse_float(ent["years"].get())
#                 target_str = ent["target"].get().strip()
#                 target = self._parse_float(target_str) if target_str else None

#                 if years <= 0:
#                     raise ValueError("Ansparzeit muss > 0 sein.")
#                 scenarios.append(ScenarioInput(principal, monthly, annual_rate, years, target))
#             except Exception as e:
#                 messagebox.showerror("Eingabefehler", f"Szenario {idx+1}: {e}")
#                 return

#         results_text = []
#         self.ax.clear()
#         self.ax.set_xlabel("Jahre")
#         self.ax.set_ylabel("Kapital (€)")
#         self.ax.set_title("Vermögensentwicklung - beide Szenarien")
#         self.ax.grid(True)

#         max_years = max(s.years for s in scenarios)
#         n = 12
#         total_months = int(round(max_years * n))
#         common_times = np.linspace(0, max_years, total_months + 1)

#         monthly_vals_all = []
#         annual_vals_all = []
#         colors = ["tab:blue", "tab:orange"]

#         for idx, sc in enumerate(scenarios):
#             monthly_used = sc.monthly
#             note = ""
#             if sc.target is not None and sc.target > 0:
#                 req = required_monthly_for_target(sc.principal, sc.annual_rate_pct, sc.years, sc.target)
#                 if req is not None:
#                     monthly_used = req
#                     note = f" (benötigte Sparrate: {req:.2f} €)"

#             fv_m = fv_monthly_compound(sc.principal, monthly_used, sc.annual_rate_pct, sc.years)
#             fv_a = fv_annual_compound(sc.principal, monthly_used, sc.annual_rate_pct, sc.years)

#             results_text.append(
#                 f"Szenario {idx+1}:\n"
#                 f"  Anfangskapital: {sc.principal:.2f} €\n"
#                 f"  Monatliche Sparrate: {monthly_used:.2f} €{note}\n"
#                 f"  Zinssatz p.a.: {sc.annual_rate_pct:.2f} %\n"
#                 f"  Ansparzeit: {sc.years:.2f} Jahre\n"
#                 f"  Endkapital (monatliche Verzinsung): {fv_m:.2f} €\n"
#                 f"  Endkapital (jährliche Verzinsung): {fv_a:.2f} €\n"
#             )

#             t_m, v_m = timeseries_monthly(sc.principal, monthly_used, sc.annual_rate_pct, sc.years)
#             t_a, v_a = timeseries_annual(sc.principal, monthly_used, sc.annual_rate_pct, sc.years)

#             common_m = np.interp(common_times, t_m, v_m)
#             common_a = np.interp(common_times, t_a, v_a)

#             monthly_vals_all.append(common_m)
#             annual_vals_all.append(common_a)

#             color = colors[idx]
#             self.ax.plot(common_times, common_m, color=color, linewidth=2,
#                          label=f"Szenario {idx+1} monatlich")
#             self.ax.plot(common_times, common_a, color=color, linestyle="--", linewidth=1.5,
#                          label=f"Szenario {idx+1} jährlich")

#         self.ax.legend()
#         self.canvas.draw()

#         self.result_text.config(state=tk.NORMAL)
#         self.result_text.delete(1.0, tk.END)
#         self.result_text.insert(tk.END, "\n\n".join(results_text))
#         self.result_text.config(state=tk.DISABLED)

#         self.export_data = {
#             "times": common_times,
#             "monthly_vals": monthly_vals_all,
#             "annual_vals": annual_vals_all
#         }

#     @staticmethod
#     def _parse_float(s: str) -> float:
#         s = s.strip().replace(",", ".")
#         if s == "":
#             raise ValueError("Feld darf nicht leer sein.")
#         return float(s)


# def main():
#     root = tk.Tk()
#     app = ZinseszinsApp(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()
