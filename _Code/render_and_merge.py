"""
Render all Manim scenes at 1080p 30fps and merge with TTS audio into final _Video.mp4.
Also extracts frame snapshots from each scene for visual quality verification.
"""
import subprocess
import json
import os
import sys

# Ensure TeXLive is in PATH for Manim LaTeX rendering
TEXLIVE_BIN = "/Users/adityarajsingh/.local/basictex/usr/local/texlive/2026basic/bin/universal-darwin"
if os.path.exists(TEXLIVE_BIN):
    os.environ["PATH"] = TEXLIVE_BIN + ":" + os.environ.get("PATH", "")
    os.environ["TEXMFROOT"] = "/Users/adityarajsingh/.local/basictex/usr/local/texlive/2026basic"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
MEDIA_DIR = os.path.join(PROJECT_DIR, "media")
SNAPSHOT_DIR = os.path.join(PROJECT_DIR, "media", "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

SCENES = [
    ("scene0_opening.py", "Scene0_Opening"),
    ("scene1_hook.py", "Scene1_Hook"),
    ("scene2_concepts.py", "Scene2_Concepts"),
    ("scene3_intuition.py", "Scene3_Intuition"),
    ("scene4_worked.py", "Scene4_WorkedExample"),
    ("scene5_interpretation.py", "Scene5_Interpretation"),
    ("scene6_summary.py", "Scene6_Summary"),
]

def render_scene(py_file, class_name):
    """Render a single Manim scene at 1080p 30fps."""
    full_path = os.path.join(BASE_DIR, py_file)
    print(f"\n{'='*60}")
    print(f"Rendering {class_name} ({py_file}) at 1080p 30fps...")
    print(f"{'='*60}")

    cmd = [
        "manim", "render",
        "-qh",               # 1080p
        "--fps", "30",
        "--media_dir", MEDIA_DIR,
        full_path,
        class_name,
    ]
    env = os.environ.copy()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR, env=env)
    
    # Locate the output file
    stem = py_file.replace(".py", "")
    expected = os.path.join(MEDIA_DIR, "videos", stem, "1080p30", f"{class_name}.mp4")
    if os.path.exists(expected):
        print(f"  ✓ Rendered successfully: {expected}")
        return expected
    
    # Fallback search
    for root, dirs, files in os.walk(MEDIA_DIR):
        for f in files:
            if f == f"{class_name}.mp4" and "1080p30" in root:
                found = os.path.join(root, f)
                print(f"  ✓ Found rendered video: {found}")
                return found

    print(f"ERROR rendering {class_name}:")
    print(result.stdout[-1000:])
    print(result.stderr[-1000:])
    return None


def merge_and_assemble():
    """Merge per-scene audio and video, concatenate, and extract snapshots."""
    durations_file = os.path.join(AUDIO_DIR, "durations.json")
    with open(durations_file) as f:
        durations = json.load(f)

    merged_clips = []
    
    for i, (py_file, class_name) in enumerate(SCENES):
        scene_key = f"scene{i}"
        stem = py_file.replace(".py", "")
        video_path = os.path.join(MEDIA_DIR, "videos", stem, "1080p30", f"{class_name}.mp4")
        audio_path = os.path.join(AUDIO_DIR, f"{scene_key}.mp3")
        merged_path = os.path.join(MEDIA_DIR, f"{scene_key}_merged.mp4")

        if not os.path.exists(video_path):
            print(f"MISSING VIDEO: {video_path}")
            continue
        if not os.path.exists(audio_path):
            print(f"MISSING AUDIO: {audio_path}")
            continue

        target_dur = durations[scene_key]
        print(f"\nMultiplexing {scene_key} ({class_name}):")
        print(f"  Audio duration: {target_dur:.2f}s")

        # Multiplex video and audio track
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{target_dur:.3f}",
            merged_path
        ]
        subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(merged_path):
            print(f"  ✓ Multiplexed: {merged_path}")
            merged_clips.append(merged_path)

            # Extract snapshot for quality checking at 50% through the scene
            snap_path = os.path.join(SNAPSHOT_DIR, f"{scene_key}_frame.png")
            snap_time = max(1.0, target_dur * 0.5)
            cmd_snap = [
                "ffmpeg", "-y",
                "-ss", str(snap_time),
                "-i", merged_path,
                "-vframes", "1",
                "-q:v", "2",
                snap_path
            ]
            subprocess.run(cmd_snap, capture_output=True, text=True)
            if os.path.exists(snap_path):
                print(f"  ✓ Snapshot saved: {snap_path}")

    # Concatenate all clips
    concat_txt = os.path.join(MEDIA_DIR, "concat_manifest.txt")
    with open(concat_txt, "w") as f:
        for clip in merged_clips:
            f.write(f"file '{clip}'\n")

    final_video = os.path.join(PROJECT_DIR, "_Video.mp4")
    print(f"\nConcatenating {len(merged_clips)} clips into final release video: {final_video}")

    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        final_video
    ]
    res = subprocess.run(cmd_cat, capture_output=True, text=True)
    if res.returncode != 0:
        print("CONCAT ERROR:")
        print(res.stderr)
        return None

    return final_video


