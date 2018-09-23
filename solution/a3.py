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
IMPORTANT_TEXT = "Individual assessment items must be solely your own work. While students are encouraged to have " \
                 "high-level conversations about the problems they are trying to solve, you must not look at another " \
                 "student's code or copy from it. The university used sophisticated anti-collusion measures to " \
                 "automatically detect similarity between assignment submissions."

# colours for indicating good and bad actions
SUCCESS = "#5cb85c"
DANGER = "#d9534f"


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

    def get_average(self):
        """(str): The average wait time for a student in the queue"""
        total = 0
        for student in self.waiting:
            total += self.times[student]
        return total/len(self.waiting)


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

    def __init__(self, master, title, text, *args, foreground="#C09853", background="#fefbed",
                 header_font=("Arial", 18, "bold"), **kwargs):
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
                         foreground=foreground, font=header_font)
        title.pack(anchor=tk.W)

        # information to display from this pane
        text = tk.Label(self, text=text, justify=tk.LEFT, wraplength=1000,
                        background=background)
        text.pack(anchor=tk.W)


class QuestionFrame(tk.Frame):
    """
    Widget to display information about a question type along with a list of
    questions in a queue

    Includes the header, examples of types of questions, the average wait time
    and a table of questions
    """
    def __init__(self, master, *args, title="Questions", subtitle="", examples=None, button="Request Help",
                 colour_scheme=None, request_callback=None, tick_function=None, cross_function=None, **kwargs):
        """
        Construct a new question frame with title details, examples of questions,
        and a colour scheme

        Parameters:
            master (tk.Frame): The tkinter widget containing the frame
            title (str): Title of this type of questions
            subtitle (str): Brief description of this type of questions
            examples (list<str>): List of examples of this type of question
            button (str): Text to display on the request help button
            colour_scheme (ColourScheme): A colour scheme to use for this question
            request_callback (func): Callable to call when help is requested
            tick_function (func): Callable to call when a student is ticked
            cross_function (func): Callable to call when a student is crossed
        """
        super().__init__(master, padx=20, pady=20, *args, **kwargs)

        if examples is None:
            examples = []

        if colour_scheme is None:
            colour_scheme = ColourScheme()

        self.colour_scheme = colour_scheme
        self._request_callback = request_callback

        self.draw_header(title, subtitle)
        self.draw_examples(title.lower(), examples)
        self.draw_button(button)

        self.draw_separator()

        self.draw_average(None)

        self.draw_separator()

        self._question_table = QuestionTable(self, tick_function=tick_function, cross_function=cross_function)
        self._question_table.pack(expand=True, fill=tk.BOTH)

    def draw_header(self, title, subtitle):
        """Render a question header to the question frame

        Parameters:
            title (str): Title of this type of question
            subtitle (str): Brief description of this type of question
        """
        header = QuestionHeader(self, title=title, subtitle=subtitle, colour_scheme=self.colour_scheme)
        header.pack(expand=True, fill=tk.BOTH)

    def draw_examples(self, label, examples):
        """Render a list of examples of this type of question

        Parameters:
            label (str): A label for this type of question
            examples (list<str>): List of examples of this type of question
        """
        example_frame = tk.Frame(self)
        example_header = tk.Label(example_frame,
                                  text=f"Some examples of {label}:")
        example_header.pack(anchor=tk.W)

        for example in examples:
            example_label = tk.Label(example_frame, text="    • " + example)
            example_label.pack(anchor=tk.W)

        example_frame.pack(anchor=tk.W, pady=20)

    def draw_button(self, text):
        """Render the button to request help for a queue

        Parameters:
            text (str): The label of the button to display
        """
        button = tk.Button(self, text=text, font=("Arial", 14, ""), foreground="white",
                           background=self.colour_scheme.button_background,
                           highlightbackground=self.colour_scheme.button_background,
                           padx=10, pady=10, command=self._request_callback)
        button.pack(pady=10)

    def draw_separator(self):
        """Render a horizontal line separator in the frame"""
        Separator(self).pack(fill=tk.X, padx=5, pady=5)

    def draw_average(self, average):  # pylint: disable=unused-argument
        """Render text to display the average wait time for a question

        Parameters:
            average (str): The average wait time for a questions
        """
        text = tk.Label(self, text="No students in queue.")
        text.pack(anchor=tk.W, pady=10)

    def refresh(self, questions):
        """Refresh the question table with a list of questions

        Parameters:
            questions (list<Question>): List of questions for a queue
        """
        self._question_table.refresh(questions)


