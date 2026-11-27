"""
Autonomous Local Neural Voice Cloning and Production Pipeline.
Clones student Aditya Raj Singh's voice using F5-TTS on Apple Silicon MPS,
generates frame-accurate synchronized narration segments, updates Manim scenes,
assembles final video, regenerates academic PDFs, and audits quality.
"""
import os
import sys
import json
import torch
import soundfile as sf
import subprocess
from pathlib import Path
from importlib.resources import files
from omegaconf import OmegaConf
from cached_path import cached_path
from hydra.utils import get_class

from f5_tts.infer.utils_infer import (
    load_model,
    load_vocoder,
    preprocess_ref_audio_text,
    infer_process,
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
CLONED_SEGMENTS_DIR = os.path.join(AUDIO_DIR, "cloned_segments")
os.makedirs(CLONED_SEGMENTS_DIR, exist_ok=True)

REF_AUDIO = os.path.join(PROJECT_DIR, "voice_sample.wav")
REF_TEXT = (
    "Hello, my name is Aditya Raj Singh and I study at Newton School of Technology "
    "in ADYPU University. I got great friends in my life."
)

sys.path.insert(0, os.path.join(PROJECT_DIR, "_Code"))
from generate_tts import SCENE_SEGMENTS


def get_inference_device():
    if torch.backends.mps.is_available():
        print("Using Apple Silicon MPS acceleration!")
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def setup_cloning_model(device="mps"):
    print("\n" + "=" * 60)
    print("Initializing F5-TTS Neural Voice Cloning Engine...")
    print(f"Device: {device}")
    print("=" * 60)

    vocoder = load_vocoder(
        vocoder_name="vocos",
        is_local=False,
        device=device
    )

    cfg_path = str(files("f5_tts").joinpath("configs/F5TTS_v1_Base.yaml"))
    model_cfg = OmegaConf.load(cfg_path)
    model_cls = get_class(f"f5_tts.model.{model_cfg.model.backbone}")
    model_arc = model_cfg.model.arch

    ckpt_file = str(cached_path("hf://SWivid/F5-TTS/F5TTS_v1_Base/model_1250000.safetensors"))
    vocab_file = str(files("f5_tts").joinpath("infer/examples/vocab.txt"))

    model = load_model(
        model_cls,
        model_arc,
        ckpt_file,
        mel_spec_type="vocos",
        vocab_file=vocab_file,
        device=device
    )
    print("✓ F5-TTS Model and Vocoder loaded in memory!\n")
    return model, vocoder


def generate_cloned_narration():
    device = get_inference_device()
    try:
        model, vocoder = setup_cloning_model(device=device)
    except Exception as e:
        print(f"Fallback to CPU: {e}")
        device = "cpu"
        model, vocoder = setup_cloning_model(device=device)

    ref_audio_proc, ref_text_proc = preprocess_ref_audio_text(REF_AUDIO, REF_TEXT)

    segment_durations = {}
    scene_durations = {}

    print("Synthesizing narration in student Aditya Raj Singh's cloned voice...")

    for scene_name, segments in SCENE_SEGMENTS.items():
        segment_durations[scene_name] = {}
        seg_wavs = []
        print(f"\n--- Processing {scene_name} ---")

        for seg_id, text in segments:
            out_wav = os.path.join(CLONED_SEGMENTS_DIR, f"{scene_name}_{seg_id}.wav")

            if os.path.exists(out_wav) and seg_id != "planes_intro":
                res = subprocess.run([
                    "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", out_wav
                ], check=True, capture_output=True, text=True)
                dur = float(res.stdout.strip())
                segment_durations[scene_name][seg_id] = dur
                seg_wavs.append(out_wav)
                print(f"  Reusing {seg_id}: {dur:.2f}s")
                continue

            if not text.strip():
                # Scene 0: Title card 5s silence
                cmd = [
                    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-t", "5.0", out_wav
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                dur = 5.0
            else:
                print(f"  Cloning {seg_id}: \"{text[:45]}...\"")
                audio_out, sample_rate, _ = infer_process(
                    ref_audio_proc,
                    ref_text_proc,
                    text,
                    model,
                    vocoder,
                    mel_spec_type="vocos",
                    nfe_step=16,
                    speed=1.18,
                    device=device,
                )
                
                raw_tmp = os.path.join(CLONED_SEGMENTS_DIR, f"raw_{scene_name}_{seg_id}.wav")
                sf.write(raw_tmp, audio_out, sample_rate)

                # Standardize to 44.1kHz stereo PCM
                cmd = [
                    "ffmpeg", "-y", "-i", raw_tmp,
                    "-ar", "44100", "-ac", "2",
                    out_wav
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                if os.path.exists(raw_tmp):
                    os.remove(raw_tmp)

                # Measure precise duration
                res = subprocess.run([
                    "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", out_wav
                ], check=True, capture_output=True, text=True)
                dur = float(res.stdout.strip())

            segment_durations[scene_name][seg_id] = dur
            seg_wavs.append(out_wav)
            print(f"    -> {seg_id} duration: {dur:.2f}s")

        # Concatenate scene segments
        concat_txt = os.path.join(CLONED_SEGMENTS_DIR, f"{scene_name}_concat.txt")
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
        print(f"  ✓ {scene_name} Master Audio: {total_scene_dur:.2f}s")

    # Save durations
    with open(os.path.join(AUDIO_DIR, "segment_durations.json"), "w") as f:
        json.dump(segment_durations, f, indent=2)
    with open(os.path.join(AUDIO_DIR, "durations.json"), "w") as f:
        json.dump(scene_durations, f, indent=2)

    total_time = sum(scene_durations.values())
    mins = int(total_time // 60)
    secs = int(total_time % 60)
    print("\n" + "=" * 60)
    print(f"Cloned Narration Total Duration: {total_time:.2f}s ({mins}:{secs:02d})")
    print(f"Target Window: 4:45 (285s) to 5:30 (330s)")
    if 285.0 <= total_time <= 330.0:
        print("✓ DURATION TARGET MET PERFECTLY!")
    else:
        print(f"Note: Total duration {total_time:.2f}s")
    print("=" * 60)
    return total_time


if __name__ == "__main__":
    generate_cloned_narration()
