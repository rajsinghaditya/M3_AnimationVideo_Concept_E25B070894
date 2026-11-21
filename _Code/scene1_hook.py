"""
Scene 1: Hook (~30 seconds)
Show the problem of solving 3 equations at once — trial and error is messy.
"""
from manim import *

class Scene1_Hook(Scene):
    def construct(self):
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene1", 30.0)

        # Show three equations
        eq1 = MathTex(r"x + y + z = 6", color=BLUE_C, font_size=44)
        eq2 = MathTex(r"2x + 3y + z = 11", color=GREEN_C, font_size=44)
        eq3 = MathTex(r"x + 2y + 3z = 14", color=ORANGE, font_size=44)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.4).shift(UP * 0.5)

        header = Text("Three equations, three unknowns...", font_size=38, color=WHITE)
        header.to_edge(UP, buff=0.6)

        self.play(Write(header), run_time=1.0)
        self.play(
            Write(eq1), Write(eq2), Write(eq3),
            run_time=2.0
        )
        self.wait(2.0)

        # Show trial and error attempt
        trial = Text("Trial: x=1, y=1, z=1?", font_size=32, color=YELLOW)
        trial.next_to(eqs, DOWN, buff=0.6)
        self.play(FadeIn(trial), run_time=0.5)

        check1 = MathTex(r"1+1+1 = 3 \neq 6", color=RED, font_size=36)
        check1.next_to(trial, DOWN, buff=0.3)
        cross = Text("✗", font_size=48, color=RED)
        cross.next_to(check1, RIGHT, buff=0.3)
        self.play(Write(check1), FadeIn(cross), run_time=1.0)
        self.wait(2.0)

        # Show substitution getting messy
        messy = Text("Substitution gets messy fast...", font_size=32, color=GREY_B)
        messy.next_to(check1, DOWN, buff=0.5)
        self.play(FadeIn(messy), run_time=0.5)
        self.wait(2.0)

        # Clear and show the question
        self.play(
            FadeOut(trial), FadeOut(check1), FadeOut(cross), FadeOut(messy),
            run_time=0.5
        )

        question = Text(
            "Is there a systematic method\nthat always works?",
            font_size=40, color=YELLOW, line_spacing=1.3
        )
        question.next_to(eqs, DOWN, buff=0.6)
        self.play(Write(question), run_time=1.5)
        self.wait(3.0)

        answer = Text("Gaussian Elimination", font_size=48, color=BLUE_C, weight=BOLD)
        answer.next_to(question, DOWN, buff=0.5)
        self.play(FadeIn(answer, scale=1.2), run_time=1.0)

        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
