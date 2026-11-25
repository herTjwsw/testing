from pathlib import Path
from flask import Flask, request, send_file, render_template_string, flash, redirect, url_for
from werkzeug.utils import secure_filename
import subprocess, tempfile, os

ROOT = Path(__file__).resolve().parent
FONT = ROOT / 'static' / 'Wind-of-Fjords-Voyage-to-Eternity.sf2'
UPLOADS = ROOT / 'uploads'
OUTPUTS = ROOT / 'outputs'
UPLOADS.mkdir(exist_ok=True); OUTPUTS.mkdir(exist_ok=True)
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'local-dev-key-change-me')

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MIDI Soundfont Converter</title><style>
*{box-sizing:border-box}body{margin:0;background:#e7e7e7;color:#222;font:14px Arial,Helvetica,sans-serif}.site{width:min(900px,calc(100% - 30px));margin:26px auto;background:#fff;border:1px solid #aaa;box-shadow:0 2px 5px #00000012}.head{background:#3b6e9b;color:#fff;padding:17px 22px 14px;border-bottom:4px solid #274d70}.head small{display:block;color:#dce9f5;font-size:11px;margin-bottom:6px}.head h1{font-size:25px;letter-spacing:-.5px;margin:0;font-weight:700}.head p{margin:6px 0 0;color:#e5eef6;font-size:13px}.content{padding:22px}.intro{margin:0 0 18px;color:#555;line-height:1.5}.tool{border:1px solid #c8c8c8;background:#fafafa;padding:18px}.tool h2{font-size:16px;margin:0 0 15px;padding-bottom:9px;border-bottom:1px solid #ddd}.upload{position:relative;min-height:106px;background:#fff;border:1px dashed #999;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:16px}.upload:hover,.upload.drag{background:#f2f7fb;border-color:#3b6e9b}.upload strong{font-size:14px}.upload p{margin:5px 0;color:#777;font-size:12px}.upload input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer}.filename{font:12px Consolas,monospace;color:#315f87;min-height:15px}.settings{display:flex;gap:20px;margin:16px 0}.setting{flex:1}.setting label{display:block;font-size:12px;font-weight:bold;margin-bottom:5px}.setting select{width:100%;height:31px;border:1px solid #aaa;background:white;padding:4px 7px;font:13px Arial}.sf{font-size:12px;color:#555;background:#f0f0f0;border:1px solid #ddd;padding:9px 10px;margin-bottom:15px}.sf b{color:#333}.btn{background:#4c84b4;color:#fff;border:1px solid #2e5f8a;border-radius:2px;padding:9px 15px;font:bold 13px Arial;cursor:pointer}.btn:hover{background:#3b6e9b}.btn:disabled{opacity:.6}.resultname{margin-left:10px;color:#666;font-size:12px}.alert{padding:9px 10px;margin-bottom:12px;background:#fff4f0;border:1px solid #d99;color:#733;font-size:13px}.notes{display:flex;gap:24px;padding:18px 2px 2px;color:#666;font-size:12px;line-height:1.5}.notes div{flex:1}.notes b{color:#333}.foot{background:#f4f4f4;border-top:1px solid #ddd;padding:10px 22px;color:#777;font-size:11px}.foot a{color:#37668e}@media(max-width:580px){.content{padding:15px}.settings,.notes{display:block}.setting{margin-bottom:12px}.notes div{margin:8px 0}.resultname{display:block;margin:9px 0 0}}
</style></head><body><main class="site"><header class="head"><small>A SMALL MIDI TOOL · VERSION 1.0</small><h1>MIDI Soundfont Converter</h1><p>Give your song the sound of an old Roblox-era game.</p></header><section class="content"><p class="intro">Choose a MIDI file. We’ll play it through the soundfont below, then save a smaller, crunchy WAV using your MIDI’s filename.</p><div class="tool"><h2>Convert a song</h2>{% with messages = get_flashed_messages() %}{% if messages %}{% for m in messages %}<div class="alert">{{m}}</div>{% endfor %}{% endif %}{% endwith %}<form id="form" action="/convert" method="post" enctype="multipart/form-data"><div class="upload" id="drop"><strong>Drop a MIDI file here, or click to browse</strong><p>Accepted files: .mid and .midi</p><div class="filename" id="filename"></div><input type="file" name="midi" id="midi" accept=".mid,.midi,audio/midi" required></div><div class="settings"><div class="setting"><label for="rate">Sample rate</label><select id="rate" name="rate"><option value="22050">22,050 Hz (recommended)</option><option value="16000">16,000 Hz (lower quality)</option><option value="11025">11,025 Hz (very low quality)</option></select></div><div class="setting"><label for="bitrate">Bit depth</label><select id="bitrate" name="bitrate"><option value="8">8-bit (crunchy)</option><option value="16">16-bit (cleaner)</option></select></div></div><div class="sf"><b>Soundfont:</b> Wind of Fjords + Voyage to Eternity.sf2 <span style="color:#66804b">(included)</span></div><button class="btn" id="go">Convert to WAV</button><span class="resultname">The download will be named after your MIDI.</span></form></div><div class="notes"><div><b>How it works</b><br>FluidSynth renders your MIDI using the bundled soundfont.</div><div><b>Lo-fi output</b><br>Mono WAV with a reduced sample rate and selected bit depth.</div><div><b>Running this app?</b><br>Requires FluidSynth and FFmpeg. See README for setup.</div></div></section><footer class="foot">A simple local project. <a href="https://github.com/" target="_blank" rel="noreferrer">Source code</a></footer></main><script>const input=document.getElementById('midi'),nameEl=document.getElementById('filename'),drop=document.getElementById('drop'),form=document.getElementById('form');input.addEventListener('change',()=>nameEl.textContent=input.files[0]?.name||'');for(const ev of ['dragenter','dragover'])drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')});for(const ev of ['dragleave','drop'])drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')});drop.addEventListener('drop',e=>{if(e.dataTransfer.files.length){input.files=e.dataTransfer.files;nameEl.textContent=input.files[0].name}});form.addEventListener('submit',()=>{document.getElementById('go').disabled=true;document.getElementById('go').textContent='Converting…'});</script></body></html>'''

@app.get('/')
def home(): return render_template_string(PAGE)

@app.post('/convert')
def convert():
    f = request.files.get('midi')
    if not f or not f.filename:
        flash('Choose a MIDI file first.'); return redirect(url_for('home'))
    original = secure_filename(f.filename)
    if Path(original).suffix.lower() not in ('.mid', '.midi'):
        flash('Please upload a .mid or .midi file.'); return redirect(url_for('home'))
    if not FONT.exists():
        flash('The bundled soundfont is missing. See README.md for setup.'); return redirect(url_for('home'))
    rate = request.form.get('rate', '22050')
    bits = request.form.get('bitrate', '8')
    if rate not in ('22050','16000','11025') or bits not in ('8','16'):
        flash('Invalid audio settings.'); return redirect(url_for('home'))
    stem = Path(original).stem or 'nostalgia'
    with tempfile.TemporaryDirectory(dir=OUTPUTS) as td:
        td = Path(td); midi = td / original; raw = td / 'render.wav'; final = OUTPUTS / f'{stem}.wav'
        f.save(midi)
        try:
            subprocess.run(['fluidsynth','-ni',str(FONT),str(midi),'-F',str(raw),'-r','44100','-g','0.8'],check=True,capture_output=True,timeout=240)
            codec = 'pcm_u8' if bits == '8' else 'pcm_s16le'
            subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-af','lowpass=f=9000,highpass=f=100','-ac','1','-ar',rate,'-c:a',codec,str(final)],check=True,capture_output=True,timeout=240)
        except FileNotFoundError as e:
            flash(f'Missing required program: {e.filename}. Install FluidSynth and FFmpeg, then restart.'); return redirect(url_for('home'))
        except subprocess.TimeoutExpired:
            flash('Rendering took too long. Try a shorter MIDI file.'); return redirect(url_for('home'))
        except subprocess.CalledProcessError as e:
            detail = e.stderr.decode(errors='replace')[-500:] if e.stderr else ''
            flash('Could not render this MIDI. Check that it is valid. ' + detail); return redirect(url_for('home'))
        return send_file(final, as_attachment=True, download_name=f'{stem}.wav', mimetype='audio/wav')

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)), debug=False)
