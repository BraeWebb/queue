#!/bin/python3
"""
Assignment 3 Solution
CSSE1001 Semester 2, 2018
"""

import datetime
import tkinter as tk
from tkinter import simpledialog


# example of type of quick queue questions
QUICK_EXAMPLES = [
    "Syntax errors",
    "Interpreting error output",
    "Assignment/MyPyTutor interpretation",
    "MyPyTutor submission issues"
]

# example of types of long queue questions
LONG_EXAMPLES = [
    "Open ended questions",
    "How to start a problem",
    "How to improve code",
    "Debugging",
    "Assignment help"
]

# text above the queue indicating an update to the queue has occurred
IMPORTANT_TEXT = "As of 29/5, an update has been made to the queue to factor in the number of questions asked that day (since midnight the night prior), per student. Higher priority will be given to students with lower numbers of questions. This is calculated separately for each of the queues."

# colours for indicating good and bad actions
SUCCESS = "#5cb85c"
DANGER = "#d9534f"


class ColourScheme:
    """
    Container for a queue frame colour screen

    Stores colour codes for various sections of the queue
    """

    def __init__(self, header_background="#dff0d8", header_border="#d6e9c6",
                 header_text="#3c763d", subtitle_text="#666",
                 button_background="#5cb85c", button_border="#4cae4c"):
        """
        Create a new ColourScheme with provided colours or defaults

        Parameters:
            header_background (str): Colour of the headers background
            header_border (str): Colour of the headers border
            header_text (str): Colour of the headers title text
            subtitle_text (str): Colour of the subtitle text in the header
            button_background (str): Colour of the request buttons background
            button_border (str): Colour of the question buttons border
        """
        self.header_background = header_background
        self.header_border = header_border
        self.header_text = header_text
        self.subtitle_text = subtitle_text
        self.button_background = button_background
        self.button_border = button_border


# colour scheme for the long question section
LONG_COLOURS = ColourScheme(header_background="#d9edf7", header_border="#bce8f1",
                            header_text="#31708f", subtitle_text="#666",
                            button_background="#5bc0de", button_border="#46b8da")

# colour scheme for the quick question section
QUICK_COLOURS = ColourScheme(header_background="#dff0d8", header_border="#d6e9c6",
                             header_text="#3c763d", subtitle_text="#666",
                             button_background="#5cb85c", button_border="#4cae4c")


class Question:
    """Data for a question displayed in a row on the queue"""

    def __init__(self, rank, name, questions, time):
        """
        Create a new Question

        Parameters:
            rank (int): The rank of the question in the queue
            name (str): The name of the student who has a question
            questions (int): The amount of questions already asked
            time (str): How long the student has been waiting
        """
        self.rank = rank
        self.name = name
        self.questions = questions
        self.time = time


class Separator(tk.Frame):
    """A horizontal line between widgets in a frame"""

    def __init__(self, master, *args, **kwargs):
        """
        Construct a new Separator

        Parameters:
            master (tk.Frame): Frame to place a horizontal line within
            *args (*): Extra positional parameters to pass to tk.Frame
            **kwargs (*): Extra keyword parameters to pass to tk.Frame
        """
        super().__init__(master, relief=tk.RIDGE, height=2, bg="#eee",
                         *args, **kwargs)


class InfoPane(tk.Frame):
    """A box of important information to display to the user"""

    def __init__(self, master, title, text, foreground="#C09853",
                 background="#fefbed", *args, **kwargs):
        """
        Create a new InfoPane with a title and description

        Parameters:
            master (tk.Frame): The frame to place the pane within
            title (str): The title of the information pane
            text (str): Information displayed by this pane
        """
        super().__init__(master, background=background, *args, **kwargs)

        # bolded and coloured title
        title = tk.Label(self, text=title, background=background,
                         foreground=foreground, font=("Arial", 18, "bold"))
        title.pack(anchor=tk.W)

        # information to display from this pane
        text = tk.Label(self, text=text, justify=tk.LEFT, wraplength=1000,
                        background=background)
        text.pack(anchor=tk.W)


class QuestionFrame(tk.Frame):
    def __init__(self, master, title="Questions", subtitle="", examples=None,
                 button="Request Help", colour_scheme=None, request_callback=None,
                 tick_function=None, cross_function=None, *args, **kwargs):
        super().__init__(master, padx=20, pady=20, *args, **kwargs)
        if examples is None:
            examples = []
        if colour_scheme is None:
            colour_scheme = ColourScheme()

        self.colour_scheme = colour_scheme
        self._request_callback = request_callback

        self.draw_header(title, subtitle)
        self.draw_examples(examples)
        self.draw_button(button)

        self.draw_separator()

        self.draw_averages()

        self.draw_separator()

        self._question_table = QuestionTable(self, tick_function, cross_function)
        self._question_table.pack(expand=True, fill=tk.BOTH)

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
                           padx=10, pady=10, command=self._request_callback)
        button.pack(pady=10)

    def draw_separator(self):
        Separator(self).pack(fill=tk.X, padx=5, pady=5)

    def draw_averages(self):
        text = tk.Label(self, text="No students in queue.")
        text.pack(anchor=tk.W, pady=10)

    def refresh(self, questions):
        self._question_table.refresh(questions)


