"""
Scene 5: Interpretation (~54 seconds)
Verify solution, link to geometry, show no-solution and infinite-solution cases.
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import json, os

ROW1_COLOR = BLUE_C
ROW2_COLOR = GREEN_C
ROW3_COLOR = ORANGE

class Scene5_Interpretation(Scene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene5"]

        header = Text("Verification & Geometric Meaning", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ==========================================
        # Segment 1: verify_intro (~4.70s)
        # "Let us verify our solution by direct substitution into all three original equations."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_intro"]

        sol_text = MathTex(r"\text{Solution: } (x, y, z) = (1, 2, 3)", font_size=36, color=YELLOW)
        sol_text.next_to(header, DOWN, buff=0.35)
        self.play(Write(sol_text), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 2: verify_eq1 (~4.70s)
        # "For Equation 1: 1 plus 2 plus 3 equals 6. Check."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_eq1"]

        v1 = MathTex(r"1 + 2 + 3 = 6", font_size=36, color=ROW1_COLOR)
        c1 = Text("✓", font_size=38, color=GREEN)
        g1 = VGroup(v1, c1).arrange(RIGHT, buff=0.3).next_to(sol_text, DOWN, buff=0.4)
        self.play(Write(v1), FadeIn(c1, scale=1.3), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 3: verify_eq2 (~7.61s)
        # "For Equation 2: 2 times 1 plus 3 times 2 plus 3 equals 2 plus 6 plus 3, which equals 11. Check."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_eq2"]

        v2 = MathTex(r"2(1) + 3(2) + 3 = 2 + 6 + 3 = 11", font_size=36, color=ROW2_COLOR)
        c2 = Text("✓", font_size=38, color=GREEN)
        g2 = VGroup(v2, c2).arrange(RIGHT, buff=0.3).next_to(g1, DOWN, buff=0.3)
        self.play(Write(v2), FadeIn(c2, scale=1.3), run_time=1.2)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 4: verify_eq3 (~7.73s)
        # "For Equation 3: 1 plus 2 times 2 plus 3 times 3 equals 1 plus 4 plus 9, which equals 14. Check."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_eq3"]

        v3 = MathTex(r"1 + 2(2) + 3(3) = 1 + 4 + 9 = 14", font_size=36, color=ROW3_COLOR)
        c3 = Text("✓", font_size=38, color=GREEN)
        g3 = VGroup(v3, c3).arrange(RIGHT, buff=0.3).next_to(g2, DOWN, buff=0.3)
        self.play(Write(v3), FadeIn(c3, scale=1.3), run_time=1.2)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 5: verify_meaning (~7.03s)
        # "This algebraic verification proves that the point (1, 2, 3) lies on all three planes: the unique intersection point."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_meaning"]

        meaning_text = Text(
            "(1, 2, 3) is the unique geometric point common to all 3 planes",
            font_size=26, color=YELLOW
        ).next_to(g3, DOWN, buff=0.5)
        self.play(FadeIn(meaning_text), run_time=0.8)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(Group(*self.mobjects)), run_time=fade_dur)

        # ==========================================
        # Segment 6: verify_contradiction (~13.51s)
        # "However, systems do not always have a single unique solution. If row reduction yields a contradictory row..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_contradiction"]

        special_header = Text("Special Cases", font_size=38, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(special_header), run_time=0.5)

        no_sol_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & * & * & * \\ 0 & 1 & * & * \\ 0 & 0 & 0 & 5 \end{array}\right]",
            font_size=38
        )
        no_sol_label = Text("Row: 0 = 5  → Contradiction!\nNo common intersection → NO SOLUTION", font_size=24, color=RED, line_spacing=1.3)
        no_sol_group = VGroup(no_sol_mat, no_sol_label).arrange(RIGHT, buff=0.6).next_to(special_header, DOWN, buff=0.6)

        self.play(Write(no_sol_mat), run_time=0.8)
        self.play(FadeIn(no_sol_label), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 7: verify_infinite (~8.93s)
        # "If instead we obtain a row like 0, 0, 0 | 0, the system may have infinitely many solutions..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["verify_infinite"]

        inf_sol_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & * & * & * \\ 0 & 1 & * & * \\ 0 & 0 & 0 & 0 \end{array}\right]",
            font_size=38
        )
        inf_sol_label = Text("Row: 0 = 0  → Free Variable\nPlanes intersect in a line → INFINITE SOLUTIONS", font_size=24, color=TEAL_C, line_spacing=1.3)
        inf_sol_group = VGroup(inf_sol_mat, inf_sol_label).arrange(RIGHT, buff=0.6).next_to(no_sol_group, DOWN, buff=0.5)

        self.play(Write(inf_sol_mat), run_time=0.8)
        self.play(FadeIn(inf_sol_label), run_time=0.8)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(Group(*self.mobjects)), run_time=fade_dur)
