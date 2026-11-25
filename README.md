# Old Roblox MIDI Converter

A small, locally-run web app: Upload a `.mid` or `.midi` file, have it rendered using the built-in soundfont **"Wind of Fjords + Voyage to Eternity.sf2,"** and then export a mono WAV file, intentionally crafted with a lo-fi aesthetic. The output filename will match the original MIDI filename (e.g., `my_song.mid` → `my_song.wav`).

## Execution

Requires Python 3.10+, as well as [FluidSynth](https://www.fluidsynth.org/) and FFmpeg (both must be added to your system PATH).

- macOS: `brew install fluidsynth ffmpeg`
- Debian/Ubuntu: `sudo apt install fluidsynth ffmpeg`
- Windows: Install FluidSynth and FFmpeg, and ensure their `bin` directories are included in your system PATH.

Run the following commands in this folder:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Select a MIDI file, configure the sample rate and bit depth, and download the resulting WAV file. The default settings use 22,050 Hz, mono, 8-bit PCM (unsigned), and a subtle bandwidth limitation—resulting in a compact, "crisp" vintage sound. The included SF2 soundfont originates from the Pixeldrain link provided in the project request. Please ensure that you have the appropriate rights for use or distribution before sharing this folder.

## Notes

- The soundfont is located at `static/Wind-of-Fjords-Voyage-to-Eternity.sf2`.
- Files are rendered on the computer where the app is running; this is a local tool, not a hosted upload service.
- MIDI playback may differ from the historical playback in Roblox. While the soundfont and the low-quality export produce the desired retro aesthetic, they do not precisely replicate the audio engine of any specific game.
- The soundfont belongs to NotRoblox from Musical Artifacts, not me.
