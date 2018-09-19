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

IMPORTANT_TEXT = "As of 29/5, an update has been made to the queue to factor in the number of questions asked that day (since midnight the night prior), per student. Higher priority will be given to students with lower numbers of questions. This is calculated separately for each of the queues."


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


class Question:
    def __init__(self, rank, name, questions, time):
        self.rank = rank
        self.name = name
        self.questions = questions
        self.time = time


class Separator(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, relief=tk.RIDGE, height=2, bg="#eee",
                         *args, **kwargs)


class InfoPane(tk.Frame):
    def __init__(self, master, title, text, foreground="#C09853",
                 background="#fefbed", *args, **kwargs):
        super().__init__(master, background=background, *args, **kwargs)
        title = tk.Label(self, text=title, background=background,
                         foreground=foreground, font=("Arial", 18, "bold"))
        title.pack(anchor=tk.W)

        text = tk.Label(self, text=text, justify=tk.LEFT, wraplength=1000,
                        background=background)
        text.pack(anchor=tk.W)


class QuestionFrame(tk.Frame):
    def __init__(self, master, title="Questions", subtitle="", examples=None,
                 button="Request Help", colour_scheme=None, *args, **kwargs):
        super().__init__(master, padx=20, pady=20, *args, **kwargs)
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

        self._question_table = question_table = QuestionTable(self)
        question_table.pack(expand=True, fill=tk.BOTH)

    def draw_header(self, title, subtitle):
        header = QuestionHeader(self, title, subtitle,
                                colour_scheme=self.colour_scheme)
        header.pack(expand=True, fill=tk.BOTH)

    def draw_examples(self, examples):
        example_frame = tk.Frame(self)
        example_header = tk.Label(example_frame,
                                  text="Some examples of quick questions:")
        example_header.pack(anchor=tk.W)

        for example in examples:
            example_label = tk.Label(example_frame, text="    • " + example)
            example_label.pack(anchor=tk.W)

        example_frame.pack(anchor=tk.W, pady=20)

    def draw_button(self, text):
        button = tk.Button(self, text=text, font=("Arial", 14, ""), foreground="white",
                           background=self.colour_scheme.button_background,
                           highlightbackground=self.colour_scheme.button_background,
                           padx=10, pady=10)
        button.pack(pady=10)

    def draw_separator(self):
        Separator(self).pack(fill=tk.X, padx=5, pady=5)

    def draw_averages(self):
        text = tk.Label(self, text="No students in queue.")
        text.pack(anchor=tk.W, pady=10)

    def add_question(self, question):
        self._question_table.add_question(question)


class QuestionTable(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._current = 1

        header = Question("#", "Name", "Questions Today", "Time")

        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.columnconfigure(self, 3, weight=1)
        self.build_row(header, 0, font=("Arial", 14, "bold"))

    def build_row(self, question, row, font=("Arial", 14, "")):
        rank_label = tk.Label(self, text=question.rank, font=font)
        rank_label.grid(row=row, column=0)

        name_label = tk.Label(self, text=question.name, font=font)
        name_label.grid(row=row, column=1, sticky=tk.W)

        questions_label = tk.Label(self, text=question.questions, font=font)
        questions_label.grid(row=row, column=2, sticky=tk.W)

        time_label = tk.Label(self, text=question.time, font=font)
        time_label.grid(row=row, column=3, sticky=tk.W)

    def add_question(self, question):
        self.build_row(question, self._current)
        self._current += 1


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

        update_text = InfoPane(master, title="Important", text=IMPORTANT_TEXT,
                               padx=20, pady=20)
        update_text.pack()

        quick_queue = QuestionFrame(master, title="Quick Questions",
                                    subtitle="< 2 mins with a tutor",
                                    examples=QUICK_EXAMPLES,
                                    button="Request Quick Help",
                                    colour_scheme=COLOUR_SCHEMES["quick"])
        quick_queue.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)

        brae = Question("1", "Mr Brae Jak Webb", "2", "2 hours")
        quick_queue.add_question(brae)
        brae = Question("2", "Peter O'Shea", "1", "1 hour")
        quick_queue.add_question(brae)
        brae = Question("3", "Evan Almighty", "2", "45 minutes")
        quick_queue.add_question(brae)

        long_queue = QuestionFrame(master, title="Long Questions",
                                   subtitle="> 2 mins with a tutor",
                                   examples=LONG_EXAMPLES,
                                   button="Request Long Help",
                                   colour_scheme=COLOUR_SCHEMES["long"])
        long_queue.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)


def main():
    root = tk.Tk()
    root.title("CSSE1001 Queue")
    Queue(root)
    root.mainloop()


if __name__ == "__main__":
    main()