class QuestionTable(tk.Frame):
    """A table of questions asked in a queue"""

    def __init__(self, master, *args, tick_function=None, cross_function=None, **kwargs):
        """Construct a new QuestionTable

        Parameters:
            master (tk.Frame): A tkinter frame to store this table within
            tick_function (func): Callable to call when a tick is pressed
            cross_function (func): Callable to call when a cross is pressed
        """
        super().__init__(master, *args, **kwargs)

        # the row in the grid to start adding questions
        self._current = 2

        self._tick_function = tick_function
        self._cross_function = cross_function

        # configure the grid to fill the space
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.columnconfigure(self, 3, weight=1)

        # create a header row for the question table
        header = Question("#", "Name", "Questions Today", "Time")
        self.build_row(header, 0, font=("Arial", 14, "bold"))

        # add a separator after the header
        Separator(self).grid(row=1, column=0, columnspan=6,
                             padx=5, pady=5, sticky=tk.NSEW)

        # a list of tuples containing all widgets related to a question
        # used for clearing rows from the queue
        self._questions = []

    def build_row(self, question, row, tick=None, cross=None,
                  font=("Arial", 14, "")):
        """Create a new row for a question in the table

        Parameters:
            question (Question): The question to display on this row
            row (int): The row number
            tick (func): Callable to call when the tick box is clicked
            cross (func): Callable to call when the cross is clicked
        """
        rank_label = tk.Label(self, text=question.rank, font=font)
        rank_label.grid(row=row, column=0)

        name_label = tk.Label(self, text=question.name, font=font)
        name_label.grid(row=row, column=1, sticky=tk.W)

        questions_label = tk.Label(self, text=question.questions, font=font)
        questions_label.grid(row=row, column=2, sticky=tk.W)

        time_label = tk.Label(self, text=question.time, font=font)
        time_label.grid(row=row, column=3, sticky=tk.W)

        cross_box = tick_box = None

        # render a cross button if a callback is given
        if cross is not None:
            cross_box = tk.Button(self, background=DANGER,
                                  command=lambda: cross(question.name),
                                  highlightbackground=DANGER, padx=8)
            cross_box.grid(row=row, column=4)

        # render a tick button if a callback is given
        if tick is not None:
            tick_box = tk.Button(self, background=SUCCESS,
                                 command=lambda: tick(question.name),
                                 highlightbackground=SUCCESS, padx=8)
            tick_box.grid(row=row, column=5)

        # return all widgets associated with this row (for later removal)
        return rank_label, name_label, questions_label, time_label, cross_box, tick_box

    def add_question(self, question):
        """Add a new question to the table

        Parameters:
            question (Question): The question to add to the table
        """
        # append result so it can later be removed
        self._questions.append(self.build_row(question, self._current,
                                              tick=self._tick_function,
                                              cross=self._cross_function,))
        # increase the current row number
        self._current += 1

    def refresh(self, questions):
        """Redraw all the rows based on the provided questions

        Parameters:
            questions (list<Question>): The questions to display in the table
        """
        # remove all previous questions
        for question in self._questions:
            for label in question:
                label.grid_forget()
        self._questions = []

        # reset the row number
        self._current = 2

        # render all the questions
        for question in questions:
            self.add_question(question)


