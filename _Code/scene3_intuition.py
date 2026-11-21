"""
Scene 3: Visual Intuition (~50 seconds)
3D scene with three planes intersecting at (1,2,3).
"""
from manim import *
import numpy as np

class Scene3_Intuition(ThreeDScene):
    def construct(self):
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene3", 50.0)

        # Set up 3D camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Create axes
        axes = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 5, 1],
            x_length=6, y_length=6, z_length=6,
            axis_config={"include_tip": True, "tip_length": 0.15}
        )
        x_label = axes.get_x_axis_label("x", direction=RIGHT)
        y_label = axes.get_y_axis_label("y", direction=UP)
        z_label = axes.get_z_axis_label("z", direction=OUT)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label), run_time=1.5)

        # Plane 1: x + y + z = 6 => z = 6 - x - y (BLUE)
        plane1 = Surface(
            lambda u, v: axes.c2p(u, v, 6 - u - v),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(10, 10),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(BLUE)

        # Plane 2: 2x + 3y + z = 11 => z = 11 - 2x - 3y (GREEN)
        plane2 = Surface(
            lambda u, v: axes.c2p(u, v, 11 - 2*u - 3*v),
            u_range=[0, 4], v_range=[0, 3],
            resolution=(10, 10),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(GREEN)

        # Plane 3: x + 2y + 3z = 14 => z = (14 - x - 2y)/3 (ORANGE)
        plane3 = Surface(
            lambda u, v: axes.c2p(u, v, (14 - u - 2*v)/3),
            u_range=[0, 4], v_range=[0, 4],
            resolution=(10, 10),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(ORANGE)

        # Labels for planes
        p1_label = MathTex(r"x+y+z=6", font_size=28, color=BLUE_C)
        p2_label = MathTex(r"2x+3y+z=11", font_size=28, color=GREEN_C)
        p3_label = MathTex(r"x+2y+3z=14", font_size=28, color=ORANGE)

        labels = VGroup(p1_label, p2_label, p3_label).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        labels.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(labels)

        self.play(Create(plane1), FadeIn(p1_label), run_time=1.5)
        self.wait(1.0)
        self.play(Create(plane2), FadeIn(p2_label), run_time=1.5)
        self.wait(1.0)
        self.play(Create(plane3), FadeIn(p3_label), run_time=1.5)
        self.wait(2.0)

        # Solution point
        sol_point = Dot3D(axes.c2p(1, 2, 3), color=YELLOW, radius=0.1)
        sol_label = MathTex(r"(1, 2, 3)", font_size=32, color=YELLOW)
        sol_label.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(sol_label)

        self.play(Create(sol_point), FadeIn(sol_label), run_time=1.0)
        self.wait(2.0)

        # Rotate camera to show intersection
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4.0)
        self.stop_ambient_camera_rotation()

        # Show row operation insight
        insight = Text(
            "Row operations replace a plane\nwith one through the SAME point",
            font_size=28, color=YELLOW, line_spacing=1.3
        )
        insight.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(insight)
        self.play(FadeIn(insight), run_time=0.8)

        # Animate plane2 transforming (representing the row operation)
        # New plane: y - z = -1 (the result of R2 - 2R1)
        plane2_new = Surface(
            lambda u, v: axes.c2p(u, v, v + 1),  # z = y + 1 from y - z = -1 => z = y+1 (x free)
            u_range=[0, 4], v_range=[0, 3],
            resolution=(10, 10),
            fill_opacity=0.3,
            stroke_width=0.5,
        ).set_color(GREEN)

        self.play(Transform(plane2, plane2_new), run_time=2.0)
        self.wait(2.0)

        # Show the solution point is still there
        self.play(
            sol_point.animate.set_color(RED).scale(1.5),
            run_time=0.5
        )
        self.play(
            sol_point.animate.set_color(YELLOW).scale(1/1.5),
            run_time=0.5
        )

        safe_text = Text("Solution set never changes!", font_size=32, color=GREEN_C)
        safe_text.next_to(insight, UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(safe_text)
        self.play(FadeIn(safe_text), run_time=0.5)

        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)

        self.play(FadeOut(Group(*self.mobjects)), FadeOut(labels), FadeOut(sol_label),
                  FadeOut(insight), FadeOut(safe_text), run_time=0.5)
