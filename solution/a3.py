#!/bin/python3
"""
Assignment 3 Solution
CSSE1001 Semester 2, 2018
"""

import tkinter as tk


SHORT_EXAMPLES = [
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


class QuestionFrame(tk.Frame):
    pass


class QuestionRow(tk.Frame):
    pass


class QuestionHeader(tk.Frame):
    pass


class Queue(tk.Frame):
    def __init__(self):
        short_queue = QuestionFrame(title="Quick Questions",
                                    subtitle="< 2 mins with a tutor",
                                    examples=SHORT_EXAMPLES,
                                    button="Request Quick Help")
        long_queue = QuestionFrame(title="Long Questions",
                                   subtitle="> 2 mins with a tutor",
                                   examples=LONG_EXAMPLES,
                                   button="Request Long Help")


def main():
    root = tk.Tk()
    queue = Queue(root)
    root.mainloop()


if __name__ == "__main__":
    main()