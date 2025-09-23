"""Label the circle"""

from manim import *

class ScriptSeq3(Scene):
    def construct(self):
        # Label the circle
        circle = Circle()
        label = Text("A").next_to(circle, DOWN)
        
        self.play(Create(circle))
        self.play(Write(label))
        self.wait(2)
