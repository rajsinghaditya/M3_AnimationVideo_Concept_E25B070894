"""
Scene 0: Opening Frame
Title card for ~5 seconds with student info.
"""
from manim import *

class Scene0_Opening(Scene):
    def construct(self):
        # Read duration from audio
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene0", 5.0)

        # Dark background (default)
        title = Text("Gaussian Elimination", font_size=56, color=WHITE, weight=BOLD)
        subtitle = Text("Solving a 3×3 System of Linear Equations", font_size=36, color=BLUE_C)
        course = Text("M3 Internal Assessment – Animation Video", font_size=30, color=GREY_B)
        name = Text("Aditya Raj Singh", font_size=32, color=WHITE)
        student_id = Text("Student ID: e25b070894", font_size=28, color=GREY_B)

        # Layout
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        info_group = VGroup(course, name, student_id).arrange(DOWN, buff=0.25)
        full = VGroup(title_group, info_group).arrange(DOWN, buff=0.8)

        # Decorative line
        line = Line(LEFT * 4, RIGHT * 4, color=BLUE_C, stroke_width=2)
        line.next_to(title_group, DOWN, buff=0.3)

        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            run_time=0.8
        )
        self.play(
            FadeIn(subtitle, shift=DOWN * 0.2),
            Create(line),
            run_time=0.6
        )
        self.play(
            FadeIn(course, shift=UP * 0.2),
            FadeIn(name, shift=UP * 0.2),
            FadeIn(student_id, shift=UP * 0.2),
            run_time=0.6
        )
        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)
        self.play(FadeOut(VGroup(title, subtitle, line, course, name, student_id)), run_time=0.5)
