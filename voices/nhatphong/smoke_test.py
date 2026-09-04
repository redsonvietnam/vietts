#!/usr/bin/env python3
"""
Smoke test for the Nhật Phong voice profile.

Verifies that the profile can be loaded, the reference audio resolved,
and VieNeu generates valid non-silent audio.

Usage:
    python voices/nhatphong/smoke_test.py
    python voices/nhatphong/smoke_test.py --text "Xin chào từ Nhật Phong."
    python voices/nhatphong/smoke_test.py --output custom_output.wav
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 on Windows
if sys.stdout.encoding != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROFILE_PATH = SCRIPT_DIR / "profile.json"
REPO_ROOT = SCRIPT_DIR.parent.parent  # voices/nhatphong/ -> vietts/


def load_profile() -> dict:
    """Load and validate the profile JSON."""
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(f"Profile not found: {PROFILE_PATH}")
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    required = ["profile_name", "reference", "inference", "runtime"]
    for key in required:
        if key not in profile:
            raise KeyError(f"Missing required key: {key}")

    return profile


def resolve_reference(profile: dict) -> Path:
    """Resolve the reference audio path relative to the repo root."""
    ref = profile["reference"]
    ref_path = REPO_ROOT / ref["relative_path"]

    if not ref_path.exists():
        raise FileNotFoundError(
            f"Reference audio not found: {ref_path}\n"
            f"Place '{ref['filename']}' at:\n"
            f"  {REPO_ROOT / ref['relative_path']}"
        )

    return ref_path


def run_smoke_test(text: str, output_path: str | None) -> bool:
    """Run the full smoke test. Returns True on success."""
    # 1. Load profile
    print(f"Loading profile: {PROFILE_PATH}")
    profile = load_profile()
    name = profile["profile_name"]
    version = profile["version"]
    status = profile["status"]
    print(f"  Name: {name}")
    print(f"  Version: {version}")
    print(f"  Status: {status}")

    if status != "experimental":
        print(f"  WARNING: Unexpected status '{status}'")

    # 2. Resolve reference
    ref = profile["reference"]
    print(f"\nReference: {ref['relative_path']}")
    print(f"  Classification: {ref['classification']}")
    print(f"  Duration: ~{ref['duration_seconds']}s")
    ref_path = resolve_reference(profile)
    print(f"  Resolved: {ref_path}")
    print(f"  File size: {ref_path.stat().st_size:,} bytes")

    # 3. Import VieNeu
    print("\nLoading VieNeu...")
    try:
        from vieneu import Vieneu
    except ImportError as e:
        print(f"  FAILED: VieNeu not installed: {e}")
        return False

    # 4. Initialize
    print("  Initializing v3 Turbo (int8, CPU)...")
    try:
        tts = Vieneu()
    except Exception as e:
        print(f"  FAILED: Could not initialize VieNeu: {e}")
        return False

    # 5. Register voice
    cfg = profile["inference"]
    print(f"  Registering voice: {name}")
    try:
        tts.add_voice(
            name=name,
            ref_audio=str(ref_path),
            denoise=cfg["denoise"],
            use_ref_codes=cfg["use_ref_codes"],
            save=False,
        )
    except Exception as e:
        print(f"  FAILED: Could not register voice: {e}")
        tts.close()
        return False

    # 6. Generate
    print(f"\nGenerating: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
    try:
        audio = tts.infer(
            text=text,
            voice=name,
            temperature=cfg["temperature"],
            repetition_penalty=cfg["repetition_penalty"],
            max_chars=cfg["max_chars"],
        )
    except Exception as e:
        print(f"  FAILED: Inference failed: {e}")
        tts.close()
        return False

    # 7. Validate output
    import numpy as np
    duration = len(audio) / tts.sample_rate
    rms = float(np.sqrt(np.mean(audio.astype(float) ** 2)))
    peak = float(np.max(np.abs(audio.astype(float))))
    non_silent = rms > 0.001

    print(f"\n  Duration: {duration:.2f}s")
    print(f"  Sample rate: {tts.sample_rate} Hz")
    print(f"  RMS: {rms:.6f}")
    print(f"  Peak: {peak:.6f}")
    print(f"  Non-silent: {non_silent}")

    if not non_silent:
        print("\n  FAILED: Audio is silent")
        tts.close()
        return False

    # 8. Save
    if output_path is None:
        output_path = str(SCRIPT_DIR / "smoke_test_output.wav")
    tts.save(audio, output_path)
    print(f"\nOutput: {output_path}")

    tts.close()
    print("\nPASS")
    return True


def main():
    parser = argparse.ArgumentParser(description="Smoke test for Nhật Phong voice profile")
    parser.add_argument(
        "--text",
        default="Xin chào, đây là giọng nói thử nghiệm từ Nhật Phong.",
        help="Text to generate",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output WAV path (default: voices/nhatphong/smoke_test_output.wav)",
    )
    args = parser.parse_args()

    try:
        success = run_smoke_test(args.text, args.output)
    except Exception as e:
        print(f"\nERROR: {e}")
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
