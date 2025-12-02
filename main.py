# ENTRY POINT

import tkinter as tk
from app import PaketFlowMonitor

if __name__ == "__main__":
    root = tk.Tk()
    app = PaketFlowMonitor(root)
    root.mainloop()