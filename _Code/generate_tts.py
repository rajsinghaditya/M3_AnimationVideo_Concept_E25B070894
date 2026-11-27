"""
Generate segmented narration audio for each scene using edge-tts.
Segments enable frame-accurate synchronization between spoken words and visual animations.

Total duration target: 4:45 - 5:30 (285s - 330s), never > 7:00.
"""
import asyncio
import edge_tts
import json
import os
import subprocess

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio")
SEGMENTS_DIR = os.path.join(AUDIO_DIR, "segments")
os.makedirs(SEGMENTS_DIR, exist_ok=True)

VOICE = "en-GB-RyanNeural"
RATE = "+25%"  # Precise pacing to land right inside 4:45 - 5:30 (285s - 330s)

SCENE_SEGMENTS = {
    "scene0": [
        ("title_card", "")  # 5s silence for opening title
    ],

    "scene1": [
        ("hook_intro",
         "Imagine you are faced with three simultaneous linear equations with three unknowns: x, y, and z."),
        ("hook_messy",
         "You could attempt guessing numbers by trial and error, or substituting equations into one another. But with multiple variables, direct substitution quickly becomes messy, tedious, and error-prone."),
        ("hook_question",
         "Is there a reliable, systematic method that always works? There is. It is called Gaussian elimination.")
    ],

    "scene2": [
        # LEARNING OBJECTIVE FIRST AS REQUESTED
        ("lo_objective",
         "Here is our central learning objective: By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3 by 3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically."),
        ("matrix_notation",
         "Now, let us define the core notation before diving into the algorithm. Any linear system can be written in matrix form as A x equals b. A is the coefficient matrix, x is the column vector of unknowns, and b is the vector of constants."),
        ("augmented_matrix",
         "We combine A and b into the augmented matrix, denoted [A | b], where a vertical bar cleanly separates coefficients from constants."),
        ("row_operations",
         "To solve the system, we use three elementary row operations: First, swap two rows. Second, scale a row by a non-zero scalar. Third, replace a row by adding a multiple of another row to it."),
        ("row_echelon_form",
         "These operations transform the matrix into row echelon form, where each leading pivot is strictly to the right of the one above it, and all entries below each pivot are zero.")
    ],

    "scene3": [
        ("planes_intro",
         "Now let us build geometric intuition in three-dimensional space. Each linear equation in three variables defines a flat plane in 3D space. Here we see three colored planes: blue for equation one, purple for equation two, and orange for equation three."),
        ("planes_intersection",
         "The solution to the system is the unique geometric point where all three planes simultaneously intersect: x equals 1, y equals 2, and z equals 3."),
        ("planes_invariance",
         "When we perform an elementary row operation, such as replacing Row 2 with Row 2 minus two times Row 1, we replace one plane with a different plane. Crucially, this new plane passes through the exact same intersection line as the original planes. Therefore, the common intersection point never moves. This shows geometrically why row operations are completely safe and preserve the exact solution set.")
    ],

    "scene4": [
        ("worked_system",
         "Let us solve our worked example step by step. Our system is: x plus y plus z equals 6, 2 x plus 3 y plus z equals 11, and x plus 2 y plus 3 z equals 14."),
        ("worked_augmented",
         "We first write the augmented matrix. Row 1 is 1, 1, 1, bar 6. Row 2 is 2, 3, 1, bar 11. And Row 3 is 1, 2, 3, bar 14. Our first pivot is 1 in Row 1, Column 1."),
        ("worked_step1",
         "In Step 1, we eliminate the entry in Row 2 using: Row 2 becomes Row 2 minus two times Row 1. Following the arithmetic: 2 minus 2 times 1 is 0. 3 minus 2 times 1 is 1. 1 minus 2 times 1 is negative 1. And 11 minus 2 times 6 is negative 1. Our new Row 2 is 0, 1, negative 1, bar negative 1."),
        ("worked_step2",
         "In Step 2, we eliminate the entry in Row 3 under the first pivot using: Row 3 becomes Row 3 minus Row 1. 1 minus 1 is 0. 2 minus 1 is 1. 3 minus 1 is 2. And 14 minus 6 is 8. Our new Row 3 is 0, 1, 2, bar 8."),
        ("worked_step3",
         "Now, our second pivot is 1 at Row 2, Column 2. In Step 3, we compute: Row 3 becomes Row 3 minus Row 2. 0 minus 0 is 0. 1 minus 1 is 0. 2 minus negative 1 gives 3. And 8 minus negative 1 gives 9. Our updated Row 3 is 0, 0, 3, bar 9."),
        ("worked_ref",
         "The matrix has now reached row echelon form, featuring an upper-triangular structure with pivots highlighted at positions 1-1, 2-2, and 3-3."),
        ("worked_backsub_z",
         "Next, we perform backward substitution. From Row 3: 3 z equals 9, giving z equals 3."),
        ("worked_backsub_y",
         "From Row 2: y minus z equals negative 1. Substituting z gives y minus 3 equals negative 1, so y equals 2."),
        ("worked_backsub_x",
         "From Row 1: x plus y plus z equals 6. Substituting y and z gives x plus 5 equals 6, so x equals 1."),
        ("worked_solution",
         "Thus, our unique solution vector is x equals 1, y equals 2, and z equals 3.")
    ],

    "scene5": [
        ("verify_intro",
         "Let us verify our solution by direct substitution into all three original equations."),
        ("verify_eq1",
         "For Equation 1: 1 plus 2 plus 3 equals 6. Check."),
        ("verify_eq2",
         "For Equation 2: 2 times 1 plus 3 times 2 plus 3 equals 2 plus 6 plus 3, which equals 11. Check."),
        ("verify_eq3",
         "For Equation 3: 1 plus 2 times 2 plus 3 times 3 equals 1 plus 4 plus 9, which equals 14. Check."),
        ("verify_meaning",
         "This algebraic verification proves that the point (1, 2, 3) lies on all three planes: the unique intersection point."),
        ("verify_contradiction",
         "However, systems do not always have a single unique solution. If row reduction yields a contradictory row like 0, 0, 0, bar 5, zero cannot equal 5, meaning no solution exists and the planes do not all meet at a common point."),
        ("verify_infinite",
         "If instead we obtain a row like 0, 0, 0, bar 0, the system may have infinitely many solutions, where the planes intersect along a line or coincide.")
    ],

    "scene6": [
        ("summary_intro",
         "To conclude, let us review our three key takeaways:"),
        ("summary_t1",
         "First, Gaussian elimination systematically transforms a linear system into row echelon form using elementary row operations."),
        ("summary_t2",
         "Second, elementary row operations are completely safe and reversible, preserving the exact solution set."),
        ("summary_t3",
         "Third, the solution has a clear geometric meaning as the common intersection point of three planes in three dimensions."),
        ("summary_credits",
         "Thank you for watching!")
    ]
}

