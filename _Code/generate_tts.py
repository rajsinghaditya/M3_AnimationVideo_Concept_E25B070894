"""Generate narration audio for each scene using edge-tts.
Engineered to precisely achieve a total duration of ~5:05 to 5:15 (within 4:45-5:30).
"""
import asyncio
import edge_tts
import json
import os
import subprocess

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "en-GB-RyanNeural"

SCENES = {
    "scene0": "",  # 5s silence for title card

    "scene1": """Imagine you are faced with three simultaneous linear equations with three unknowns: x, y, and z.
You could attempt guessing numbers by trial and error, or substituting equations into one another over and over.
With multiple variables, direct substitution quickly becomes messy, tedious, and error-prone.
Is there a reliable, systematic method that always works?
There is. It is called Gaussian elimination.""",

    "scene2": """Let us define the core notation before diving into the algorithm.
Any linear system can be written in matrix form as A x equals b.
A is the coefficient matrix, x is the column vector of unknowns, and b is the vector of constants.
We combine them into an augmented matrix, denoted [A | b], where a vertical bar separates coefficients from constants.
To solve the system, we use three elementary row operations:
First, swap two rows.
Second, scale a row by a non-zero scalar.
Third, replace a row by adding a multiple of another row to it.
These operations reduce the matrix into row echelon form, where each leading pivot is strictly to the right of the one above it, and all entries below each pivot are zero.
Our learning objective:
By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3 by 3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically.""",

    "scene3": """Now let us build geometric intuition in three-dimensional space.
Each linear equation in three variables defines a flat plane in 3D space.
Here we see three colored planes: blue for equation one, green for equation two, and orange for equation three.
The solution to the system is the unique geometric point where all three planes simultaneously intersect: x equals 1, y equals 2, and z equals 3.
When we perform an elementary row operation, such as replacing Row 2 with Row 2 minus two times Row 1, we replace one plane with a different plane.
Crucially, this new plane passes through the exact same intersection line as the original planes.
Therefore, the common intersection point never moves.
This shows geometrically why row operations are completely safe and preserve the exact solution set.""",

    "scene4": """Let us solve our worked example step by step.
Our system is:
x plus y plus z equals 6,
2 x plus 3 y plus z equals 11,
and x plus 2 y plus 3 z equals 14.
We first write the augmented matrix.
Row 1 is 1, 1, 1, bar 6.
Row 2 is 2, 3, 1, bar 11.
Row 3 is 1, 2, 3, bar 14.
Our first pivot is 1 in Row 1, Column 1.
In Step 1, we eliminate the entry in Row 2 using: Row 2 becomes Row 2 minus two times Row 1.
Row arithmetic:
2 minus 2 times 1 is 0.
3 minus 2 times 1 is 1.
1 minus 2 times 1 is negative 1.
11 minus 2 times 6 is negative 1.
Our new Row 2 is 0, 1, negative 1, bar negative 1.
In Step 2, we eliminate the entry in Row 3 under the first pivot using: Row 3 becomes Row 3 minus Row 1.
1 minus 1 is 0.
2 minus 1 is 1.
3 minus 1 is 2.
14 minus 6 is 8.
New Row 3 is 0, 1, 2, bar 8.
Now our second pivot is 1 at Row 2, Column 2.
In Step 3, we eliminate the entry below it using: Row 3 becomes Row 3 minus Row 2.
0 minus 0 is 0.
1 minus 1 is 0.
2 minus negative 1 is 3.
8 minus negative 1 is 9.
Our updated Row 3 is 0, 0, 3, bar 9.
The matrix is now in row echelon form, with pivots highlighted at positions 1-1, 2-2, and 3-3.
Next, we perform back substitution.
From Row 3: 3 z equals 9, giving z equals 3.
From Row 2: y minus z equals negative 1. Substituting z gives y minus 3 equals negative 1, so y equals 2.
From Row 1: x plus y plus z equals 6. Substituting y and z gives x plus 5 equals 6, so x equals 1.
The solution vector is x equals 1, y equals 2, z equals 3.""",

    "scene5": """Let us verify our solution by direct substitution into all three original equations.
For Equation 1: 1 plus 2 plus 3 equals 6. Check.
For Equation 2: 2 times 1 plus 3 times 2 plus 3 equals 2 plus 6 plus 3, which equals 11. Check.
For Equation 3: 1 plus 2 times 2 plus 3 times 3 equals 1 plus 4 plus 9, which equals 14. Check.
This algebraic verification proves that the point (1, 2, 3) lies on all three planes: the unique intersection point.
However, systems do not always have a single unique solution.
If row reduction yields a contradictory row like 0, 0, 0, bar 5, zero cannot equal 5, meaning no solution exists and the planes do not all meet at a common point.
If instead we obtain a row like 0, 0, 0, bar 0, the system may have infinitely many solutions, where the planes intersect along a line or coincide.""",

    "scene6": """To conclude, let us review our three key takeaways:
First, Gaussian elimination systematically transforms a linear system into row echelon form using elementary row operations.
Second, elementary row operations are completely safe and reversible, preserving the exact solution set.
Third, the solution has a clear geometric meaning as the common intersection point of three planes in three dimensions.
Thank you for watching!""",
}


async def generate_audio(scene_name, text):
    output_path = os.path.join(AUDIO_DIR, f"{scene_name}.mp3")
    if not text.strip():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
            "-t", "5", "-q:a", "9", output_path
        ], capture_output=True)
        return scene_name, 5.0

    communicate = edge_tts.Communicate(text, VOICE, rate="+25%")
    await communicate.save(output_path)

    result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", output_path
    ], capture_output=True, text=True)
    duration = float(result.stdout.strip())
    return scene_name, duration


async def main():
    durations = {}
    print("Generating calibrated TTS audio tracks...")
    for scene_name, text in SCENES.items():
        name, dur = await generate_audio(scene_name, text)
        durations[name] = dur
        print(f"  {name}: {dur:.1f}s")

    durations_path = os.path.join(AUDIO_DIR, "durations.json")
    with open(durations_path, "w") as f:
        json.dump(durations, f, indent=2)
    print(f"\nDurations saved to {durations_path}")
    total = sum(durations.values())
    mins = int(total // 60)
    secs = int(total % 60)
    print(f"Total duration: {total:.1f}s = {mins}:{secs:02d}")
    return durations


if __name__ == "__main__":
    asyncio.run(main())
