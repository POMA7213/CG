import tkinter as tk
from tkinter import colorchooser
import colorsys
from tkinter import Scale, StringVar


def cmyk2rgb(c, m, y, k):
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b


def rgb2cmyk(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        c = m = y = 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    return c, m, y, k


def rgb2hls(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = round(h * 360)
    l = round(l * 100)
    s = round(s * 100)
    return h, l, s


def hls2rgb(h, l, s):
    h = h / 360
    l = l / 100
    s = s / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r = round(r * 255)
    g = round(g * 255)
    b = round(b * 255)
    return r, g, b


def hex2rgb(color):
    color = color.lstrip('#')
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Colors")

        self.cmyk_labels = []
        self.rgb_labels = []
        self.hls_labels = []

        self.input_type_var = StringVar()
        self.input_sliders = []

        self.create_color_inputs()
        self.create_color_labels()

        self.root.mainloop()

    def create_color_inputs(self):
        input_type_frame = tk.Frame(self.root)
        input_type_frame.pack()
        input_type_label = tk.Label(input_type_frame, text="Input Type")
        input_type_label.grid(row=0, column=0)
        input_type_dropdown = tk.OptionMenu(input_type_frame, self.input_type_var, "CMYK", "RGB", "HLS",
                                            command=self.update_input_type)
        input_type_dropdown.grid(row=0, column=1)

        slider_frame = tk.Frame(self.root)
        slider_frame.pack(side=tk.LEFT)

        for i in range(4):
            self.input_sliders.append(Scale(slider_frame, from_=0, to=255, length=256, orient=tk.HORIZONTAL,
                                            command=self.update_slider_value))
            self.input_sliders[i].pack()

    def create_color_labels(self):
        labels_frame = tk.Frame(self.root)
        labels_frame.pack(side=tk.BOTTOM)

        cmyk_frame = tk.Frame(labels_frame)
        cmyk_frame.grid(row=0, column=0, padx=10)
        cmyk_label = tk.Label(cmyk_frame, text="CMYK:")
        cmyk_label.pack()
        for i in range(4):
            label = tk.Label(cmyk_frame, text="")
            label.pack()
            self.cmyk_labels.append(label)

        rgb_frame = tk.Frame(labels_frame)
        rgb_frame.grid(row=0, column=1, padx=10)
        rgb_label = tk.Label(rgb_frame, text="RGB:")
        rgb_label.pack()
        for i in range(3):
            label = tk.Label(rgb_frame, text="")
            label.pack()
            self.rgb_labels.append(label)

        hls_frame = tk.Frame(labels_frame)
        hls_frame.grid(row=0, column=2, padx=10)
        hls_label = tk.Label(hls_frame, text="HLS:")
        hls_label.pack()
        for i in range(3):
            label = tk.Label(hls_frame, text="")
            label.pack()
            self.hls_labels.append(label)

        palette_button = tk.Button(labels_frame, text="Sliders", command=self.choose_color)
        palette_button.grid(row=0, column=3, padx=10)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            r, g, b = hex2rgb(color)
            c, m, y, k = rgb2cmyk(r, g, b)
            h, l, s = rgb2hls(r, g, b)
            self.set_background_color(r, g, b)
            self.update_cmyk_labels(c, m, y, k)
            self.update_rgb_labels(r, g, b)
            self.update_hls_labels(h, l, s)
            self.set_slider_values(r, g, b)

    def set_slider_values(self, r, g, b):
        self.input_sliders[0].set(r)
        self.input_sliders[1].set(g)
        self.input_sliders[2].set(b)

    def update_input_type(self, event):
        input_type = self.input_type_var.get()
        if input_type == "CMYK":
            self.set_slider_conf(0, 100)
            self.input_sliders[3].pack()
        elif input_type == "RGB":
            self.set_slider_conf(0, 255)
            self.input_sliders[3].pack_forget()
        elif input_type == "HLS":
            self.set_slider_conf(0, 100)
            self.input_sliders[0].configure(from_=0, to=359)
            self.input_sliders[3].pack_forget()

    def set_slider_conf(self, from__, to__):
        for i in range(4):
            self.input_sliders[i].configure(from_=from__, to=to__)

    def update_slider_value(self, value):
        input_type = self.input_type_var.get()
        if input_type == "CMYK":
            self.update_cmyk(None)
        elif input_type == "RGB":
            self.update_rgb(None)
        elif input_type == "HLS":
            self.update_hls(None)

    def update_cmyk(self, event):
        try:
            input_value = [int(slider.get()) / 100 for slider in self.input_sliders]
            if self.input_type_var.get() == "CMYK":
                c, m, y, k = input_value
                r, g, b = cmyk2rgb(c, m, y, k)
                h, l, s = rgb2hls(r, g, b)
                self.set_background_color(r, g, b)
                self.update_cmyk_labels(c, m, y, k)
                self.update_rgb_labels(r, g, b)
                self.update_hls_labels(h, l, s)
        except ValueError:
            pass

    def update_rgb(self, event):
        try:
            input_value = [int(slider.get()) for slider in self.input_sliders[:-1]]
            if self.input_type_var.get() == "RGB":
                r, g, b = input_value
                c, m, y, k = rgb2cmyk(r, g, b)
                h, l, s = rgb2hls(r, g, b)
                self.set_background_color(r, g, b)
                self.update_cmyk_labels(c, m, y, k)
                self.update_rgb_labels(r, g, b)
                self.update_hls_labels(h, l, s)
        except ValueError:
            pass

    def update_hls(self, event):
        try:
            input_value = [int(slider.get()) for slider in self.input_sliders[:-1]]
            if self.input_type_var.get() == "HLS":
                h, l, s = input_value
                r, g, b = hls2rgb(h, l, s)
                c, m, y, k = rgb2cmyk(r, g, b)
                self.set_background_color(r, g, b)
                self.update_cmyk_labels(c, m, y, k)
                self.update_rgb_labels(r, g, b)
                self.update_hls_labels(h, l, s)
        except ValueError:
            pass

    def update_cmyk_labels(self, c, m, y, k):
        labels = self.cmyk_labels
        labels[0].configure(text=f"C: {c:.2f}")
        labels[1].configure(text=f"M: {m:.2f}")
        labels[2].configure(text=f"Y: {y:.2f}")
        labels[3].configure(text=f"K: {k:.2f}")

    def update_rgb_labels(self, r, g, b):
        labels = self.rgb_labels
        labels[0].configure(text=f"R: {r}")
        labels[1].configure(text=f"G: {g}")
        labels[2].configure(text=f"B: {b}")

    def update_hls_labels(self, h, l, s):
        labels = self.hls_labels
        labels[0].configure(text=f"H: {h}")
        labels[1].configure(text=f"L: {l}")
        labels[2].configure(text=f"S: {s}")

    def set_background_color(self, r, g, b):
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.root.configure(background=hex_color)


if __name__ == "__main__":
    app = App()