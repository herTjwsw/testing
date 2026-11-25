# Old Roblox MIDI Converter

A small local web app: upload a `.mid` / `.midi`, render it through the bundled **Wind of Fjords + Voyage to Eternity.sf2** soundfont, then export a deliberately lo-fi mono WAV named after the MIDI (for example `my_song.mid` → `my_song.wav`).

## Run it

Requires Python 3.10+, [FluidSynth](https://www.fluidsynth.org/) and FFmpeg on your PATH.

- macOS: `brew install fluidsynth ffmpeg`
- Debian/Ubuntu: `sudo apt install fluidsynth ffmpeg`
- Windows: install FluidSynth and FFmpeg, and ensure their `bin` directories are on PATH.

From this folder:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Choose a MIDI, select a sample rate / bit depth, and download the resulting WAV. The defaults use 22,050 Hz, mono, unsigned 8-bit PCM plus a modest band-limit for a compact, crunchy vintage sound. The included SF2 came from the Pixeldrain link supplied in the project request; confirm you have the rights to use/share it before redistributing this folder.

## Notes

- The soundfont is in `static/Wind-of-Fjords-Voyage-to-Eternity.sf2`.
- Files render on the machine running the app; this is a local utility, not a hosted upload service.
- MIDI playback can differ from Roblox's historical playback; the soundfont and low-quality export provide the retro feel, rather than reproducing a particular game's exact audio engine.