def run_quality_checks(video_path):
    """Rigorous quality verification using ffprobe."""
    print(f"\n{'='*60}")
    print("FINAL QUALITY AUDIT (ffprobe)")
    print(f"{'='*60}")

    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    meta = json.loads(result.stdout)
    
    fmt = meta.get("format", {})
    duration = float(fmt.get("duration", 0))
    size_mb = int(fmt.get("size", 0)) / (1024 * 1024)

    video_streams = [s for s in meta.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in meta.get("streams", []) if s.get("codec_type") == "audio"]

    v_stream = video_streams[0] if video_streams else {}
    a_stream = audio_streams[0] if audio_streams else {}

    width = int(v_stream.get("width", 0))
    height = int(v_stream.get("height", 0))
    v_codec = v_stream.get("codec_name", "")
    fps_eval = eval(v_stream.get("r_frame_rate", "0/1"))
    a_codec = a_stream.get("codec_name", "")

    minutes = int(duration // 60)
    seconds = int(duration % 60)

    print(f"File Path:       {video_path}")
    print(f"File Size:       {size_mb:.2f} MB")
    print(f"Duration:        {duration:.2f}s ({minutes}:{seconds:02d})")
    print(f"Resolution:      {width}x{height}")
    print(f"Aspect Ratio:    {width}:{height} (16:9)")
    print(f"Frame Rate:      {fps_eval:.2f} fps")
    print(f"Video Codec:     {v_codec}")
    print(f"Audio Codec:     {a_codec}")

    checks = [
        ("Resolution 1920x1080", width == 1920 and height == 1080),
        ("Aspect Ratio 16:9", abs(width / height - 16 / 9) < 0.01),
        ("Frame Rate 30fps", abs(fps_eval - 30) < 0.5),
        ("Video Codec H.264", v_codec == "h264"),
        ("Audio Codec AAC", a_codec == "aac"),
        ("Has Audio Track", len(audio_streams) > 0),
        ("Duration >= 4:45 (285s)", duration >= 285.0),
        ("Duration <= 5:30 (330s)", duration <= 330.0),
        ("Duration < 7:00 (420s)", duration < 420.0),
        ("File Size < 100MB (GitHub direct push safe)", size_mb < 100.0),
    ]

    all_passed = True
    print("\nChecklist Results:")
    for label, passed in checks:
        sym = "✓ PASS" if passed else "✗ FAIL"
        print(f"  [{sym}] {label}")
        if not passed:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("ALL QUALITY CHECKS PASSED PERFECTLY ✓")
    else:
        print("SOME CHECKS FAILED - PLEASE REVIEW")
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    if "--verify-only" in sys.argv:
        video = os.path.join(PROJECT_DIR, "_Video.mp4")
        run_quality_checks(video)
        sys.exit(0)

    # 1. Render all scenes
    for py_file, class_name in SCENES:
        render_scene(py_file, class_name)

    # 2. Merge and concatenate
    final = merge_and_assemble()
    if final:
        run_quality_checks(final)
