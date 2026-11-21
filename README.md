# Gaussian Elimination: Solving a 3×3 System of Linear Equations

**Mathematics 3 (Linear Algebra and Calculus) — Internal Assessment Animation Project**  
**Student:** Aditya Raj Singh  
**Student ID:** `e25b070894`  
**Batch:** Turing  
**Repository:** [https://github.com/rajsinghaditya/M3_AnimationVideo_Concept_E25B070894](https://github.com/rajsinghaditya/M3_AnimationVideo_Concept_E25B070894)

---

## 🎯 Learning Objective

> *"By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3×3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically."*

---

## 📹 Video Specifications & Compliance

| Parameter | Specification | Achieved Metric | Status |
| :--- | :--- | :--- | :--- |
| **Resolution** | 1920×1080 (Full HD) | 1920×1080 | ✅ Compliant |
| **Aspect Ratio** | 16:9 widescreen | 16:9 | ✅ Compliant |
| **Frame Rate** | 30 fps | 30.00 fps | ✅ Compliant |
| **Video Codec** | H.264 (AVC) | `h264` (Main / High profile, yuv420p) | ✅ Compliant |
| **Audio Codec** | AAC (stereo, 192 kbps) | `aac`, 44.1 kHz, 192 kbps | ✅ Compliant |
| **Target Duration** | 4:45 – 5:30 (< 7:00 strict max) | **5:26** (326.2 seconds) | ✅ Compliant |
| **File Size** | < 100 MB (GitHub direct push safe) | **14.93 MB** | ✅ Compliant |
| **Visual Palette** | Row 1 Blue, Row 2 Green, Row 3 Orange, Pivots Yellow | Consistent throughout all 2D/3D scenes | ✅ Compliant |

---

## 🧮 Mathematical Problem & Verified Solution

### Given 3×3 Linear System:
$$\begin{aligned}
x + y + z &= 6 \\
2x + 3y + z &= 11 \\
x + 2y + 3z &= 14
\end{aligned}$$

### Initial Augmented Matrix $[A \mid \vec{b}]$:
$$\left[\begin{array}{ccc|c}
1 & 1 & 1 & 6 \\
2 & 3 & 1 & 11 \\
1 & 2 & 3 & 14
\end{array}\right]$$

### Gaussian Elimination Steps:
1. **$R_2 \leftarrow R_2 - 2R_1$**:
   $$\left[\begin{array}{ccc|c}
   1 & 1 & 1 & 6 \\
   0 & 1 & -1 & -1 \\
   1 & 2 & 3 & 14
   \end{array}\right]$$
2. **$R_3 \leftarrow R_3 - R_1$**:
   $$\left[\begin{array}{ccc|c}
   1 & 1 & 1 & 6 \\
   0 & 1 & -1 & -1 \\
   0 & 1 & 2 & 8
   \end{array}\right]$$
3. **$R_3 \leftarrow R_3 - R_2$**:
   $$\left[\begin{array}{ccc|c}
   1 & 1 & 1 & 6 \\
   0 & 1 & -1 & -1 \\
   0 & 0 & 3 & 9
   \end{array}\right] \quad \text{(Row Echelon Form)}$$

### Backward Substitution:
- From Row 3: $3z = 9 \implies \mathbf{z = 3}$
- From Row 2: $y - z = -1 \implies y - 3 = -1 \implies \mathbf{y = 2}$
- From Row 1: $x + y + z = 6 \implies x + 2 + 3 = 6 \implies \mathbf{x = 1}$

$$\mathbf{(x, y, z) = (1, 2, 3)}$$

### Substitution Check (shown on screen in Scene 5):
- **Equation 1:** $1 + 2 + 3 = 6$ ✅
- **Equation 2:** $2(1) + 3(2) + 3 = 2 + 6 + 3 = 11$ ✅
- **Equation 3:** $1 + 2(2) + 3(3) = 1 + 4 + 9 = 14$ ✅

---

## 🎬 6-Scene Structure

- **Scene 0: Opening Title Card (~5s)** — Title, subtitle, student metadata, course, and institutional identity.
- **Scene 1: The Hook (~23s)** — Motivation for systematic elimination; why trial & random substitution fail.
- **Scene 2: Concept Introduction (~53s)** — $A\vec{x} = \vec{b}$, augmented matrix $[A \mid \vec{b}]$, 3 elementary row operations, pivots, Row Echelon Form (REF), and on-screen learning objective.
- **Scene 3: Visual Intuition (~42s)** — 3D camera view with three planes intersecting at $(1, 2, 3)$; geometric proof that row operations replace planes while strictly preserving their common intersection.
- **Scene 4: Worked Example (~124s)** — Full step-by-step Gaussian elimination with highlighted pivots, row-by-row arithmetic callouts, transformation to REF, and backward substitution.
- **Scene 5: Interpretation & Special Cases (~54s)** — Full algebraic verification in all three original equations, geometric meaning, contradictory row $[0\ 0\ 0 \mid 5]$ (inconsistent / no solution), and zero row $[0\ 0\ 0 \mid 0]$ (infinitely many solutions).
- **Scene 6: Summary & Credits (~23s)** — Three fundamental takeaways, textbook citations, and AI transparency disclosure.

---

## 📂 Repository Contents

```
├── _Video.mp4              # Final 1080p narrated animation video (~5:22)
├── Storyboard.pdf          # Full project storyboard with 6-scene production table
├── Narration_Script.pdf    # Complete voice-over transcript for all scenes
├── Code_Walkthrough.pdf    # Comprehensive code explanation & viva defense guide
├── Viva_Prep.pdf           # 15 high-probability viva questions and model answers
├── README.md               # This project documentation
└── _Code/                  # Complete source code directory
    ├── verify_math.py          # NumPy numerical verification & assertion suite
    ├── generate_tts.py         # Asynchronous neural TTS audio generator (edge-tts)
    ├── generate_pdfs.py        # ReportLab PDF documentation generator
    ├── render_and_merge.py     # Automated Manim render, audio multiplexer & ffprobe validator
    ├── scene0_opening.py       # Scene 0: Academic title card
    ├── scene1_hook.py          # Scene 1: Conceptual hook
    ├── scene2_concepts.py      # Scene 2: Notation, row operations & learning objective
    ├── scene3_intuition.py     # Scene 3: 3D planes intersection & invariance proof
    ├── scene4_worked.py        # Scene 4: Worked Gaussian elimination & back substitution
    ├── scene5_interpretation.py# Scene 5: Verification & singular/infinite cases
    ├── scene6_summary.py       # Scene 6: Key takeaways & credits
    ├── narration_script.txt    # Plaintext narration transcription
    └── requirements.txt        # Python dependency specifications
```

---

## 🛠️ Tools & Technologies Used

- **Animation Engine:** [Manim Community Edition](https://www.manim.community/) (v0.22.1)
- **Math Typesetting:** LaTeX (TeXLive / BasicTeX engine) with `MathTex`
- **Voice Synthesis:** [edge-tts](https://github.com/rany2/edge-tts) (Microsoft Neural Voice: `en-GB-RyanNeural`)
- **Numerical Verification:** NumPy (`verify_math.py` with hard assertions and `np.linalg.solve`)
- **Video & Audio Multiplexing:** FFmpeg (libx264, AAC, faststart container)
- **PDF Publishing:** ReportLab 5.1

---

## 🔄 How to Reproduce & Re-Render

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rajsinghaditya/M3_AnimationVideo_Concept_E25B070894.git
   cd M3_AnimationVideo_Concept_E25B070894
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r _Code/requirements.txt
   ```

3. **Verify mathematics:**
   ```bash
   python3 _Code/verify_math.py
   ```

4. **Generate narration audio:**
   ```bash
   python3 _Code/generate_tts.py
   ```

5. **Generate documentation PDFs:**
   ```bash
   python3 _Code/generate_pdfs.py
   ```

6. **Render animations and merge final video:**
   ```bash
   python3 _Code/render_and_merge.py
   ```

The compiled video will be saved directly to `_Video.mp4`.

---

## 📚 References

1. **Gilbert Strang**, *Introduction to Linear Algebra*, 5th Edition, Wellesley-Cambridge Press, 2016.
2. **David C. Lay, Steven R. Lay, Judi J. McDonald**, *Linear Algebra and Its Applications*, 6th Edition, Pearson, 2021.
3. **Manim Community Developers**, *Manim Community Edition Documentation*, [https://docs.manim.community/](https://docs.manim.community/).

---

## 🤖 AI Transparency Disclosure

*Script, animation code, documentation, and narration were produced with the assistance of Claude (Anthropic). Voice: edge-tts (`en-GB-RyanNeural`). All mathematical proofs, numerical steps, and theoretical consistency were thoroughly reviewed and verified by the student.*
