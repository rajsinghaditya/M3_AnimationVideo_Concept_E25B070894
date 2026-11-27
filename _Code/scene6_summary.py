"""
Scene 6: Summary and Credits (~23 seconds)
Three takeaways, references, AI disclosure.
Frame-accurate synchronization with segmented narration audio.
"""
from manim import *
import json, os

class Scene6_Summary(Scene):
    def construct(self):
        seg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio", "segment_durations.json")
        with open(seg_path) as f:
            all_dur = json.load(f)
        segs = all_dur["scene6"]

        header = Text("Key Takeaways", font_size=42, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)

        # ==========================================
        # Segment 1: summary_intro (~3.46s)
        # "To conclude, let us review our three key takeaways:"
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["summary_intro"]

        takeaway1 = VGroup(
            Text("1.", font_size=28, color=YELLOW),
            Text("Systematic Reduction: Row operations reduce any 3×3\n   system to row echelon form step by step.", font_size=24, color=WHITE, line_spacing=1.2),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP)

        takeaway2 = VGroup(
            Text("2.", font_size=28, color=YELLOW),
            Text("Solution Invariance: Row operations are completely safe\n   and preserve the exact solution set.", font_size=24, color=WHITE, line_spacing=1.2),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP)

        takeaway3 = VGroup(
            Text("3.", font_size=28, color=YELLOW),
            Text("Geometric Meaning: The solution is the unique intersection\n   point of the three planes in 3D space.", font_size=24, color=WHITE, line_spacing=1.2),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP)

        takeaways = VGroup(takeaway1, takeaway2, takeaway3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(header, DOWN, buff=0.5)

        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 2: summary_t1 (~6.50s)
        # "First, Gaussian elimination systematically transforms a linear system..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["summary_t1"]
        self.play(FadeIn(takeaway1, shift=RIGHT * 0.3), run_time=0.8)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 3: summary_t2 (~5.52s)
        # "Second, elementary row operations are completely safe and reversible..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["summary_t2"]
        self.play(FadeIn(takeaway2, shift=RIGHT * 0.3), run_time=0.8)
        if self.time < target_t:
            self.wait(target_t - self.time)

        # ==========================================
        # Segment 4: summary_t3 (~5.93s)
        # "Third, the solution has a clear geometric meaning..."
        # ==========================================
        t_start = self.time
        target_t = t_start + segs["summary_t3"]
        self.play(FadeIn(takeaway3, shift=RIGHT * 0.3), run_time=0.8)

        fade_dur = 0.5
        if self.time < target_t - fade_dur:
            self.wait(target_t - fade_dur - self.time)
        self.play(FadeOut(header), FadeOut(takeaways), run_time=fade_dur)

        # ==========================================
        # Segment 5: summary_credits (~1.87s + credits display)
        # "Thank you for watching!" + display references and disclosure
        # ==========================================
        thanks = Text("Thank you for watching!", font_size=40, color=WHITE, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(Write(thanks), run_time=0.6)

        refs_header = Text("References", font_size=26, color=YELLOW, weight=BOLD)
        ref1 = Text('Gilbert Strang, "Introduction to Linear Algebra", 5th Ed.', font_size=20, color=GREY_B)
        ref2 = Text('David C. Lay, "Linear Algebra and Its Applications", 6th Ed.', font_size=20, color=GREY_B)
        ref3 = Text('Manim Community Edition Documentation', font_size=20, color=GREY_B)
        refs = VGroup(refs_header, ref1, ref2, ref3).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        refs.next_to(thanks, DOWN, buff=0.4).shift(LEFT * 0.5)

        ai_header = Text("AI Disclosure", font_size=26, color=YELLOW, weight=BOLD)
        ai1 = Text("Script, animation code, and narration were produced", font_size=19, color=GREY_B)
        ai2 = Text("with the help of Claude (Anthropic).", font_size=19, color=GREY_B)
        ai3 = Text("Voice: F5-TTS Neural Voice Clone (Aditya Raj Singh).", font_size=19, color=GREY_B)
        ai4 = Text("All mathematics was checked by the student.", font_size=19, color=GREY_B)
        ai_group = VGroup(ai_header, ai1, ai2, ai3, ai4).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        ai_group.next_to(refs, DOWN, buff=0.35)

        self.play(FadeIn(refs), FadeIn(ai_group), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
