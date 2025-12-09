import tkinter as tk
from tkinter import ttk
from utils.theme import COLORS, FONTS, DIMENSIONS

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=45, 
                 bg_color=COLORS["primary"], text_color=COLORS["primary_text"], 
                 hover_color=COLORS["primary_hover"], border_color=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=kwargs.get('bg', COLORS["background_card"]), 
                         highlightthickness=0, bd=0)
        
        self.command = command
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color
        self.border_color = border_color
        
        self.width = width
        self.height = height
        self.radius = DIMENSIONS["border_radius"]
        
        self.normal_state()
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

    def round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def normal_state(self):
        self.delete("all")
        # Draw background
        if self.border_color:
            # Draw border stroke (slightly larger rect behind or use outline logic if polygon supports it well, 
            # but polygon outline drawing can be jagged. Better to fill.)
            # For simplicity in this mockup, we'll use outline parameter of create_polygon if border_color is set
            self.round_rect(2, 2, self.width-2, self.height-2, radius=self.radius, 
                           fill=self.bg_color, outline=self.border_color, width=2)
        else:
            self.round_rect(0, 0, self.width, self.height, radius=self.radius, fill=self.bg_color)
            
        # Draw text
        self.create_text(self.width/2, self.height/2, text=self.text, 
                         fill=self.text_color, font=FONTS["body_bold"])

    def hover_state(self):
        self.delete("all")
        if self.border_color:
             self.round_rect(2, 2, self.width-2, self.height-2, radius=self.radius, 
                           fill=self.bg_color, outline=self.hover_color, width=2)
             # Change text color to hover color if it's an outlined button (usually)
             # assuming outlined button has transparent/white bg and colored text/border
             text_col = self.hover_color if self.bg_color == COLORS["background_card"] else self.text_color
             self.create_text(self.width/2, self.height/2, text=self.text, 
                         fill=text_col, font=FONTS["body_bold"])
        else:
            self.round_rect(0, 0, self.width, self.height, radius=self.radius, fill=self.hover_color)
            self.create_text(self.width/2, self.height/2, text=self.text, 
                            fill=self.text_color, font=FONTS["body_bold"])

    def on_enter(self, event):
        self.configure(cursor="hand2")
        self.hover_state()

    def on_leave(self, event):
        self.configure(cursor="")
        self.normal_state()

    def on_click(self, event):
        # click effect (shrink slightly or darken?)
        pass

    def on_release(self, event):
        if self.command:
            self.command()


class RoundedEntry(tk.Frame):
    def __init__(self, parent, width=300, height=40, placeholder="", show=None, icon=None, **kwargs):
        bg_color = kwargs.get('bg', COLORS["background_card"])
        super().__init__(parent, width=width, height=height, bg=bg_color)
        
        self.width = width
        self.height = height
        self.radius = DIMENSIONS["border_radius"]
        self.placeholder = placeholder
        self.show_char = show
        self.icon_char = icon
        
        # Internal Canvas for drawing
        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg_color, 
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.entry_var = tk.StringVar()
        
        self.draw_border(COLORS["border"])
        
        # Icono (Leading)
        self.padding_left = 15
        if self.icon_char:
            self.canvas.create_text(20, height/2, text=self.icon_char, fill=COLORS["text_secondary"], font=("Segoe UI Symbol", 12))
            self.padding_left = 40
            
        # Eye icon for password (Trailing) - Use a real Button instead of canvas text
        self.eye_padding_right = 15  # Default padding
        if self.show_char == "*":
            self.eye_visible = False
            self.eye_padding_right = 50  # More space for eye icon
            
            # Create a Button widget for the eye icon instead of canvas text
            eye_x = width - 25
            eye_y = height / 2
            
            self.eye_button = tk.Button(
                self.canvas,
                text="👁",
                font=("Segoe UI Symbol", 12),
                fg=COLORS["text_secondary"],
                bg=COLORS["background_card"],
                bd=0,
                relief=tk.FLAT,
                cursor="hand2",
                activebackground=COLORS["background_card"],
                command=self.toggle_password_click
            )
            # Place the button on the canvas
            self.canvas.create_window(eye_x, eye_y, window=self.eye_button, anchor="center")
        
        # Entry Widget real (child of canvas to clip correctly if window)
        # Note: using canvas.create_window places it "inside" the canvas layout
        self.entry = tk.Entry(self.canvas, textvariable=self.entry_var, font=FONTS["body"], 
                              bd=0, highlightthickness=0, bg=COLORS["background_card"], fg=COLORS["text_primary"])
        
        if self.show_char:
            self.entry.config(show=self.show_char)
            
        # Bind events for focus
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Place entry on top of canvas using create_window - adjusted width to not cover eye icon
        entry_width = width - self.padding_left - self.eye_padding_right
        self.entry_window = self.canvas.create_window(self.padding_left, height/2, window=self.entry, anchor="w", width=entry_width)

    def draw_border(self, color):
        self.canvas.delete("border")
        self.round_rect(1, 1, self.width-1, self.height-1, radius=self.radius, outline=color, width=1, tag="border")

    def round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        outline = kwargs.pop("outline", "black")
        return self.canvas.create_polygon(points, **kwargs, smooth=True, fill="", outline=outline)

    def on_focus_in(self, event):
        self.draw_border(COLORS["border_focus"])

    def on_focus_out(self, event):
        self.draw_border(COLORS["border"])

    def toggle_password(self, event):
        self.eye_visible = not self.eye_visible
        print(f"Toggle password - eye_visible: {self.eye_visible}")  # Debug
        if self.eye_visible:
            self.entry.config(show="")
            self.canvas.itemconfigure(self.eye_btn, fill=COLORS["primary"])
        else:
            self.entry.config(show="*")
            self.canvas.itemconfigure(self.eye_btn, fill=COLORS["text_secondary"])
    
    def toggle_password_click(self):
        """Toggle password visibility - Button command version"""
        self.eye_visible = not self.eye_visible
        if self.eye_visible:
            self.entry.config(show="")
            self.eye_button.config(fg=COLORS["primary"])
        else:
            self.entry.config(show="*")
            self.eye_button.config(fg=COLORS["text_secondary"])

    def get(self):
        return self.entry.get()
        
    def insert(self, index, string):
        return self.entry.insert(index, string)
        
    def delete(self, first, last=None):
        return self.entry.delete(first, last)
        
    def config(self, **kwargs):
        # Intercept state config to update background/border if disabled
        if 'state' in kwargs:
            state = kwargs['state']
            if state == 'disabled':
                self.canvas.configure(bg="#F5F5F5") 
                self.entry.config(bg="#F5F5F5")
            else:
                self.canvas.configure(bg=COLORS["background_card"])
                self.entry.config(bg=COLORS["background_card"])
                
        return self.entry.config(**kwargs)
