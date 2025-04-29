import time

class LogSystem:
    def __init__(self):
        self.log_widgets = {}  # Dictionary to store text widgets for each asset
        
    def add_log_widget(self, asset, text_widget):
        """Add a text widget for a specific asset"""
        self.log_widgets[asset] = text_widget
        
    def remove_log_widget(self, asset):
        """Remove a text widget for a specific asset"""
        if asset in self.log_widgets:
            del self.log_widgets[asset]
            
    def clear_log_widgets(self):
        """Clear all log widgets"""
        self.log_widgets.clear()

    def logar(self, mensagem, asset=None):
        """Log a message to a specific asset's widget or all widgets if asset is None"""
        hora = time.strftime("%H:%M:%S")
        texto_final = f"[{hora}] {mensagem}\n"

        if asset and asset in self.log_widgets:
            # Log to specific asset widget
            widget = self.log_widgets[asset]
            widget.insert('end', texto_final)
            widget.see('end')
        elif not asset:
            # Log to all widgets if no specific asset
            for widget in self.log_widgets.values():
                widget.insert('end', texto_final)
                widget.see('end')
