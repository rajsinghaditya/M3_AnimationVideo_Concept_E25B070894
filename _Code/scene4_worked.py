"""
Scene 4: Worked Example (~100 seconds)
Full Gaussian elimination with animated row operations and back substitution.
"""
from manim import *

# Colour scheme
ROW1_COLOR = BLUE_C
ROW2_COLOR = GREEN_C
ROW3_COLOR = ORANGE
PIVOT_COLOR = YELLOW

class Scene4_WorkedExample(Scene):
    def construct(self):
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene4", 100.0)

        header = Text("Worked Example", font_size=42, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # Show the system
        eq1 = MathTex(r"x + y + z = 6", color=ROW1_COLOR, font_size=38)
        eq2 = MathTex(r"2x + 3y + z = 11", color=ROW2_COLOR, font_size=38)
        eq3 = MathTex(r"x + 2y + 3z = 14", color=ROW3_COLOR, font_size=38)
        sys_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.3).next_to(header, DOWN, buff=0.5)
        self.play(Write(sys_group), run_time=1.5)
        self.wait(2.5)

        # Transform to augmented matrix
        arrow = MathTex(r"\Rightarrow", font_size=40)
        arrow.next_to(sys_group, RIGHT, buff=0.3)

        def make_aug_matrix(rows, pos=ORIGIN, scale=1.0):
            """Create an augmented matrix from a 3x4 list of strings."""
            # Build LaTeX string
            entries = r" \\ ".join([" & ".join(row) for row in rows])
            tex = r"\left[\begin{array}{ccc|c} " + entries + r" \end{array}\right]"
            mat = MathTex(tex, font_size=int(40 * scale))
            mat.move_to(pos)
            return mat

        # Clear system and show matrix
        self.play(FadeOut(sys_group), run_time=0.4)

        mat_label = Text("Augmented Matrix", font_size=30, color=GREY_B)
        mat_label.next_to(header, DOWN, buff=0.3)
        self.play(Write(mat_label), run_time=0.5)

        # Initial matrix
        mat0 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=42
        ).next_to(mat_label, DOWN, buff=0.5)

        self.play(Write(mat0), run_time=1.5)
        self.wait(1.5)

        # Highlight first pivot
        # We'll use a surrounding rectangle approach
        pivot_box = SurroundingRectangle(
            mat0[0][1],  # First '1' in the matrix
            color=PIVOT_COLOR, buff=0.08, stroke_width=2
        )
        pivot_label = Text("Pivot", font_size=24, color=PIVOT_COLOR)
        pivot_label.next_to(pivot_box, LEFT, buff=0.3)
        self.play(Create(pivot_box), FadeIn(pivot_label), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(pivot_box), FadeOut(pivot_label), run_time=0.3)

        # ===== STEP 1: R2 <- R2 - 2*R1 =====
        step1_label = MathTex(r"R_2 \leftarrow R_2 - 2R_1", font_size=34, color=GREEN_C)
        step1_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step1_label), run_time=0.8)
        self.wait(1.0)

        # Show arithmetic
        arith1 = VGroup(
            MathTex(r"2-2(1) = 0", font_size=28, color=GREEN_C),
            MathTex(r"3-2(1) = 1", font_size=28, color=GREEN_C),
            MathTex(r"1-2(1) = -1", font_size=28, color=GREEN_C),
            MathTex(r"11-2(6) = -1", font_size=28, color=GREEN_C),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        arith1.next_to(step1_label, DOWN, buff=0.3)
        self.play(FadeIn(arith1), run_time=1.0)
        self.wait(2.5)

        # New matrix after step 1
        mat1 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=42
        ).move_to(mat0.get_center())
        self.play(
            FadeOut(arith1),
            TransformMatchingTex(mat0, mat1),
            run_time=1.0
        )
        self.wait(1.5)

        # ===== STEP 2: R3 <- R3 - R1 =====
        self.play(FadeOut(step1_label), run_time=0.3)
        step2_label = MathTex(r"R_3 \leftarrow R_3 - R_1", font_size=34, color=ORANGE)
        step2_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step2_label), run_time=0.8)
        self.wait(0.5)

        arith2 = VGroup(
            MathTex(r"1-1 = 0", font_size=28, color=ORANGE),
            MathTex(r"2-1 = 1", font_size=28, color=ORANGE),
            MathTex(r"3-1 = 2", font_size=28, color=ORANGE),
            MathTex(r"14-6 = 8", font_size=28, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        arith2.next_to(step2_label, DOWN, buff=0.3)
        self.play(FadeIn(arith2), run_time=1.0)
        self.wait(2.5)

        mat2 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 1 & 2 & 8 \end{array}\right]",
            font_size=42
        ).move_to(mat1.get_center())
        self.play(
            FadeOut(arith2),
            TransformMatchingTex(mat1, mat2),
            run_time=1.0
        )
        self.wait(1.5)

        # ===== STEP 3: R3 <- R3 - R2 =====
        self.play(FadeOut(step2_label), run_time=0.3)
        step3_label = MathTex(r"R_3 \leftarrow R_3 - R_2", font_size=34, color=ORANGE)
        step3_label.to_edge(RIGHT, buff=0.8).shift(UP * 1)
        self.play(Write(step3_label), run_time=0.8)
        self.wait(0.5)

        arith3 = VGroup(
            MathTex(r"0-0 = 0", font_size=28, color=ORANGE),
            MathTex(r"1-1 = 0", font_size=28, color=ORANGE),
            MathTex(r"2-(-1) = 3", font_size=28, color=ORANGE),
            MathTex(r"8-(-1) = 9", font_size=28, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        arith3.next_to(step3_label, DOWN, buff=0.3)
        self.play(FadeIn(arith3), run_time=1.0)
        self.wait(2.5)

        mat3 = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & 3 & 9 \end{array}\right]",
            font_size=42
        ).move_to(mat2.get_center())
        self.play(
            FadeOut(arith3),
            TransformMatchingTex(mat2, mat3),
            run_time=1.0
        )
        self.wait(1.0)

        # Highlight REF label and pivots
        self.play(FadeOut(step3_label), run_time=0.3)
        ref_label = Text("Row Echelon Form ✓", font_size=30, color=PIVOT_COLOR)
        ref_label.to_edge(RIGHT, buff=0.5).shift(UP * 1)
        self.play(Write(ref_label), run_time=0.6)
        self.wait(2.0)

        # ===== BACK SUBSTITUTION =====
        self.play(FadeOut(ref_label), FadeOut(mat_label), run_time=0.3)

        bs_header = Text("Back Substitution", font_size=34, color=WHITE, weight=BOLD)
        bs_header.next_to(header, DOWN, buff=0.3)
        self.play(Write(bs_header), run_time=0.5)

        # Move matrix to left
        self.play(mat3.animate.scale(0.85).to_edge(LEFT, buff=0.8), run_time=0.5)

        # Back sub steps
        step_z = MathTex(r"3z = 9 \implies z = 3", font_size=36, color=ORANGE)
        step_y = MathTex(r"y - z = -1 \implies y = -1 + 3 = 2", font_size=36, color=GREEN_C)
        step_x = MathTex(r"x + y + z = 6 \implies x = 6 - 2 - 3 = 1", font_size=36, color=BLUE_C)

        bs_steps = VGroup(step_z, step_y, step_x).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        bs_steps.next_to(mat3, RIGHT, buff=0.6).shift(DOWN * 0.3)

        self.play(Write(step_z), run_time=1.0)
        self.wait(1.5)
        self.play(Write(step_y), run_time=1.0)
        self.wait(1.5)
        self.play(Write(step_x), run_time=1.0)
        self.wait(1.5)

        # Solution
        sol = MathTex(
            r"(x, y, z) = (1, 2, 3)",
            font_size=44, color=YELLOW
        )
        sol_box = SurroundingRectangle(sol, color=YELLOW, buff=0.15, corner_radius=0.05)
        sol_group = VGroup(sol, sol_box)
        sol_group.next_to(bs_steps, DOWN, buff=0.5)

        self.play(Write(sol), Create(sol_box), run_time=1.0)

        # Wait remaining
        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
