"""
Scene 3: Visual Intuition (~43 seconds)
3D scene with three planes intersecting at (1,2,3).
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import numpy as np
import json, os

class Scene3_Intuition(ThreeDScene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene3"]

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Axes setup
        axes = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 5, 1],
            x_length=5.5, y_length=5.5, z_length=5.5,
            axis_config={"include_tip": True, "tip_length": 0.15}
        )
        x_label = axes.get_x_axis_label("x", direction=RIGHT)
        y_label = axes.get_y_axis_label("y", direction=UP)
        z_label = axes.get_z_axis_label("z", direction=OUT)

        # Three planes
        # Plane 1: x + y + z = 6 => z = 6 - x - y (BLUE)
        plane1 = Surface(
            lambda u, v: axes.c2p(u, v, 6 - u - v),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(8, 8),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(BLUE)

        # Plane 2: 2x + 3y + z = 11 => z = 11 - 2x - 3y (GREEN)
        plane2 = Surface(
            lambda u, v: axes.c2p(u, v, 11 - 2*u - 3*v),
            u_range=[0, 4], v_range=[0, 3],
            resolution=(8, 8),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(GREEN)

        # Plane 3: x + 2y + 3z = 14 => z = (14 - x - 2y)/3 (ORANGE)
        plane3 = Surface(
            lambda u, v: axes.c2p(u, v, (14 - u - 2*v)/3),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(8, 8),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(ORANGE)

        p1_label = MathTex(r"x+y+z=6", font_size=28, color=BLUE_C)
        p2_label = MathTex(r"2x+3y+z=11", font_size=28, color=GREEN_C)
        p3_label = MathTex(r"x+2y+3z=14", font_size=28, color=ORANGE)
        labels = VGroup(p1_label, p2_label, p3_label).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        labels.to_corner(UL, buff=0.5)

        # ==========================================
        # Segment 1: planes_intro (~14.21s)
        # "Now let us build geometric intuition in three-dimensional space..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["planes_intro"]

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label), run_time=1.5)
        self.add_fixed_in_frame_mobjects(labels)

        self.play(Create(plane1), FadeIn(p1_label), run_time=2.0)
        self.play(Create(plane2), FadeIn(p2_label), run_time=2.0)
        self.play(Create(plane3), FadeIn(p3_label), run_time=2.0)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 2: planes_intersection (~7.85s)
        # "The solution to the system is the unique geometric point where all three planes simultaneously intersect: (1, 2, 3)."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["planes_intersection"]

        sol_point = Dot3D(axes.c2p(1, 2, 3), color=YELLOW, radius=0.12)
        sol_label = MathTex(r"(1, 2, 3)", font_size=34, color=YELLOW)
        sol_label.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(sol_label)

        self.play(Create(sol_point), FadeIn(sol_label), run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.15)

        rot_wait = max(0.5, target_t - self.time)
        self.wait(rot_wait)
        self.stop_ambient_camera_rotation()

        # ==========================================
        # Segment 3: planes_invariance (~20.52s)
        # "When we perform an elementary row operation... we replace one plane with a different plane... intersection point never moves..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["planes_invariance"]

        insight = Text(
            "Row operations replace a plane\nwith one through the SAME line!",
            font_size=26, color=YELLOW, line_spacing=1.3
        ).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(insight)
        self.play(FadeIn(insight), run_time=1.0)

        # Transform plane2 to y - z = -1 => z = y + 1
        plane2_new = Surface(
            lambda u, v: axes.c2p(u, v, v + 1),
            u_range=[0, 4], v_range=[0, 3],
            resolution=(8, 8),
            fill_opacity=0.35,
            stroke_width=0.5,
        ).set_color(GREEN)

        self.play(Transform(plane2, plane2_new), run_time=2.5)

        # Highlight point remains invariant
        self.play(sol_point.animate.set_color(RED).scale(1.5), run_time=0.6)
        self.play(sol_point.animate.set_color(YELLOW).scale(1/1.5), run_time=0.6)

        safe_text = Text("Solution set never changes!", font_size=30, color=GREEN_C, weight=BOLD)
        safe_text.next_to(insight, UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(safe_text)
        self.play(FadeIn(safe_text), run_time=0.8)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(
            FadeOut(Group(*self.mobjects)),
            FadeOut(labels), FadeOut(sol_label),
            FadeOut(insight), FadeOut(safe_text),
            run_time=fade_dur
        )
