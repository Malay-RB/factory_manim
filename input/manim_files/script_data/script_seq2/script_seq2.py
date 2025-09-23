"""Draw a circle"""

from manim import *

class ScriptSeq2(Scene):
    def construct(self):
        # Draw a circle
        circle = Circle()
        self.play(Create(circle))
        self.wait(2)