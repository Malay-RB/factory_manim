"""Show a title card"""

from manim import *

class ScriptSeq1(Scene):
    def construct(self):
        # Show a title card
        title = Text("Welcome to our video!")
        self.play(Write(title))
        self.wait(2)