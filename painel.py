import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
from utils import obter_saldo
from estrategia import EstrategiaTrading
from log_system import LogSystem
import threading
import time
from datetime import datetime


class PainelApp:  # Changed from EnhancedPainelApp to PainelApp to match imports
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 Pro Trading")

        # Theme colors
        self.dark_theme = {
            'bg_dark': '#0A0A0A',  # Darker background
            'bg_medium': '#1E1E1E',  # Medium background
            'bg_light': '#2D2D2D',  # Light background
            'accent': '#00C853',  # Vibrant green
            'accent_hover': '#00E676',  # Lighter green
            'warning': '#FFB300',  # Warning color
            'danger': '#FF3D00',  # Danger color
            'text': '#FFFFFF',  # White text
            'text_secondary': '#B3B3B3'  # Gray text
        }

        self.light_theme = {
            'bg_dark': '#F5F5F5',  # Light gray background
            'bg_medium': '#FFFFFF',  # White background
            'bg_light': '#FAFAFA',  # Very light gray
            'accent': '#00C853',  # Keep green
            'accent_hover': '#00E676',  # Keep hover
            'warning': '#FFB300',  # Keep warning
            'danger': '#FF3D00',  # Keep danger
            'text': '#212121',  # Dark text
            'text_secondary': '#757575'  # Gray text
        }

        self.is_dark_mode = True
        self.colors = self.dark_theme

        self.root.configure(bg=self.colors['bg_dark'])
        self.root.resizable(False, False)
        self.centralizar_janela(1000, 700)

        # Initialize variables for multiple assets
        self.ativos_selecionados = [tk.StringVar() for _ in range(4)]
        self.timeframe_selecionado = tk.StringVar()
        self.lote_selecionado = tk.StringVar(value="0.10")
        self.operando = False
        self.estrategias = {}  # Dictionary to store strategy instances

        self.log_system = LogSystem()

        self.setup_styles()
        self.setup_ui()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Combobox style
        style.configure("Custom.TCombobox",
                        fieldbackground=self.colors['bg_light'],
                        background=self.colors['bg_light'],
                        foreground=self.colors['text'],
                        arrowcolor=self.colors['accent'],
                        selectbackground=self.colors['accent'],
                        selectforeground=self.colors['text'])

        # Update style on theme change
        self.root.bind('<<ThemeChanged>>', lambda e: self.update_styles())

    def update_styles(self):
        style = ttk.Style()
        style.configure("Custom.TCombobox",
                        fieldbackground=self.colors['bg_light'],
                        background=self.colors['bg_light'],
                        foreground=self.colors['text'],
                        arrowcolor=self.colors['accent'],
                        selectbackground=self.colors['accent'],
                        selectforeground=self.colors['text'])

    def setup_ui(self):
        # Theme switcher at the very top
        self.setup_theme_switcher(self.root)

        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'], padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        # Header
        self.setup_header(main_container)

        # Trading dashboard
        self.setup_dashboard(main_container)

        # Control panel
        self.setup_control_panel(main_container)

        # Enhanced log panel
        self.setup_log_panel(main_container)

        # Start data update threads
        self.start_update_threads()

    def setup_theme_switcher(self, parent):
        # Create a frame at the top of the window
        switcher_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        switcher_frame.pack(fill="x")

        # Add padding frame to position the button
        padding_frame = tk.Frame(switcher_frame, bg=self.colors['bg_dark'], height=10)
        padding_frame.pack(fill="x")

        # Create the theme toggle button with a more visible style
        self.theme_button = tk.Button(
            switcher_frame,
            text="☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro",
            command=self.toggle_theme,
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_light'],
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.theme_button.pack(side="right", padx=20, pady=5)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.colors = self.dark_theme if self.is_dark_mode else self.light_theme

        # Update theme button with animation effect
        self.theme_button.config(
            text="☀️ Modo Claro" if self.is_dark_mode else "🌙 Modo Escuro",
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        )

        # Create animation effect
        self.theme_button.config(relief="sunken")
        self.root.after(100, lambda: self.theme_button.config(relief="flat"))

        # Update all widgets
        self.update_theme()

        # Generate theme changed event
        self.root.event_generate('<<ThemeChanged>>')

    def update_theme(self):
        # Update root
        self.root.configure(bg=self.colors['bg_dark'])

        # Update all frames and widgets
        for widget in self.root.winfo_children():
            self.update_widget_colors(widget)

    def update_widget_colors(self, widget):
        widget_type = widget.winfo_class()

        if widget_type in ['Frame', 'Labelframe']:
            if widget.cget('bg') in [self.dark_theme['bg_dark'], self.light_theme['bg_dark']]:
                widget.configure(bg=self.colors['bg_dark'])
            elif widget.cget('bg') in [self.dark_theme['bg_medium'], self.light_theme['bg_medium']]:
                widget.configure(bg=self.colors['bg_medium'])
            elif widget.cget('bg') in [self.dark_theme['bg_light'], self.light_theme['bg_light']]:
                widget.configure(bg=self.colors['bg_light'])

        elif widget_type == 'Label':
            widget.configure(
                bg=widget.master.cget('bg'),
                fg=self.colors['text'] if widget.cget('fg') == self.dark_theme['text'] else self.colors[
                    'text_secondary']
            )

        elif widget_type == 'Button':
            if widget.cget('bg') == self.colors['accent']:
                # Don't change accent buttons
                pass
            else:
                widget.configure(
                    bg=self.colors['bg_light'],
                    fg=self.colors['text'],
                    activebackground=self.colors['accent_hover'],
                    activeforeground=self.colors['text']
                )

        elif widget_type == 'Text':
            widget.configure(
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                insertbackground=self.colors['text']
            )

        # Update children widgets
        for child in widget.winfo_children():
            self.update_widget_colors(child)

    def setup_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg_dark'])
        header.pack(fill="x", pady=(0, 20))

        # Logo and title container
        title_container = tk.Frame(header, bg=self.colors['bg_dark'])
        title_container.pack(side="left")

        logo_label = tk.Label(
            title_container,
            text="📈",
            font=("Helvetica", 32),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        logo_label.pack(side="left", padx=(0, 10))

        title_label = tk.Label(
            title_container,
            text="FUTURE MT5 PRO",
            font=("Helvetica", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        )
        title_label.pack(side="left")

        # Balance display
        self.saldo_frame = tk.Frame(header, bg=self.colors['bg_light'], padx=15, pady=10)
        self.saldo_frame.pack(side="right")

        tk.Label(
            self.saldo_frame,
            text="SALDO",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack()

        self.saldo_label = tk.Label(
            self.saldo_frame,
            text="R$ 0.00",
            font=("Helvetica", 18, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        )
        self.saldo_label.pack()

    def setup_dashboard(self, parent):
        dashboard = tk.Frame(parent, bg=self.colors['bg_medium'], padx=20, pady=20)
        dashboard.pack(fill="x", pady=(0, 20))

        # Asset selection container
        assets_frame = tk.Frame(dashboard, bg=self.colors['bg_medium'])
        assets_frame.pack(fill="x", pady=(0, 20))

        # Create 4 asset selection frames
        for i in range(4):
            asset_frame = self.create_asset_frame(assets_frame, f"ATIVO {i+1}", i)
            asset_frame.pack(side="left", padx=10, fill="x", expand=True)

        # Settings container
        settings_frame = tk.Frame(dashboard, bg=self.colors['bg_medium'])
        settings_frame.pack(fill="x")

        # Timeframe selection
        timeframe_frame = self.create_input_group(settings_frame, "TIMEFRAME")
        self.combo_timeframe = ttk.Combobox(
            timeframe_frame,
            textvariable=self.timeframe_selecionado,
            values=["M1", "M5", "M15", "M30", "H1", "H4", "D1"],
            style="Custom.TCombobox",
            width=25
        )
        self.combo_timeframe.pack(fill="x")
        self.combo_timeframe.current(1)

        # Lot size input
        lot_frame = self.create_input_group(settings_frame, "LOTE")
        self.entry_lote = tk.Entry(
            lot_frame,
            textvariable=self.lote_selecionado,
            font=("Helvetica", 12),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief="flat",
            width=25
        )
        self.entry_lote.pack(fill="x")

        # Organize frames horizontally
        asset_frame.pack(side="left", padx=(0, 10))
        timeframe_frame.pack(side="left", padx=10)
        lot_frame.pack(side="left", padx=(10, 0))

    def create_input_group(self, parent, label):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])

        tk.Label(
            frame,
            text=label,
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(anchor="w", pady=(0, 5))

        return frame

    def setup_control_panel(self, parent):
        control_panel = tk.Frame(parent, bg=self.colors['bg_medium'], padx=20, pady=20)
        control_panel.pack(fill="x", pady=(0, 20))

        # Status indicator
        self.status_label = tk.Label(
            control_panel,
            text="⭘ AGUARDANDO",
            font=("Helvetica", 12, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        )
        self.status_label.pack(side="left")

        # Control buttons
        buttons_frame = tk.Frame(control_panel, bg=self.colors['bg_medium'])
        buttons_frame.pack(side="right")

        self.btn_atualizar = self.create_button(
            buttons_frame,
            "🔄 Atualizar",
            self.carregar_ativos,
            self.colors['bg_light']
        )
        self.btn_atualizar.pack(side="left", padx=(0, 10))

        self.btn_iniciar = self.create_button(
            buttons_frame,
            "▶ Iniciar Robô",
            self.iniciar_robô,
            self.colors['accent']
        )
        self.btn_iniciar.pack(side="left", padx=(0, 10))

        self.btn_parar = self.create_button(
            buttons_frame,
            "⏹ Parar",
            self.parar_robô,
            self.colors['danger']
        )
        self.btn_parar.pack(side="left")

    def create_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=color,
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )

    def setup_log_panel(self, parent):
        log_container = tk.Frame(parent, bg=self.colors['bg_medium'], padx=20, pady=20)
        log_container.pack(fill="both", expand=True)

        # Create 2x2 grid for logs
        for i in range(2):
            for j in range(2):
                index = i * 2 + j
                self.create_log_section(log_container, f"ATIVO {index + 1}", i, j)

        # Configure grid weights
        log_container.grid_columnconfigure(0, weight=1)
        log_container.grid_columnconfigure(1, weight=1)
        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_rowconfigure(1, weight=1)

    def create_log_section(self, parent, title, row, col):
        # Section frame
        section = tk.Frame(parent, bg=self.colors['bg_medium'])
        section.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Header
        header = tk.Frame(section, bg=self.colors['bg_medium'])
        header.pack(fill="x", pady=(0, 5))

        tk.Label(
            header,
            text=title,
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(side="left")

        # Log text area
        text_log = tk.Text(
            section,
            height=10,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief="flat",
            font=("Consolas", 9),
            padx=10,
            pady=10
        )
        text_log.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(section, command=text_log.yview)
        scrollbar.pack(side="right", fill="y")
        text_log.config(yscrollcommand=scrollbar.set)

        # Add text widget to log system
        self.log_system.add_log_widget(title, text_log)

    def start_update_threads(self):
        # Update balance
        threading.Thread(target=self.atualizar_saldo_loop, daemon=True).start()
        # Update time
        threading.Thread(target=self.atualizar_hora_loop, daemon=True).start()
        # Load initial assets
        self.carregar_ativos()

    def atualizar_hora_loop(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
            time.sleep(1)

    def atualizar_saldo_loop(self):
        while True:
            saldo = obter_saldo()
            self.saldo_label.config(text=f"R$ {saldo:.2f}")
            time.sleep(5)

    def carregar_ativos(self):
        try:
            symbols = mt5.symbols_get()
            lista_ativos = [symbol.name for symbol in symbols if symbol.visible]
            
            # Update all asset comboboxes
            for i, ativo_var in enumerate(self.ativos_selecionados):
                combo = self.root.nametowidget(ativo_var.master)
                combo['values'] = lista_ativos
            
            self.log_system.logar("✅ Lista de ativos atualizada com sucesso!")
        except Exception as e:
            self.log_system.logar(f"❌ Erro ao carregar ativos: {e}")

    def verificar_campos(self, *args):
        ativos = [ativo.get().strip() for ativo in self.ativos_selecionados]
        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()
        
        # Check if all fields are filled and all assets are different
        if all(ativos) and len(set(ativos)) == 4 and timeframe and lote:
            self.btn_iniciar.config(state="normal")
        else:
            self.btn_iniciar.config(state="disabled")

    def iniciar_robô(self):
        # Validate selections
        ativos = [ativo.get().strip() for ativo in self.ativos_selecionados]
        if len(set(ativos)) != 4 or "" in ativos:
            self.log_system.logar("⚠️ Selecione 4 ativos diferentes!")
            return

        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()
        if not timeframe:
            self.log_system.logar("⚠️ Selecione um timeframe para operar!")
            return
        if not lote:
            self.lote_selecionado.set("0.10")
            lote = "0.10"
            self.log_system.logar("⚠️ Lote vazio. Valor padrão 0.10 atribuído.")

        try:
            lote_float = round(float(lote), 2)
            if lote_float <= 0:
                self.log_system.logar("⚠️ O lote deve ser maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro de Lote", "Valor de lote inválido! Informe um número válido como 0.10")
            self.log_system.logar("❌ Erro: Lote inválido informado.")
            return

        # Start strategies for each asset
        for i, ativo in enumerate(ativos):
            if self.validar_ativo(ativo):
                estrategia = EstrategiaTrading(ativo, timeframe, lote_float, self.log_system)
                self.estrategias[ativo] = estrategia
                threading.Thread(target=estrategia.executar, daemon=True).start()
                self.log_system.logar(f"✅ Iniciando análise para {ativo}", f"ATIVO {i + 1}")

        self.operando = True
        self.status_label.config(text="● OPERANDO", fg=self.colors['accent'])

    def validar_ativo(self, ativo):
        info = mt5.symbol_info(ativo)
        if info is None:
            self.log_system.logar(f"❌ Ativo {ativo} não encontrado no MetaTrader 5.")
            return False
        if not info.visible:
            self.log_system.logar(f"⚠️ Ativo {ativo} não está visível no MT5. Abra o ativo no terminal!")
            return False
        if info.trade_mode != mt5.SYMBOL_TRADE_MODE_FULL:
            self.log_system.logar(f"❌ Ativo {ativo} não está liberado para operar (modo inválido)!")
            return False

        tick = mt5.symbol_info_tick(ativo)
        if tick is None:
            self.log_system.logar(f"❌ Não foi possível obter preços do ativo {ativo}.")
            return False

        spread = (tick.ask - tick.bid) / info.point
        spread_maximo_aceito = 50

        if spread > spread_maximo_aceito:
            self.log_system.logar(f"⚠️ Spread do ativo {ativo} está muito alto ({spread:.1f} pontos).")
            return False

        if tick.bid == 0 or tick.ask == 0:
            self.log_system.logar(f"⚠️ Mercado para o ativo {ativo} está FECHADO.")
            return False

        self.log_system.logar(f"✅ Mercado para o ativo {ativo} está ABERTO.")
        return True

    def parar_robô(self):
        self.operando = False
        self.status_label.config(text="⭘ AGUARDANDO", fg=self.colors['text_secondary'])
        
        # Stop all strategies
        for ativo, estrategia in self.estrategias.items():
            estrategia.parar()
            self.log_system.logar(f"🛑 Análise parada para {ativo}")
        
        self.estrategias.clear()
        self.log_system.logar("✅ Todas as análises foram encerradas")


if __name__ == "__main__":
    root = tk.Tk()
    app = PainelApp(root)
    root.mainloop()