"""
Scene 4: Worked Example (~125 seconds)
Full Gaussian elimination with animated row operations and back substitution.
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import json, os

ROW1_COLOR = BLUE_C
ROW2_COLOR = GREEN_C
ROW3_COLOR = ORANGE
PIVOT_COLOR = YELLOW

class Scene4_WorkedExample(Scene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene4"]

        header = Text("Worked Example", font_size=42, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ==========================================
        # Segment 1: worked_system (~11.06s)
        # "Let us solve our worked example step by step. Our system is: x + y + z = 6..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_system"]

        eq1 = MathTex(r"x + y + z = 6", color=ROW1_COLOR, font_size=38)
        eq2 = MathTex(r"2x + 3y + z = 11", color=ROW2_COLOR, font_size=38)
        eq3 = MathTex(r"x + 2y + 3z = 14", color=ROW3_COLOR, font_size=38)
        sys_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.3).next_to(header, DOWN, buff=0.5)

        self.play(Write(sys_group), run_time=1.8)

        fade_dur = 0.4
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(sys_group), run_time=fade_dur)

        # ==========================================
        # Segment 2: worked_augmented (~15.79s)
        # "We first write the augmented matrix. Row 1 is 1, 1, 1 | 6..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_augmented"]

        mat_label = Text("Augmented Matrix", font_size=30, color=GREY_B).next_to(header, DOWN, buff=0.3)
        self.play(Write(mat_label), run_time=0.5)

        mat0 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=42
        ).next_to(mat_label, DOWN, buff=0.5)
        self.play(Write(mat0), run_time=1.5)

        # First pivot box
        pivot_box1 = SurroundingRectangle(mat0[0][1], color=PIVOT_COLOR, buff=0.08, stroke_width=2.5)
        pivot_lbl1 = Text("Pivot", font_size=24, color=PIVOT_COLOR).next_to(pivot_box1, LEFT, buff=0.3)
        self.play(Create(pivot_box1), FadeIn(pivot_lbl1), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)
        self.play(FadeOut(pivot_box1), FadeOut(pivot_lbl1), run_time=0.3)

        # ==========================================
        # Segment 3: worked_step1 (~21.86s)
        # "In Step 1, we eliminate the entry in Row 2 using: Row 2 becomes Row 2 minus two times Row 1..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_step1"]

        step1_label = MathTex(r"R_2 \leftarrow R_2 - 2R_1", font_size=34, color=GREEN_C)
        step1_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step1_label), run_time=0.8)

        arith1 = VGroup(
            MathTex(r"2 - 2(1) = 0", font_size=28, color=GREEN_C),
            MathTex(r"3 - 2(1) = 1", font_size=28, color=GREEN_C),
            MathTex(r"1 - 2(1) = -1", font_size=28, color=GREEN_C),
            MathTex(r"11 - 2(6) = -1", font_size=28, color=GREEN_C),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(step1_label, DOWN, buff=0.3)
        self.play(FadeIn(arith1), run_time=1.2)

        mat1 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=42
        ).move_to(mat0.get_center())

        step1_trans_t = target_t - 2.0
        if self.time < step1_trans_t:
            self.wait(step1_trans_t - self.time)

        self.play(FadeOut(arith1), TransformMatchingTex(mat0, mat1), run_time=1.0)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 4: worked_step2 (~18.14s)
        # "In Step 2, we eliminate the entry in Row 3 under the first pivot using: Row 3 becomes Row 3 minus Row 1..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_step2"]

        self.play(FadeOut(step1_label), run_time=0.3)
        step2_label = MathTex(r"R_3 \leftarrow R_3 - R_1", font_size=34, color=ORANGE)
        step2_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step2_label), run_time=0.8)

        arith2 = VGroup(
            MathTex(r"1 - 1 = 0", font_size=28, color=ORANGE),
            MathTex(r"2 - 1 = 1", font_size=28, color=ORANGE),
            MathTex(r"3 - 1 = 2", font_size=28, color=ORANGE),
            MathTex(r"14 - 6 = 8", font_size=28, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(step2_label, DOWN, buff=0.3)
        self.play(FadeIn(arith2), run_time=1.2)

        mat2 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 1 & 2 & 8 \end{array}\right]",
            font_size=42
        ).move_to(mat1.get_center())

        step2_trans_t = target_t - 2.0
        if self.time < step2_trans_t:
            self.wait(step2_trans_t - self.time)

        self.play(FadeOut(arith2), TransformMatchingTex(mat1, mat2), run_time=1.0)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 5: worked_step3 (~21.53s)
        # "Now, our second pivot is 1 at Row 2, Column 2. In Step 3, we compute: Row 3 becomes Row 3 minus Row 2..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_step3"]

        self.play(FadeOut(step2_label), run_time=0.3)
        step3_label = MathTex(r"R_3 \leftarrow R_3 - R_2", font_size=34, color=ORANGE)
        step3_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step3_label), run_time=0.8)

        arith3 = VGroup(
            MathTex(r"0 - 0 = 0", font_size=28, color=ORANGE),
            MathTex(r"1 - 1 = 0", font_size=28, color=ORANGE),
            MathTex(r"2 - (-1) = 3", font_size=28, color=ORANGE),
            MathTex(r"8 - (-1) = 9", font_size=28, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(step3_label, DOWN, buff=0.3)
        self.play(FadeIn(arith3), run_time=1.2)

        mat3 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 3 & 9 \end{array}\right]",
            font_size=42
        ).move_to(mat2.get_center())

        step3_trans_t = target_t - 2.0
        if self.time < step3_trans_t:
            self.wait(step3_trans_t - self.time)

        self.play(FadeOut(arith3), TransformMatchingTex(mat2, mat3), run_time=1.0)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 6: worked_ref (~8.14s)
        # "The matrix has now reached row echelon form, featuring an upper-triangular structure with pivots highlighted..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_ref"]

        self.play(FadeOut(step3_label), run_time=0.3)
        ref_label = Text("Row Echelon Form ✓", font_size=32, color=PIVOT_COLOR, weight=BOLD)
        ref_label.to_edge(RIGHT, buff=0.6).shift(UP * 1)
        self.play(Write(ref_label), run_time=0.8)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 7: worked_backsub_z (~6.82s)
        # "Next, we perform backward substitution. From Row 3: 3 z equals 9, giving z equals 3."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_backsub_z"]

        self.play(FadeOut(ref_label), FadeOut(mat_label), run_time=0.3)
        bs_header = Text("Back Substitution", font_size=34, color=WHITE, weight=BOLD).next_to(header, DOWN, buff=0.3)
        self.play(Write(bs_header), run_time=0.5)

        self.play(mat3.animate.scale(0.85).to_edge(LEFT, buff=0.8), run_time=0.6)

        step_z = MathTex(r"3z = 9 \implies z = 3", font_size=36, color=ORANGE)
        step_z.next_to(mat3, RIGHT, buff=0.8).shift(UP * 0.8)
        self.play(Write(step_z), run_time=1.0)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 8: worked_backsub_y (~8.06s)
        # "From Row 2: y minus z equals negative 1. Substituting z gives y minus 3 equals negative 1, so y equals 2."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_backsub_y"]

        step_y = MathTex(r"y - z = -1 \implies y - 3 = -1 \implies y = 2", font_size=34, color=GREEN_C)
        step_y.next_to(step_z, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step_y), run_time=1.2)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 9: worked_backsub_x (~7.80s)
        # "From Row 1: x plus y plus z equals 6. Substituting y and z gives x plus 5 equals 6, so x equals 1."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_backsub_x"]

        step_x = MathTex(r"x + y + z = 6 \implies x + 2 + 3 = 6 \implies x = 1", font_size=34, color=BLUE_C)
        step_x.next_to(step_y, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step_x), run_time=1.2)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 10: worked_solution (~5.62s)
        # "Thus, our unique solution vector is x equals 1, y equals 2, and z equals 3."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["worked_solution"]

        sol = MathTex(r"(x, y, z) = (1, 2, 3)", font_size=42, color=YELLOW)
        sol_box = SurroundingRectangle(sol, color=YELLOW, buff=0.15, corner_radius=0.08)
        sol_group = VGroup(sol, sol_box).next_to(step_x, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(sol), Create(sol_box), run_time=1.0)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(Group(*self.mobjects)), run_time=fade_dur)
