"""
Scene 2: Concept Introduction (~54 seconds)
Define notation: Learning Objective first, then Ax=b, augmented matrix, row operations, pivot, REF.
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import json, os

class Scene2_Concepts(Scene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene2"]

        # ==========================================
        # Segment 1: lo_objective (~13.61s)
        # LEARNING OBJECTIVE SHOWN FIRST AS REQUESTED
        # "Here is our central learning objective: By the end of this video, the viewer will be able to explain..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["lo_objective"]

        lo_header = Text("Learning Objective", font_size=42, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.8)
        lo_text = Text(
            "By the end of this video, the viewer will be able to explain\n"
            "how Gaussian elimination uses row operations to reduce a\n"
            "3×3 system to row echelon form, why those operations do\n"
            "not change the solution set, and what the solution means\n"
            "geometrically.",
            font_size=28,
            color=WHITE,
            line_spacing=1.4,
        ).next_to(lo_header, DOWN, buff=0.5)

        lo_box = SurroundingRectangle(lo_text, color=BLUE_C, buff=0.35, corner_radius=0.1)

        self.play(Write(lo_header), run_time=0.8)
        self.play(FadeIn(lo_text), Create(lo_box), run_time=1.5)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(lo_header), FadeOut(lo_text), FadeOut(lo_box), run_time=fade_dur)

        # ==========================================
        # Segment 2: matrix_notation (~12.98s)
        # "Now, let us define the core notation before diving into the algorithm. Any linear system can be written..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["matrix_notation"]

        header = Text("Matrix Notation", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.6)

        sys_eq = MathTex(
            r"x + y + z &= 6 \\",
            r"2x + 3y + z &= 11 \\",
            r"x + 2y + 3z &= 14",
            font_size=36
        ).shift(LEFT * 3 + UP * 0.4)
        sys_eq[0].set_color(BLUE_C)
        sys_eq[1].set_color(GREEN_C)
        sys_eq[2].set_color(ORANGE)

        self.play(Write(sys_eq), run_time=1.2)

        arrow = MathTex(r"\Rightarrow", font_size=44).next_to(sys_eq, RIGHT, buff=0.5)
        ax_eq = MathTex(r"A", r"\vec{x}", r"=", r"\vec{b}", font_size=46)
        ax_eq.next_to(arrow, RIGHT, buff=0.5)
        ax_eq[0].set_color(YELLOW)
        ax_eq[1].set_color(WHITE)
        ax_eq[3].set_color(TEAL_C)

        self.play(Write(arrow), Write(ax_eq), run_time=0.8)

        a_label = Text("coefficient\nmatrix", font_size=20, color=YELLOW).next_to(ax_eq[0], DOWN, buff=0.3)
        x_label = Text("unknowns", font_size=20, color=WHITE).next_to(ax_eq[1], DOWN, buff=0.3)
        b_label = Text("constants", font_size=20, color=TEAL_C).next_to(ax_eq[3], DOWN, buff=0.3)
        self.play(FadeIn(a_label), FadeIn(x_label), FadeIn(b_label), run_time=0.8)

        fade_dur = 0.4
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(
            FadeOut(sys_eq), FadeOut(arrow), FadeOut(ax_eq),
            FadeOut(a_label), FadeOut(x_label), FadeOut(b_label),
            run_time=fade_dur
        )

        # ==========================================
        # Segment 3: augmented_matrix (~7.32s)
        # "We combine A and b into the augmented matrix, denoted [A | b]..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["augmented_matrix"]

        aug_header = Text("Augmented Matrix  [A | b]", font_size=34, color=WHITE)
        aug_header.next_to(header, DOWN, buff=0.5)
        aug_mat = MathTex(
            r"\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]",
            font_size=42
        ).next_to(aug_header, DOWN, buff=0.5)

        self.play(Write(aug_header), Write(aug_mat), run_time=1.4)

        fade_dur = 0.4
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(aug_header), FadeOut(aug_mat), run_time=fade_dur)

        # ==========================================
        # Segment 4: row_operations (~11.66s)
        # "To solve the system, we use three elementary row operations: First, swap two rows..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["row_operations"]

        new_header = Text("Elementary Row Operations", font_size=36, color=WHITE, weight=BOLD)
        new_header.next_to(header, DOWN, buff=0.4)
        self.play(Write(new_header), run_time=0.6)

        ops = VGroup(
            VGroup(
                Text("1. ", font_size=28, color=YELLOW),
                Text("Swap", font_size=28, color=YELLOW, weight=BOLD),
                Text(" two rows", font_size=28, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("2. ", font_size=28, color=YELLOW),
                Text("Scale", font_size=28, color=YELLOW, weight=BOLD),
                Text(" a row by a nonzero constant", font_size=28, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("3. ", font_size=28, color=YELLOW),
                Text("Replace", font_size=28, color=YELLOW, weight=BOLD),
                Text(" a row by adding a multiple of another", font_size=28, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(new_header, DOWN, buff=0.5)

        for op in ops:
            self.play(FadeIn(op, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.6)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 5: row_echelon_form (~8.06s)
        # "These operations transform the matrix into row echelon form..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["row_echelon_form"]

        ref_text = Text("Row Echelon Form (REF)", font_size=32, color=TEAL_C, weight=BOLD)
        ref_text.next_to(ops, DOWN, buff=0.5)

        ref_desc = VGroup(
            Text("• Each pivot is strictly to the right of the one above", font_size=24, color=WHITE),
            Text("• All entries below each pivot are zero", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ref_text, DOWN, buff=0.25)

        self.play(Write(ref_text), FadeIn(ref_desc), run_time=1.2)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(Group(*self.mobjects)), run_time=fade_dur)