SCENES = {
    scene: "\n\n".join(text for _, text in segs if text.strip())
    for scene, segs in SCENE_SEGMENTS.items()
}


async def generate_segment(scene_name, seg_id, text):
    out_wav = os.path.join(SEGMENTS_DIR, f"{scene_name}_{seg_id}.wav")
    out_mp3 = os.path.join(SEGMENTS_DIR, f"{scene_name}_{seg_id}.mp3")

    if not text.strip():
        # 5 seconds silence for title card
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", "5.0", out_wav
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return 5.0

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(out_mp3)

    # Convert to standardized 44.1kHz stereo WAV for seamless concatenation
    cmd = [
        "ffmpeg", "-y", "-i", out_mp3,
        "-ar", "44100", "-ac", "2",
        out_wav
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Probe duration
    res = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", out_wav
    ], check=True, capture_output=True, text=True)
    return float(res.stdout.strip())


async def main():
    print("Synthesizing segmented narration with action-level synchronization...")
    segment_durations = {}
    scene_durations = {}

    for scene_name, segments in SCENE_SEGMENTS.items():
        segment_durations[scene_name] = {}
        seg_wavs = []

        for seg_id, text in segments:
            dur = await generate_segment(scene_name, seg_id, text)
            segment_durations[scene_name][seg_id] = dur
            seg_wavs.append(os.path.join(SEGMENTS_DIR, f"{scene_name}_{seg_id}.wav"))
            print(f"  {scene_name} / {seg_id}: {dur:.2f}s")

        # Concatenate segment WAVs into single scene WAV and MP3
        concat_txt = os.path.join(SEGMENTS_DIR, f"{scene_name}_concat.txt")
        with open(concat_txt, "w") as f:
            for w in seg_wavs:
                f.write(f"file '{w}'\n")

        scene_wav = os.path.join(AUDIO_DIR, f"{scene_name}.wav")
        scene_mp3 = os.path.join(AUDIO_DIR, f"{scene_name}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_txt, "-c:a", "pcm_s16le", scene_wav
        ], check=True, capture_output=True)

        subprocess.run([
            "ffmpeg", "-y", "-i", scene_wav,
            "-c:a", "libmp3lame", "-b:a", "192k", scene_mp3
        ], check=True, capture_output=True)

        res = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", scene_wav
        ], check=True, capture_output=True, text=True)
        total_scene_dur = float(res.stdout.strip())
        scene_durations[scene_name] = total_scene_dur
        print(f"--> Total {scene_name}: {total_scene_dur:.2f}s")

    # Save durations
    with open(os.path.join(AUDIO_DIR, "segment_durations.json"), "w") as f:
        json.dump(segment_durations, f, indent=2)
    with open(os.path.join(AUDIO_DIR, "durations.json"), "w") as f:
        json.dump(scene_durations, f, indent=2)

    total_time = sum(scene_durations.values())
    mins = int(total_time // 60)
    secs = int(total_time % 60)
    print(f"\n============================================================")
    print(f"Total Video Narration Duration: {total_time:.2f}s ({mins}:{secs:02d})")
    print(f"Target Window: 4:45 (285s) to 5:30 (330s)")
    if 285.0 <= total_time <= 330.0:
        print("✓ DURATION TARGET MET PERFECTLY!")
    else:
        print(f"Note: Total duration {total_time:.2f}s")
    print(f"============================================================")


if __name__ == "__main__":
    asyncio.run(main())