class QuestionHeader(tk.Frame):
    """Header for a question"""
    def __init__(self, master, *args, title="Questions", subtitle="", colour_scheme=None,
                 title_font=("Arial", 28, "bold"), subtitle_font=("Arial", 14, ""), **kwargs):
        """Create a new QuestionHeader

        Parameters:
            master (tk.Frame): The tkinter frame to place the header within
            title (str): Title for the header
            subtitle (str): Subtitle/brief description of the type of questions
            colour_scheme (ColourScheme): The colour scheme to use for the header
        """
        if colour_scheme is None:
            colour_scheme = ColourScheme()

        self.scheme = scheme = colour_scheme

        super().__init__(master, background=scheme.header_background,
                         highlightbackground=scheme.header_border,
                         highlightthickness=1, *args, **kwargs)

        title = tk.Label(self, background=scheme.header_background, text=title,
                         font=title_font, foreground=scheme.header_text)
        title.pack(expand=True, padx=20, pady=20)

        subtitle = tk.Label(self, background=scheme.header_background,
                            text=subtitle, font=subtitle_font,
                            foreground=scheme.subtitle_text)
        subtitle.pack(expand=True, padx=20, pady=10)


class QueueApp(tk.Frame):
    """CSSE1001 queue application"""

    def __init__(self, master, *args, **kwargs):
        """Create a new queue window

        Parameters:
            master (tk.Tk|tk.Toplevel): The window to render the application within
        """
        super().__init__(master, *args, **kwargs)

        # display information about the recent update
        update_text = InfoPane(self, title="Important", text=IMPORTANT_TEXT, padx=20, pady=20)
        update_text.pack()

        self._quick_queue = quick_queue = Queue()
        quick_frame = QuestionFrame(self, title="Quick Questions", subtitle="< 2 mins with a tutor",
                                    examples=QUICK_EXAMPLES, button="Request Quick Help", colour_scheme=QUICK_COLOURS,
                                    request_callback=lambda event=None: self.request(quick_queue),
                                    tick_function=lambda name: self.tick(quick_queue, name),
                                    cross_function=lambda name: self.cross(quick_queue, name))
        quick_frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)

        self._long_queue = long_queue = Queue()
        long_frame = QuestionFrame(self, title="Long Questions", subtitle="> 2 mins with a tutor",
                                   examples=LONG_EXAMPLES, button="Request Long Help", colour_scheme=LONG_COLOURS,
                                   request_callback=lambda event=None: self.request(long_queue),
                                   tick_function=lambda name: self.tick(long_queue, name),
                                   cross_function=lambda name: self.cross(long_queue, name))
        long_frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=True)

        self._quick_frame = quick_frame
        self._long_frame = long_frame
        self.refresh()

    def request(self, queue):
        """Prompt the student to enter their name and add them to the queue

        Parameters:
            queue (Queue): The queue to add the student onto
        """
        name = simpledialog.askstring("Name", "Please Enter Your Name")
        if name:
            queue.add_student(name)
            self.refresh_queues()

    def tick(self, queue, name):
        """Remove the given student from the displayed queue and refresh

        Parameters:
            queue (Queue): The queue to remove the student from
            name (str): The name of the student to remove
        """
        queue.remove_student(name)
        self.refresh_queues()

    def cross(self, queue, name):
        """Remove the given student from the displayed queue and refresh

        Parameters:
            queue (Queue): The queue to remove the student from
            name (str): The name of the student to remove
        """
        queue.remove_student(name)
        self.refresh_queues()

    def refresh_queues(self):
        """Refresh the two queues with updates from the model"""
        self._quick_frame.refresh(self._quick_queue.get_questions())
        self._long_frame.refresh(self._long_queue.get_questions())

    def refresh(self):
        """Start the queue auto-refreshing"""
        self.refresh_queues()
        self.after(10000, self.refresh)


def main():
    """Run the queue application"""
    root = tk.Tk()
    root.title("CSSE1001 Queue")
    queue = QueueApp(root)
    queue.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
