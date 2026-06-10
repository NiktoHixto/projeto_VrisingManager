import customtkinter as ctk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None

        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow:
            return

        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25

        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(tw, text=self.text, justify="left", fg_color="#222222", corner_radius=8)
        label.pack(padx=5, pady=5)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
