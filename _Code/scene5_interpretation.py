"""
Scene 5: Interpretation (~40 seconds)
Verify solution, link to geometry, show no-solution and infinite-solution cases.
"""
from manim import *

ROW1_COLOR = BLUE_C
ROW2_COLOR = GREEN_C
ROW3_COLOR = ORANGE

class Scene5_Interpretation(Scene):
    def construct(self):
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene5", 40.0)

        header = Text("Verification", font_size=42, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=0.6)

        sol_text = MathTex(r"(x, y, z) = (1, 2, 3)", font_size=38, color=YELLOW)
        sol_text.next_to(header, DOWN, buff=0.4)
        self.play(Write(sol_text), run_time=0.6)
        self.wait(0.5)

        # Verification equations
        v1 = MathTex(r"1 + 2 + 3", r"=", r"6", font_size=36, color=ROW1_COLOR)
        check1 = Text("✓", font_size=40, color=GREEN)
        v1_group = VGroup(v1, check1).arrange(RIGHT, buff=0.3)

        v2 = MathTex(r"2(1) + 3(2) + 3", r"=", r"2+6+3", r"=", r"11", font_size=36, color=ROW2_COLOR)
        check2 = Text("✓", font_size=40, color=GREEN)
        v2_group = VGroup(v2, check2).arrange(RIGHT, buff=0.3)

        v3 = MathTex(r"1 + 2(2) + 3(3)", r"=", r"1+4+9", r"=", r"14", font_size=36, color=ROW3_COLOR)
        check3 = Text("✓", font_size=40, color=GREEN)
        v3_group = VGroup(v3, check3).arrange(RIGHT, buff=0.3)

        checks = VGroup(v1_group, v2_group, v3_group).arrange(DOWN, buff=0.35)
        checks.next_to(sol_text, DOWN, buff=0.5)

        for vg in [v1_group, v2_group, v3_group]:
            self.play(Write(vg[0]), run_time=0.8)
            self.play(FadeIn(vg[1], scale=1.5), run_time=0.4)
            self.wait(0.5)

        self.wait(1.5)

        # Intersection point reminder
        intersect_text = Text(
            "The point (1, 2, 3) is where all three planes intersect.",
            font_size=28, color=YELLOW
        )
        intersect_text.next_to(checks, DOWN, buff=0.5)
        self.play(FadeIn(intersect_text), run_time=0.6)
        self.wait(2.0)

        # Clear and show special cases
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # No solution case
        special_header = Text("Special Cases", font_size=38, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(special_header), run_time=0.5)

        no_sol_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & * & * & * \\ 0 & 1 & * & * \\ 0 & 0 & 0 & 5 \end{array}\right]",
            font_size=38
        )
        no_sol_label = Text("→ No solution (contradiction)", font_size=28, color=RED)
        no_sol_group = VGroup(no_sol_mat, no_sol_label).arrange(RIGHT, buff=0.4)
        no_sol_group.next_to(special_header, DOWN, buff=0.6)

        self.play(Write(no_sol_mat), run_time=0.8)
        self.play(FadeIn(no_sol_label), run_time=0.4)
        self.wait(2.0)

        # Infinite solutions case
        inf_sol_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & * & * & * \\ 0 & 1 & * & * \\ 0 & 0 & 0 & 0 \end{array}\right]",
            font_size=38
        )
        inf_sol_label = Text("→ Infinitely many solutions", font_size=28, color=TEAL_C)
        inf_sol_group = VGroup(inf_sol_mat, inf_sol_label).arrange(RIGHT, buff=0.4)
        inf_sol_group.next_to(no_sol_group, DOWN, buff=0.5)

        self.play(Write(inf_sol_mat), run_time=0.8)
        self.play(FadeIn(inf_sol_label), run_time=0.4)

        # Wait remaining
        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
