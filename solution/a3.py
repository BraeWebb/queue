#!/bin/python3
"""
Assignment 3 Solution
CSSE1001 Semester 2, 2018
"""

import tkinter as tk


QUICK_EXAMPLES = [
    "Syntax errors",
    "Interpreting error output",
    "Assignment/MyPyTutor interpretation",
    "MyPyTutor submission issues"
]

LONG_EXAMPLES = [
    "Open ended questions",
    "How to start a problem",
    "How to improve code",
    "Debugging",
    "Assignment help"
]


class ColourScheme:
    def __init__(self, header_background="#dff0d8", header_border="#d6e9c6",
                 header_text="#3c763d", subtitle_text="#666",
                 button_background="#5cb85c", button_border="#4cae4c"):
        self.header_background = header_background
        self.header_border = header_border
        self.header_text = header_text
        self.subtitle_text = subtitle_text
        self.button_background = button_background
        self.button_border = button_border


COLOUR_SCHEMES = {
    "long": ColourScheme(header_background="#d9edf7", header_border="#bce8f1",
                         header_text="#31708f", subtitle_text="#666",
                         button_background="#5bc0de", button_border="#46b8da"),
    "quick": ColourScheme(header_background="#dff0d8", header_border="#d6e9c6",
                          header_text="#3c763d", subtitle_text="#666",
                          button_background="#5cb85c", button_border="#4cae4c")
}


class Separator(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, relief=tk.RIDGE, height=2, bg="#eee",
                         *args, **kwargs)


class QuestionFrame(tk.Frame):
    def __init__(self, master, title="Questions", subtitle="", examples=None,
                 button="Request Help", colour_scheme=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if examples is None:
            examples = []
        if colour_scheme is None:
            colour_scheme = ColourScheme()

        self.colour_scheme = colour_scheme

        self.draw_header(title, subtitle)
        self.draw_examples(examples)
        self.draw_button(button)

        self.draw_separator()

        self.draw_averages()

        self.draw_separator()

    def draw_header(self, title, subtitle):
        header = QuestionHeader(self, title, subtitle,
                                colour_scheme=self.colour_scheme,)
        header.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def draw_examples(self, examples):
        example_header = tk.Label(self, text="Some examples of quick questions:")
        example_header.pack(anchor=tk.W)

        for example in examples:
            example_label = tk.Label(self, text="    • " + example)
            example_label.pack(anchor=tk.W)

    def draw_button(self, text):
        button = tk.Button(self, text=text, font=("Arial", 14, ""), foreground="white",
                           background=self.colour_scheme.button_background,
                           highlightbackground=self.colour_scheme.button_background,
                           padx=10, pady=10)
        button.pack()

    def draw_separator(self):
        Separator(self).pack(fill=tk.X, padx=5, pady=5)

    def draw_averages(self):
        text = tk.Label(self, text="No students in queue.")
        text.pack()


class QuestionRow(tk.Frame):
    pass


class QuestionHeader(tk.Frame):
    def __init__(self, master, title="Questions", subtitle="", colour_scheme=None,
                 *args, **kwargs):
        if colour_scheme is None:
            colour_scheme = ColourScheme()

        self.scheme = scheme = colour_scheme

        super().__init__(master, background=scheme.header_background,
                         highlightbackground=scheme.header_border,
                         highlightthickness=1, *args, **kwargs)

        title = tk.Label(self, background=scheme.header_background, text=title,
                         font=("Arial", 28, "bold"), foreground=scheme.header_text)
        title.pack(expand=True, padx=20, pady=20)

        subtitle = tk.Label(self, background=scheme.header_background,
                            text=subtitle, font=("Arial", 14, ""),
                            foreground=scheme.subtitle_text)
        subtitle.pack(expand=True, padx=20, pady=10)


class Queue(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        quick_queue = QuestionFrame(master, title="Quick Questions",
                                    subtitle="< 2 mins with a tutor",
                                    examples=QUICK_EXAMPLES,
                                    button="Request Quick Help",
                                    colour_scheme=COLOUR_SCHEMES["quick"])
        quick_queue.pack(side=tk.LEFT, fill=tk.BOTH)

        long_queue = QuestionFrame(master, title="Long Questions",
                                   subtitle="> 2 mins with a tutor",
                                   examples=LONG_EXAMPLES,
                                   button="Request Long Help",
                                   colour_scheme=COLOUR_SCHEMES["long"])
        long_queue.pack(side=tk.LEFT, fill=tk.BOTH)


def main():
    root = tk.Tk()
    Queue(root)
    root.mainloop()


if __name__ == "__main__":
    main()