class QuestionTable(tk.Frame):
    def __init__(self, master, tick_function=None, cross_function=None,
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._current = 2
        self._tick_function = tick_function
        self._cross_function = cross_function

        header = Question("#", "Name", "Questions Today", "Time")

        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.columnconfigure(self, 3, weight=1)
        self.build_row(header, 0, font=("Arial", 14, "bold"))

        Separator(self).grid(row=1, column=0, columnspan=6,
                             padx=5, pady=5, sticky=tk.NSEW)

        self._questions = []

    def build_row(self, question, row, tick=None, cross=None,
                  font=("Arial", 14, "")):
        rank_label = tk.Label(self, text=question.rank, font=font)
        rank_label.grid(row=row, column=0)

        name_label = tk.Label(self, text=question.name, font=font)
        name_label.grid(row=row, column=1, sticky=tk.W)

        questions_label = tk.Label(self, text=question.questions, font=font)
        questions_label.grid(row=row, column=2, sticky=tk.W)

        time_label = tk.Label(self, text=question.time, font=font)
        time_label.grid(row=row, column=3, sticky=tk.W)

        cross_box = tick_box = None

        if cross is not None:
            cross_box = tk.Button(self, background=DANGER,
                                  command=lambda: cross(question.name),
                                  highlightbackground=DANGER, padx=8)
            cross_box.grid(row=row, column=4)

        if tick is not None:
            tick_box = tk.Button(self, background=SUCCESS,
                                 command=lambda: tick(question.name),
                                 highlightbackground=SUCCESS, padx=8)
            tick_box.grid(row=row, column=5)

        return rank_label, name_label, questions_label, time_label, cross_box, tick_box

    def add_question(self, question):
        self._questions.append(self.build_row(question, self._current,
                                              tick=self._tick_function,
                                              cross=self._cross_function,))
        self._current += 1

    def refresh(self, questions):
        for question in self._questions:
            for label in question:
                label.grid_forget()

        for question in questions:
            self.add_question(question)


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


class QueueApp(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        update_text = InfoPane(self, title="Important", text=IMPORTANT_TEXT,
                               padx=20, pady=20)
        update_text.pack()

        self._quick_queue = quick_queue = Queue()
        quick_frame = QuestionFrame(self, title="Quick Questions",
                                    subtitle="< 2 mins with a tutor",
                                    examples=QUICK_EXAMPLES,
                                    button="Request Quick Help",
                                    colour_scheme=QUICK_COLOURS,
                                    request_callback=lambda event=None: self.request(quick_queue),
                                    tick_function=lambda name: self.tick(quick_queue, name),
                                    cross_function=lambda name: self.cross(quick_queue, name))
        quick_frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)

        self._long_queue = long_queue = Queue()
        long_frame = QuestionFrame(self, title="Long Questions",
                                   subtitle="> 2 mins with a tutor",
                                   examples=LONG_EXAMPLES,
                                   button="Request Long Help",
                                   colour_scheme=LONG_COLOURS,
                                   request_callback=lambda event=None: self.request(long_queue),
                                   tick_function=lambda name: self.tick(long_queue, name),
                                   cross_function=lambda name: self.cross(long_queue, name))
        long_frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)

        self._quick_frame = quick_frame
        self._long_frame = long_frame
        self.refresh()

    def request(self, queue):
        name = simpledialog.askstring("Name", "Please Enter Your Name")
        if name:
            queue.add_student(name)
            self.refresh_queues()

    def tick(self, queue, name):
        queue.remove_student(name)
        self.refresh_queues()

    def cross(self, queue, name):
        queue.remove_student(name)
        self.refresh_queues()

    def refresh_queues(self):
        self._quick_frame.refresh(self._quick_queue.get_questions())
        self._long_frame.refresh(self._long_queue.get_questions())

    def refresh(self):
        self.refresh_queues()
        self.after(10000, self.refresh)


class Queue:
    """Queue of students waiting to have a question answered"""

    def __init__(self):
        """Initialize a new queue"""
        # list of students waiting in the queue
        self.waiting = []

        # a map of students to the amount of questions they've asked
        self.history = {}

        # a map of students to the time they joined the queue
        self.times = {}

    def add_student(self, name):
        """Add a student to the queue

        Parameters:
            name (str): The name of the student that's joining
        """
        if name in self.waiting:
            return

        # update or set the questions asked count
        count = self.history.get(name, 0)
        self.history[name] = count + 1

        # log the time they asked the question
        self.times[name] = datetime.datetime.now()

        self.waiting.append(name)

    def remove_student(self, name):
        """Remove a student from the queue

        Parameters:
            name (str): The name of the student that's leaving
        """
        self.waiting.remove(name)

    def get_questions(self):
        """(list<Question>): The list of questions for this queue"""
        questions = []
        for i, student in enumerate(self.waiting):
            question_count = self.history[student]
            time_waiting = format_time(self.times[student], datetime.datetime.now())

            questions.append(Question(i + 1, student, question_count, time_waiting))
        return questions


def format_time(start, end):
    """
    Computes the difference between two times and displays a friendly format

    If hours of difference displays 'X hours', if minutes 'X minutes', if only
    seconds of difference, 'a few seconds ago'

    Parameters:
        start (datetime.datetime): The starting time
        end (datetime.datetime): The end time to compare to start time

    Returns:
        (str): Formatted difference as specified above
    """
    diff = end - start

    hours = diff.days // 24
    minutes = diff.seconds // 60

    if hours > 0:
        return str(hours) + (" hours" if hours > 1 else " hour")

    if minutes > 0:
        return str(minutes) + (" minutes" if minutes > 1 else " minute")

    return "a few seconds ago"


def main():
    root = tk.Tk()
    root.title("CSSE1001 Queue")
    queue = QueueApp(root)
    queue.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
