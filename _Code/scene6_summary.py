"""
Scene 6: Summary and Credits (~30 seconds)
Three takeaways, references, AI disclosure.
"""
from manim import *

class Scene6_Summary(Scene):
    def construct(self):
        import json, os
        dur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "durations.json")
        with open(dur_path) as f:
            durations = json.load(f)
        scene_dur = durations.get("scene6", 30.0)

        header = Text("Key Takeaways", font_size=42, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.6)

        takeaways = VGroup(
            VGroup(
                Text("1.", font_size=30, color=YELLOW),
                Text("Gaussian elimination systematically reduces a system\n   to row echelon form using row operations.", font_size=26, color=WHITE, line_spacing=1.2),
            ).arrange(RIGHT, buff=0.2, aligned_edge=UP),
            VGroup(
                Text("2.", font_size=30, color=YELLOW),
                Text("Row operations never change the solution set.", font_size=26, color=WHITE),
            ).arrange(RIGHT, buff=0.2, aligned_edge=UP),
            VGroup(
                Text("3.", font_size=30, color=YELLOW),
                Text("The solution is the geometric intersection point\n   of all the planes.", font_size=26, color=WHITE, line_spacing=1.2),
            ).arrange(RIGHT, buff=0.2, aligned_edge=UP),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        takeaways.next_to(header, DOWN, buff=0.5)

        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(1.0)

        self.wait(2.0)

        # Transition to credits
        self.play(FadeOut(header), FadeOut(takeaways), run_time=0.5)

        # Thank you
        thanks = Text("Thank you for watching!", font_size=42, color=WHITE, weight=BOLD)
        thanks.to_edge(UP, buff=0.8)
        self.play(Write(thanks), run_time=0.6)

        # References
        refs_header = Text("References", font_size=28, color=YELLOW, weight=BOLD)
        ref1 = Text('Gilbert Strang, "Introduction to Linear Algebra", 5th Ed.', font_size=22, color=GREY_B)
        ref2 = Text('David C. Lay, "Linear Algebra and Its Applications", 6th Ed.', font_size=22, color=GREY_B)
        ref3 = Text('Manim Community Edition Documentation', font_size=22, color=GREY_B)
        refs = VGroup(refs_header, ref1, ref2, ref3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        refs.next_to(thanks, DOWN, buff=0.5).shift(LEFT * 0.5)

        # AI Disclosure
        ai_header = Text("AI Disclosure", font_size=28, color=YELLOW, weight=BOLD)
        ai1 = Text("Script, animation code, and narration were produced", font_size=20, color=GREY_B)
        ai2 = Text("with the help of Claude (Anthropic).", font_size=20, color=GREY_B)
        ai3 = Text("Voice: edge-tts, en-GB-RyanNeural.", font_size=20, color=GREY_B)
        ai4 = Text("All mathematics was checked by the student.", font_size=20, color=GREY_B)
        ai_group = VGroup(ai_header, ai1, ai2, ai3, ai4).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ai_group.next_to(refs, DOWN, buff=0.4)

        self.play(FadeIn(refs), FadeIn(ai_group), run_time=1.0)

        # Wait remaining
        remaining = max(0.2, scene_dur - self.time - 0.5)
        self.wait(remaining)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
