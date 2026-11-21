"""
Scene 1: Hook (~22 seconds)
Show the problem of solving 3 equations at once — trial and error is messy.
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import json, os

class Scene1_Hook(Scene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene1"]

        # ==========================================
        # Segment 1: hook_intro (~5.50s)
        # "Imagine you are faced with three simultaneous linear equations with three unknowns: x, y, and z."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["hook_intro"]

        header = Text("Three equations, three unknowns...", font_size=38, color=WHITE).to_edge(UP, buff=0.6)
        eq1 = MathTex(r"x + y + z = 6", color=BLUE_C, font_size=42)
        eq2 = MathTex(r"2x + 3y + z = 11", color=GREEN_C, font_size=42)
        eq3 = MathTex(r"x + 2y + 3z = 14", color=ORANGE, font_size=42)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35).shift(UP * 0.5)

        self.play(Write(header), run_time=0.8)
        self.play(Write(eqs), run_time=1.8)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 2: hook_messy (~10.10s)
        # "You could attempt guessing numbers by trial and error, or substituting equations into one another..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["hook_messy"]

        trial = Text("Trial: x=1, y=1, z=1?", font_size=32, color=YELLOW).next_to(eqs, DOWN, buff=0.5)
        self.play(FadeIn(trial), run_time=0.6)

        check1 = MathTex(r"1 + 1 + 1 = 3 \neq 6", color=RED, font_size=34).next_to(trial, DOWN, buff=0.25)
        cross = Text("✗", font_size=40, color=RED).next_to(check1, RIGHT, buff=0.25)
        self.play(Write(check1), FadeIn(cross), run_time=0.8)

        messy = Text("Direct substitution gets messy fast...", font_size=30, color=GREY_B).next_to(check1, DOWN, buff=0.35)
        self.play(FadeIn(messy), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 3: hook_question (~6.77s)
        # "Is there a reliable, systematic method that always works? There is. It is called Gaussian elimination."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["hook_question"]

        self.play(
            FadeOut(trial), FadeOut(check1), FadeOut(cross), FadeOut(messy),
            run_time=0.5
        )

        question = Text(
            "Is there a systematic method\nthat always works?",
            font_size=38, color=YELLOW, line_spacing=1.3
        ).next_to(eqs, DOWN, buff=0.5)
        self.play(Write(question), run_time=1.2)

        answer = Text("Gaussian Elimination", font_size=46, color=BLUE_C, weight=BOLD).next_to(question, DOWN, buff=0.4)
        self.play(FadeIn(answer, scale=1.15), run_time=1.0)

        # End of scene transition
        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(Group(*self.mobjects)), run_time=fade_dur)
