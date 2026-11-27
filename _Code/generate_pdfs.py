"""
Generate all required PDF deliverables using ReportLab:
1. Storyboard.pdf
2. Narration_Script.pdf
3. Code_Walkthrough.pdf
4. Viva_Prep.pdf
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRIMARY_COLOR = colors.HexColor("#1A365D")  # Deep Blue
SECONDARY_COLOR = colors.HexColor("#2B6CB0")  # Blue Accent
DARK_TEXT = colors.HexColor("#2D3748")  # Charcoal
LIGHT_BG = colors.HexColor("#F7FAFC")
ACCENT_PURPLE = colors.HexColor("#7B2CBF")  # Purple accent
ACCENT_ORANGE = colors.HexColor("#C05621")
BORDER_COLOR = colors.HexColor("#E2E8F0")

def setup_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY_COLOR,
        spaceAfter=12,
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY_COLOR,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6,
    )
    
    meta_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
    )
    
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        spaceAfter=6,
    )
    
    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'body': body_style,
        'meta': meta_style,
        'code': code_style,
    }


def add_header_banner(elements, styles, title, doc_type):
    elements.append(Paragraph(title, styles['title']))
    elements.append(Paragraph(f"<b>M3 Internal Assessment Animation Video</b> | {doc_type}", styles['subtitle']))
    
    meta_text = (
        "<b>Student:</b> Aditya Raj Singh &nbsp;|&nbsp; "
        "<b>Student ID:</b> e25b070894 &nbsp;|&nbsp; "
        "<b>Course:</b> Mathematics 3 (Linear Algebra & Calculus) &nbsp;|&nbsp; "
        "<b>Batch:</b> Turing"
    )
    t = Table([[Paragraph(meta_text, styles['meta'])]], colWidths=[7.2 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 14))


def generate_storyboard():
    pdf_path = os.path.join(PROJECT_DIR, "Storyboard.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = setup_styles()
    elements = []
    
    add_header_banner(elements, styles, "Project Storyboard", "Design & Structure")
    
    # Learning Objective Box
    lo_html = (
        "<b>Learning Objective:</b><br/>"
        "<i>\"By the end of this video, the viewer will be able to explain how Gaussian elimination uses "
        "row operations to reduce a 3×3 system to row echelon form, why those operations do not change "
        "the solution set, and what the solution means geometrically.\"</i>"
    )
    t_lo = Table([[Paragraph(lo_html, styles['body'])]], colWidths=[7.2 * inch])
    t_lo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(t_lo)
    elements.append(Spacer(1, 14))
    
    elements.append(Paragraph("6-Scene Production Architecture Table", styles['h1']))
    
    table_data = [
        [
            Paragraph("<b>Scene & Time</b>", styles['meta']),
            Paragraph("<b>Purpose & Goal</b>", styles['meta']),
            Paragraph("<b>Visual Elements & Colour Scheme</b>", styles['meta']),
            Paragraph("<b>Narration Summary</b>", styles['meta']),
            Paragraph("<b>Mathematical Content</b>", styles['meta']),
        ],
        [
            Paragraph("<b>Scene 0</b><br/>Opening Card<br/>(~5s)", styles['body']),
            Paragraph("Set academic context, author metadata, and topic identity.", styles['body']),
            Paragraph("Clean dark slate canvas. High-contrast typography. Professional divider accent line.", styles['body']),
            Paragraph("Silent title card for viewer orientation.", styles['body']),
            Paragraph("M3 IA: Gaussian Elimination on 3×3 Systems.", styles['body']),
        ],
        [
            Paragraph("<b>Scene 1</b><br/>The Hook<br/>(~28-30s)", styles['body']),
            Paragraph("Motivate the necessity of an algorithmic approach over trial & substitution.", styles['body']),
            Paragraph("Three equations in Row 1 Blue, Row 2 Purple, Row 3 Orange. Red cross over failed trial.", styles['body']),
            Paragraph("Demonstrates how trial and error or random substitution collapses into algebraic chaos.", styles['body']),
            Paragraph("Trial: (1,1,1) ⇒ 3 ≠ 6.<br/>Systematic algorithm introduction.", styles['body']),
        ],
        [
            Paragraph("<b>Scene 2</b><br/>Concept Intro<br/>(~60-65s)", styles['body']),
            Paragraph("Define matrix notation, elementary row operations, pivots, and row echelon form.", styles['body']),
            Paragraph("A x = b matrix mapping, augmented matrix [A|b] with partition bar, bulleted operations, learning objective box.", styles['body']),
            Paragraph("Establishes A, x, b, [A|b]. Clarifies swap, scale, and replace. Formulates formal learning objective.", styles['body']),
            Paragraph("Ax = b, augmented matrix [A|b], definition of pivot and Upper Triangular REF.", styles['body']),
        ],
        [
            Paragraph("<b>Scene 3</b><br/>Visual Intuition<br/>(~50s)", styles['body']),
            Paragraph("Deliver 3D geometric interpretation and prove invariance of the solution set.", styles['body']),
            Paragraph("Three 3D intersecting planes (Blue, Purple, Orange) rotated dynamically. Yellow sphere at intersection.", styles['body']),
            Paragraph("Explains that each row operation transforms a plane into another plane through the identical intersection.", styles['body']),
            Paragraph("Planes meeting at unique point (1,2,3). Geometry of row replacement.", styles['body']),
        ],
        [
            Paragraph("<b>Scene 4</b><br/>Worked Example<br/>(~100-110s)", styles['body']),
            Paragraph("Step-by-step Gaussian elimination to REF followed by complete backward substitution.", styles['body']),
            Paragraph("Dynamic matrix transitions. Highlighted yellow pivot boxes. Step-by-step arithmetic displayed to the right.", styles['body']),
            Paragraph("Audible narration walks through arithmetic across every row entry. Explains bottom-up back substitution.", styles['body']),
            Paragraph("R2 ← R2 - 2R1<br/>R3 ← R3 - R1<br/>R3 ← R3 - R2<br/>z=3, y=2, x=1", styles['body']),
        ],
        [
            Paragraph("<b>Scene 5</b><br/>Interpretation<br/>(~40-45s)", styles['body']),
            Paragraph("Rigorous check in original equations; analyze singular & degenerate cases.", styles['body']),
            Paragraph("Equations verified with yellow checkmarks. Augmented matrices showing contradiction [0 0 0 | 5] & free variable [0 0 0 | 0].", styles['body']),
            Paragraph("Verifies solution against original system. Explains no-solution (parallel/inconsistent) and infinite solutions.", styles['body']),
            Paragraph("1+2+3=6 ✓<br/>2+6+3=11 ✓<br/>1+4+9=14 ✓<br/>Contradiction: 0=5<br/>Dependent: 0=0", styles['body']),
        ],
        [
            Paragraph("<b>Scene 6</b><br/>Summary & Credits<br/>(~25-30s)", styles['body']),
            Paragraph("Consolidate key concepts, provide textbook references and AI transparency disclosure.", styles['body']),
            Paragraph("Numbered takeaway cards, structured bibliography citations, institutional academic credits.", styles['body']),
            Paragraph("Three core takeaways: systematic algorithm, solution invariance, and geometric meaning. Concluding remarks.", styles['body']),
            Paragraph("Synthesis of linear system theory, REF transformation, and 3D plane intersection.", styles['body']),
        ],
    ]
    
    t_table = Table(table_data, colWidths=[1.1*inch, 1.4*inch, 1.6*inch, 1.6*inch, 1.5*inch])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_table)
    
    doc.build(elements)
    print("✓ Storyboard.pdf generated")


def generate_narration_script_pdf():
    pdf_path = os.path.join(PROJECT_DIR, "Narration_Script.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = setup_styles()
    elements = []
    
    add_header_banner(elements, styles, "Complete Narration Script", "Voice-Over Transcription")
    
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from generate_tts import SCENES
    
    scene_titles = {
        "scene0": "Scene 0: Opening Title Card (0:00 - 0:05)",
        "scene1": "Scene 1: The Hook — Why Elimination? (0:05 - 0:33)",
        "scene2": "Scene 2: Concept Introduction & Learning Objective (0:33 - 1:39)",
        "scene3": "Scene 3: Visual Intuition & Plane Invariance (1:39 - 2:32)",
        "scene4": "Scene 4: Worked Example & Back Substitution (2:32 - 4:18)",
        "scene5": "Scene 5: Algebraic Verification & Special Cases (4:18 - 5:02)",
        "scene6": "Scene 6: Summary Takeaways & Credits (5:02 - 5:28)",
    }
    
    for scene_id, text in SCENES.items():
        title = scene_titles.get(scene_id, scene_id.upper())
        elements.append(Paragraph(title, styles['h1']))
        
        if not text.strip():
            elements.append(Paragraph("<i>[Silent opening title sequence displaying student metadata, topic name, and academic credentials.]</i>", styles['body']))
        else:
            paragraphs = text.strip().split("\n")
            for p in paragraphs:
                if p.strip():
                    elements.append(Paragraph(p.strip(), styles['body']))
        elements.append(Spacer(1, 10))
        
    doc.build(elements)
    print("✓ Narration_Script.pdf generated")


def generate_code_walkthrough():
    pdf_path = os.path.join(PROJECT_DIR, "Code_Walkthrough.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = setup_styles()
    elements = []
    
    add_header_banner(elements, styles, "Codebase Technical Walkthrough", "Viva Defense & Implementation Guide")
    
    overview_text = (
        "This document provides a comprehensive, plain-English breakdown of all Python code, Manim animation architecture, "
        "and media synthesis pipelines implemented for this project. It is structured to serve as an authoritative viva preparation aid."
    )
    elements.append(Paragraph(overview_text, styles['body']))
    elements.append(Spacer(1, 8))
    
    files = [
        (
            "1. verify_math.py — Rigorous Mathematical Verification Engine",
            "This script serves as the mathematical safety harness for the entire video. Before any graphic is generated, "
            "it establishes NumPy arrays representing matrix A and vector b. It performs elementary row operations sequentially:\n"
            "• R2 ← R2 - 2R1 yields [0, 1, -1 | -1]\n"
            "• R3 ← R3 - R1 yields [0, 1, 2 | 8]\n"
            "• R3 ← R3 - R2 yields [0, 0, 3 | 9]\n"
            "It validates each intermediate row against hard assertions, computes back substitution (z=3, y=2, x=1), "
            "verifies the solution using np.linalg.solve, and checks substitution into all three original equations."
        ),
        (
            "2. generate_tts.py — Asynchronous Neural Voice-Over Synthesizer",
            "Leverages F5-TTS zero-shot neural voice cloning to generate natural, crystal-clear narration matching student Aditya Raj Singh's exact voice sample. "
            "narration. The script defines precise per-scene speech scripts calibrated to match target pacing. "
            "Crucially, it executes asynchronously, writes MP3 files for scenes 0 through 6, and measures exact durations with ffprobe, "
            "saving a durations.json file that drives all Manim scene run times."
        ),
        (
            "3. scene0_opening.py — Academic Title Card (Scene 0)",
            "Constructed using Manim's Text mobjects with clean, modern typography. It displays the title 'Gaussian Elimination', "
            "subtitle 'Solving a 3×3 System of Linear Equations', course title, student name (Aditya Raj Singh), and ID (e25b070894). "
            "It reads its exact wait duration dynamically from durations.json to ensure flawless synchronization."
        ),
        (
            "4. scene1_hook.py — Conceptual Hook (Scene 1)",
            "Animates the three equations color-coded by row (Blue, Purple, Orange). Shows a trial guess (x=1, y=1, z=1) failing "
            "with a red cross (1+1+1=3 ≠ 6), illustrates the hazard of messy substitution, and dramatically introduces "
            "'Gaussian Elimination' as the systematic method that always works."
        ),
        (
            "5. scene2_concepts.py — Notation & Learning Objective (Scene 2)",
            "Transitions smoothly from simultaneous equations to matrix form Ax = b and augmented matrix [A | b] with a partition bar. "
            "Animates the three elementary row operations (Swap, Scale, Replace), defines pivots and Row Echelon Form (REF), "
            "and highlights the exact required learning objective inside a prominent styled border."
        ),
        (
            "6. scene3_intuition.py — 3D Geometric Plane Intersection (Scene 3)",
            "Inherits from Manim's ThreeDScene. Plots three distinct surfaces representing the three equations in 3D coordinate space. "
            "A yellow 3D sphere highlights the unique intersection point (1, 2, 3). Camera orientation and ambient rotation provide depth. "
            "Crucially, it transforms plane 2 according to R2 ← R2 - 2R1, visually demonstrating that the new plane continues passing through "
            "the exact same intersection line, proving that row operations preserve the solution set."
        ),
        (
            "7. scene4_worked.py — Core Worked Example (Scene 4)",
            "The heart of the computational demonstration. Animate the augmented matrix with row color-coding. Highlights each pivot "
            "with a glowing yellow box. Shows the explicit arithmetic on the right-hand side for every single entry during R2 ← R2 - 2R1, "
            "R3 ← R3 - R1, and R3 ← R3 - R2. Once REF is achieved, the matrix shifts left, and step-by-step backward substitution unfolds "
            "bottom-up: z = 3, y = 2, x = 1, culminating in the boxed solution vector (1, 2, 3)."
        ),
        (
            "8. scene5_interpretation.py — Verification & Degenerate Cases (Scene 5)",
            "Plugs (1, 2, 3) back into Equations 1, 2, and 3 with dynamic yellow checkmarks. Connects this back to the geometric intersection. "
            "Then introduces the two fundamental alternative outcomes: inconsistent systems exhibiting a contradictory row [0 0 0 | 5] "
            "(parallel or non-intersecting planes), and dependent systems exhibiting a row of zeros [0 0 0 | 0] (infinite solutions)."
        ),
        (
            "9. scene6_summary.py — Synthesis, References & AI Disclosure (Scene 6)",
            "Presents the three foundational takeaways on staggered cards, displays academic literature citations (Gilbert Strang, "
            "David C. Lay, and Manim CE), and presents the mandatory AI disclosure statement acknowledging Claude (Anthropic) for "
            "scripting and animation assistance with full mathematical validation by the student."
        ),
        (
            "10. render_and_merge.py — Full Render, Audio-Video Stitching & Quality Inspection",
            "Automates end-to-end rendering: renders all scenes at 1080p 30fps with Manim, combines each scene video with its "
            "corresponding neural audio track using FFmpeg, concatenates clips using the demuxer, encodes to H.264/AAC with faststart, "
            "and runs strict ffprobe quality checks validating 1920×1080 resolution, 16:9 aspect ratio, audio stream integrity, and total duration."
        ),
    ]
    
    for title, desc in files:
        elements.append(Paragraph(title, styles['h1']))
        elements.append(Paragraph(desc.replace("\n", "<br/>"), styles['body']))
        elements.append(Spacer(1, 4))
        
    doc.build(elements)
    print("✓ Code_Walkthrough.pdf generated")


def generate_viva_prep():
    pdf_path = os.path.join(PROJECT_DIR, "Viva_Prep.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = setup_styles()
    elements = []
    
    add_header_banner(elements, styles, "Viva Voce Comprehensive Preparation Guide", "15 High-Probability Questions & Model Answers")
    
    questions = [
        (
            "Q1: What is the fundamental difference between Row Echelon Form (REF) and Reduced Row Echelon Form (RREF)?",
            "In Row Echelon Form (REF), each pivot is to the right of the pivot in the row above, all entries below pivots are zero, "
            "and any all-zero rows are at the bottom. In Reduced Row Echelon Form (RREF), an additional condition requires that each pivot "
            "equals 1 and is the ONLY non-zero entry in its entire column (entries above pivots are also zero). Gaussian elimination produces REF; "
            "Gauss-Jordan elimination continues to RREF."
        ),
        (
            "Q2: Mathematically, why do elementary row operations preserve the solution set of a linear system?",
            "Elementary row operations correspond to multiplying the augmented matrix by elementary matrices E, which are strictly invertible. "
            "Because each elementary operation can be reversed by an inverse elementary operation of the same class (swapping back, scaling by 1/c, "
            "or subtracting the added multiple), the solution space of EAx = Eb is identical to that of Ax = b."
        ),
        (
            "Q3: What is the geometric interpretation of a 3×3 system of linear equations?",
            "Each linear equation a_i x + b_i y + c_i z = d_i represents a flat two-dimensional plane in three-dimensional Euclidean space R³. "
            "Solving the system corresponds to finding the geometric intersection of the three planes. A unique solution is a single point of concurrence; "
            "infinitely many solutions correspond to intersection along a line or identical planes; no solution means the planes do not share any common point."
        ),
        (
            "Q4: What happens geometrically when a row replacement operation R2 ← R2 - 2R1 is applied?",
            "The equation represented by R2 is replaced by a linear combination of R1 and R2. Geometrically, any point that lies on both Plane 1 and Plane 2 "
            "satisfies this new equation. Thus, the new plane belongs to the 'pencil' (or sheaf) of planes passing through the intersection line of Plane 1 and Plane 2. "
            "Since the intersection locus is preserved, the point common to all three planes remains invariant."
        ),
        (
            "Q5: How do you detect an inconsistent system from its augmented matrix during Gaussian elimination?",
            "An inconsistent system reveals itself when row operations produce a row of the form [0 0 0 | k] where k ≠ 0. "
            "This corresponds to the algebraic equation 0x + 0y + 0z = k, or 0 = k, which is an impossible contradiction. "
            "Geometrically, this signifies that the planes have no common intersection point (e.g., parallel planes or triangular prism configuration)."
        ),
        (
            "Q6: How do you detect infinitely many solutions and identify free variables?",
            "If elimination yields a row of all zeros [0 0 0 | 0] without contradictions, and the number of non-zero pivot rows r is strictly less than "
            "the number of variables n (here r < 3), there are n - r free variables. Variables without pivot columns become free parameters (e.g., z = t), "
            "leading to a parametric line or plane of solutions."
        ),
        (
            "Q7: Why did you choose Row 1 Blue, Row 2 Purple, and Row 3 Orange in your animation?",
            "Consistent color mapping reduces cognitive load. By coloring each row's algebraic equation, its row in the augmented matrix, and its corresponding "
            "plane in the 3D scene identically (Row 1 Blue, Row 2 Purple, Row 3 Orange), the viewer instantly maps algebraic transformations to geometric entities. "
            "Yellow is reserved exclusively for focal highlights: pivots, solution boxes, and intersection points."
        ),
        (
            "Q8: How did you handle synchronization between the spoken narration and visual animations?",
            "I used an 'audio-first' synthesis architecture. The voice-over audio was generated first using F5-TTS neural voice cloning from student Aditya Raj Singh's voice sample, and its precise duration was extracted "
            "using ffprobe down to the millisecond into durations.json. Each Manim scene reads this file and computes dynamic wait intervals (self.wait) so that "
            "on-screen text transitions and matrix highlights occur in perfect synchrony with the voice."
        ),
        (
            "Q9: What is partial pivoting, and why was it not required in this specific worked example?",
            "Partial pivoting is the technique of swapping rows to place the entry with the largest absolute value in the pivot position before eliminating below. "
            "It avoids division by zero and minimizes numerical roundoff error in floating-point computation. In our worked example, the (1,1) entry was already 1 "
            "and the (2,2) entry was 1 after step 1, so no row swap was necessary to proceed cleanly."
        ),
        (
            "Q10: What is the computational complexity of Gaussian elimination on an n×n system?",
            "Gaussian elimination requires approximately (2/3)n³ arithmetic operations (floating-point additions and multiplications) for the forward elimination phase, "
            "and approximately n² operations for backward substitution. For large systems, forward elimination dominates the computational budget."
        ),
        (
            "Q11: In Scene 4, what is the exact sequence of elementary row operations performed?",
            "1. R2 ← R2 - 2R1: transforms [2 3 1 | 11] into [0 1 -1 | -1]\n"
            "2. R3 ← R3 - R1: transforms [1 2 3 | 14] into [0 1 2 | 8]\n"
            "3. R3 ← R3 - R2: transforms [0 1 2 | 8] into [0 0 3 | 9]\n"
            "This achieves the upper-triangular Row Echelon Form."
        ),
        (
            "Q12: How does backward substitution work once the matrix is in REF?",
            "Backward substitution proceeds bottom-up from the lowest non-zero row:\n"
            "• From Row 3: 3z = 9 ⇒ z = 3\n"
            "• From Row 2: y - z = -1 ⇒ y - 3 = -1 ⇒ y = 2\n"
            "• From Row 1: x + y + z = 6 ⇒ x + 2 + 3 = 6 ⇒ x = 1\n"
            "Each solved variable is substituted directly into upper rows."
        ),
        (
            "Q13: Why is NumPy verification performed before rendering animations?",
            "To guarantee zero mathematical or transcription error on screen. The verify_math.py script simulates the exact row operations using NumPy arrays, "
            "asserts that intermediate rows match expected analytical outputs, checks against np.linalg.solve(A, b), and tests back-substitution into all equations. "
            "Only verified numbers enter the Manim animation scripts."
        ),
        (
            "Q14: How does 3D camera motion in Scene 3 enhance the viewer's understanding?",
            "A static 2D projection of three 3D planes can obscure where they intersect due to depth ambiguity. By rotating the camera (phi=70°, theta=-45° with "
            "ambient rotation), parallax allows the human visual system to perceive the 3D planes and observe that all three surfaces indeed concur at the single "
            "yellow point (1, 2, 3)."
        ),
        (
            "Q15: What tools and technologies comprise the production pipeline of this project?",
            "• Manim Community Edition (v0.22.1) for programmatic 2D/3D mathematical animations\n"
            "• Python 3 with NumPy for numerical verification\n"
            "• F5-TTS Neural Voice Cloning (matching student Aditya Raj Singh's voice sample) for authentic narration\n"
            "• FFmpeg for H.264/AAC video rendering, audio-video multiplexing, and format compliance\n"
            "• ReportLab for generating professional assessment PDF documentation."
        ),
    ]
    
    for q, a in questions:
        q_box = Table([
            [Paragraph(f"<b>{q}</b>", styles['h2'])],
            [Paragraph(a.replace("\n", "<br/>"), styles['body'])]
        ], colWidths=[7.0 * inch])
        q_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(q_box)
        elements.append(Spacer(1, 6))
        
    doc.build(elements)
    print("✓ Viva_Prep.pdf generated")


if __name__ == "__main__":
    generate_storyboard()
    generate_narration_script_pdf()
    generate_code_walkthrough()
    generate_viva_prep()
