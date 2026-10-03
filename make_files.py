#!/usr/bin/env python3
"""Writes the test harness files into the current directory tree."""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ROOT, "js")
os.makedirs(JS, exist_ok=True)

FILES = {}

# ─── index.html ─────────────────────────────────────────────────────────
FILES["index.html"] = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>iOS Test Harness</title>
<style>
  body { font: 14px ui-monospace, Menlo, monospace; background: #111; color: #eee; padding: 16px; line-height: 1.5; }
  h1 { font-size: 18px; margin: 0 0 12px; }
  h2 { font-size: 14px; color: #6cf; margin: 20px 0 6px; border-bottom: 1px solid #333; padding-bottom: 4px; }
  .ok { color: #6f6; }
  .no { color: #f66; }
  .warn { color: #fc6; }
  .kv { padding-left: 16px; }
  button { background: #2a2a2a; color: #eee; border: 1px solid #444; padding: 8px 14px; font: inherit; border-radius: 6px; margin: 8px 0; }
</style>
</head>
<body>
<h1>iOS Test Harness — Phase 1</h1>
<div id="out"></div>
<button onclick="location.reload()">Re-run</button>
<script>
const out = document.getElementById('out');
function sec(t) { out.insertAdjacentHTML('beforeend', '<h2>' + t + '</h2>'); }
function kv(k, v, cls) { out.insertAdjacentHTML('beforeend', '<div class="kv"><span class="' + (cls||'') + '">' + k + ':</span> ' + v + '</div>'); }

sec('Device');
kv('userAgent', navigator.userAgent);
kv('platform', navigator.platform);
kv('hardwareConcurrency', navigator.hardwareConcurrency);
kv('maxTouchPoints', navigator.maxTouchPoints);
kv('language', navigator.language);
kv('timezone', Intl.DateTimeFormat().resolvedOptions().timeZone);

const ua = navigator.userAgent;
const ios = ua.match(/OS (\d+)_(\d+)(?:_(\d+))?/);
if (ios) kv('iOS version', ios[1] + '.' + ios[2] + (ios[3] ? '.' + ios[3] : ''), 'ok');
const wk = ua.match(/AppleWebKit\/(\d+\.\d+)/);
if (wk) kv('WebKit', wk[1]);

sec('JS engine');
kv('WebAssembly', typeof WebAssembly !== 'undefined' ? 'yes' : 'no', typeof WebAssembly !== 'undefined' ? 'ok' : 'no');
kv('BigInt', typeof BigInt !== 'undefined' ? 'yes' : 'no');
kv('WeakRef', typeof WeakRef !== 'undefined' ? 'yes' : 'no');
kv('SharedArrayBuffer', typeof SharedArrayBuffer !== 'undefined' ? 'yes' : 'no');
kv('Atomics', typeof Atomics !== 'undefined' ? 'yes' : 'no');

const t0 = performance.now();
let x = 0;
for (let i = 0; i < 5000000; i++) x = (x + i) | 0;
const jms = performance.now() - t0;
kv('5M-loop time (ms)', jms.toFixed(1));
kv('JIT likely active', jms < 100 ? 'yes (fast)' : jms < 500 ? 'partial' : 'no / throttled',
   jms < 100 ? 'ok' : 'warn');

sec('WebGL');
const canvas = document.createElement('canvas');
const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
kv('WebGL1', gl ? 'yes' : 'no', gl ? 'ok' : 'no');
if (gl) {
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  kv('vendor', gl.getParameter(gl.VENDOR));
  kv('renderer', gl.getParameter(gl.RENDERER));
  if (dbg) kv('unmasked', gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL));
  kv('maxTextureSize', gl.getParameter(gl.MAX_TEXTURE_SIZE));
  const exts = gl.getSupportedExtensions() || [];
  kv('extensions', exts.length);
  kv('OES_texture_float', exts.includes('OES_texture_float') ? 'yes' : 'no');
}
const gl2 = document.createElement('canvas').getContext('webgl2');
kv('WebGL2', gl2 ? 'yes' : 'no', gl2 ? 'ok' : 'warn');

sec('Alternate pivots');
kv('AudioContext', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined' ? 'yes' : 'no');
kv('RTCPeerConnection', typeof RTCPeerConnection !== 'undefined' ? 'yes' : 'no');
kv('MediaSource', typeof MediaSource !== 'undefined' ? 'yes' : 'no');
kv('VideoDecoder', typeof VideoDecoder !== 'undefined' ? 'yes' : 'no');
kv('OffscreenCanvas', typeof OffscreenCanvas !== 'undefined' ? 'yes' : 'no');

sec('Storage');
kv('localStorage', (function(){ try { localStorage.setItem('t','1'); localStorage.removeItem('t'); return 'yes'; } catch(e){ return 'no'; } })());
kv('IndexedDB', typeof indexedDB !== 'undefined' ? 'yes' : 'no');

sec('Context');
kv('isSecureContext', window.isSecureContext ? 'yes' : 'no');
kv('crossOriginIsolated', window.crossOriginIsolated ? 'yes' : 'no');
kv('origin', location.origin);

const f = document.createElement('iframe');
f.src = 'js/frame-test.html';
f.style.cssText = 'width:1px;height:1px;position:absolute;left:-9999px;';
document.body.appendChild(f);
kv('1x1 iframe', 'inserted');
</script>
</body>
</html>
"""

# ─── js/frame-test.html ─────────────────────────────────────────────────
FILES["js/frame-test.html"] = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>frame-test</title></head>
<body><script>
console.log('[frame-test] loaded');
parent.postMessage({type:'frame-ok', ua: navigator.userAgent}, '*');
</script></body></html>
"""

# ─── js/jit.html ────────────────────────────────────────────────────────
FILES["js/jit.html"] = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>JIT primitives</title>
<style>
  body { font: 14px ui-monospace; background:#111; color:#eee; padding:16px; line-height:1.5;}
  h2 { font-size:14px; color:#6cf; margin:16px 0 6px; border-bottom:1px solid #333;}
  .ok{color:#6f6;} .no{color:#f66;} .warn{color:#fc6;}
</style>
</head>
<body>
<h1>JIT / JS engine primitives</h1>
<div id="out"></div>
<script>
const out = document.getElementById('out');
function sec(t){out.insertAdjacentHTML('beforeend','<h2>'+t+'</h2>');}
function kv(k,v,c){out.insertAdjacentHTML('beforeend','<div><span class="'+(c||'')+'">'+k+':</span> '+v+'</div>');}

sec('Typed array spray');
const t0 = performance.now();
const arr = [];
for (let i = 0; i < 10000; i++) arr.push(new Float64Array(64));
const sp = performance.now() - t0;
kv('10k Float64Array allocations', sp.toFixed(1) + ' ms', sp < 200 ? 'ok' : 'warn');

sec('Overlapping views');
const buf = new ArrayBuffer(1024);
const f64 = new Float64Array(buf);
const u32 = new Uint32Array(buf);
const u8  = new Uint8Array(buf);
f64[0] = 1.5;
kv('f64[0]=1.5 -> u32[0]', u32[0].toString(16), 'ok');
kv('f64[0]=1.5 -> u32[1]', u32[1].toString(16), 'ok');

sec('Bounds checks');
const testArr = new Float64Array(1000);
for (let i = 0; i < 1e5; i++) testArr[i % 1000];
try {
  const v = testArr[5000];
  kv('out-of-bounds read', 'returned ' + v + ' (!)', 'no');
} catch (e) {
  kv('out-of-bounds read', 'threw ' + e.constructor.name, 'ok');
}

sec('WebAssembly');
if (typeof WebAssembly !== 'undefined') {
  const wasmBytes = new Uint8Array([
    0x00,0x61,0x73,0x6d, 0x01,0x00,0x00,0x00,
    0x01,0x05,0x01,0x60,0x00,0x01,0x7f,
    0x03,0x02,0x01,0x00,
    0x07,0x08,0x01,0x04,0x74,0x65,0x73,0x74,0x00,0x00,
    0x0a,0x06,0x01,0x04,0x00,0x41,0x2a,0x0b
  ]);
  WebAssembly.instantiate(wasmBytes).then(function(r){
    var v = r.instance.exports.test();
    kv('wasm instantiate', v === 42 ? 'ok (42)' : 'unexpected ' + v, v === 42 ? 'ok' : 'no');
  }).catch(function(e){ kv('wasm instantiate', 'error: ' + e.message, 'no'); });
}
</script>
</body></html>
"""

# ─── js/webgl.html ──────────────────────────────────────────────────────
FILES["js/webgl.html"] = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>WebGL pivot</title>
<style>
  body{font:13px ui-monospace;background:#111;color:#eee;padding:16px}
  .ok{color:#6f6}.no{color:#f66}.warn{color:#fc6}
  h2{font-size:14px;color:#6cf;margin:16px 0 6px;border-bottom:1px solid #333}
</style></head>
<body><h1>WebGL / GPU pivot test</h1><div id="out"></div>
<script>
var out = document.getElementById('out');
function sec(t){out.insertAdjacentHTML('beforeend','<h2>'+t+'</h2>');}
function kv(k,v,c){out.insertAdjacentHTML('beforeend','<div><span class="'+(c||'')+'">'+k+':</span> '+v+'</div>');}

sec('WebGL1 context');
var canvas = document.createElement('canvas');
canvas.width = 256; canvas.height = 256;
var gl = canvas.getContext('webgl', { antialias: false });
if (!gl) { kv('context', 'failed', 'no'); }
else {
  kv('context created', 'yes', 'ok');
  var dbg = gl.getExtension('WEBGL_debug_renderer_info');
  if (dbg) {
    kv('UNMASKED_VENDOR', gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL));
    kv('UNMASKED_RENDERER', gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL));
  }
  var exts = gl.getSupportedExtensions() || [];
  kv('extensions', exts.length);
  ['OES_texture_float','OES_texture_half_float','WEBGL_draw_buffers',
   'EXT_color_buffer_float','WEBGL_debug_shaders','EXT_disjoint_timer_query',
   'WEBGL_compressed_texture_astc','WEBGL_compressed_texture_etc'].forEach(function(e){
    kv('ext:'+e, exts.indexOf(e) >= 0 ? 'yes' : 'no', exts.indexOf(e) >= 0 ? 'ok' : '');
  });

  sec('Shader compile');
  var vs = gl.createShader(gl.VERTEX_SHADER);
  gl.shaderSource(vs, 'attribute vec2 p; void main(){ gl_Position = vec4(p,0.,1.); }');
  gl.compileShader(vs);
  kv('vertex shader', gl.getShaderParameter(vs, gl.COMPILE_STATUS) ? 'ok' : 'fail',
     gl.getShaderParameter(vs, gl.COMPILE_STATUS) ? 'ok' : 'no');

  sec('Texture alloc');
  var tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 2048, 2048, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
  kv('2K RGBA texture', gl.getError() === 0 ? 'ok' : 'error', gl.getError() === 0 ? 'ok' : 'warn');
  kv('MAX_TEXTURE_SIZE', gl.getParameter(gl.MAX_TEXTURE_SIZE));
  kv('MAX_RENDERBUFFER_SIZE', gl.getParameter(gl.MAX_RENDERBUFFER_SIZE));

  sec('Float textures');
  if (exts.indexOf('OES_texture_float') >= 0) {
    var ftex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, ftex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 256, 256, 0, gl.RGBA, gl.FLOAT, null);
    kv('256x256 float texture', gl.getError() === 0 ? 'ok' : 'error',
       gl.getError() === 0 ? 'ok' : 'no');
  }
}

sec('WebGL2');
var gl2 = document.createElement('canvas').getContext('webgl2');
kv('webgl2 context', gl2 ? 'yes' : 'no', gl2 ? 'ok' : 'warn');
if (gl2) {
  kv('MAX_TEXTURE_SIZE (gl2)', gl2.getParameter(gl2.MAX_TEXTURE_SIZE));
  kv('MAX_ARRAY_TEXTURE_LAYERS', gl2.getParameter(gl2.MAX_ARRAY_TEXTURE_LAYERS));
}
</script></body></html>
"""

# ─── js/timing.html ─────────────────────────────────────────────────────
FILES["js/timing.html"] = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Timing</title>
<style>
  body{font:13px ui-monospace;background:#111;color:#eee;padding:16px}
  .ok{color:#6f6}.no{color:#f66}.warn{color:#fc6}
  h2{font-size:14px;color:#6cf;margin:16px 0 6px;border-bottom:1px solid #333}
</style></head>
<body><h1>Timing precision</h1><div id="out"></div>
<script>
var out = document.getElementById('out');
function sec(t){out.insertAdjacentHTML('beforeend','<h2>'+t+'</h2>');}
function kv(k,v,c){out.insertAdjacentHTML('beforeend','<div><span class="'+(c||'')+'">'+k+':</span> '+v+'</div>');}

sec('performance.now()');
var samples = [];
for (var i = 0; i < 100000; i++) {
  var a = performance.now();
  var b = performance.now();
  if (b > a) samples.push(b - a);
}
samples.sort(function(x,y){ return x - y; });
kv('median delta (ms)', samples[Math.floor(samples.length/2)].toFixed(6));
kv('min delta (ms)', samples[0].toFixed(6), samples[0] > 0.0001 ? 'ok' : 'coarse');
kv('resolution', samples[0] < 0.001 ? 'high (<1 us)' : samples[0] < 0.05 ? 'medium' : 'coarse',
   samples[0] < 0.05 ? 'ok' : 'warn');

sec('Hot-loop stability');
function run() {
  var s = 0;
  for (var i = 0; i < 100000; i++) s += i * i;
  return s;
}
for (var i = 0; i < 1000; i++) run();
var times = [];
for (var i = 0; i < 100; i++) {
  var t = performance.now();
  run();
  times.push(performance.now() - t);
}
times.sort(function(a,b){ return a-b; });
kv('median (ms)', times[50].toFixed(3));
kv('min (ms)', times[0].toFixed(3));
kv('max (ms)', times[99].toFixed(3));
var ratio = times[99] / times[0];
kv('max/min ratio', ratio.toFixed(2), ratio < 3 ? 'ok (stable)' : 'noisy');
</script></body></html>
"""

# ─── Write ──────────────────────────────────────────────────────────────
for rel, content in FILES.items():
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote " + rel + "  (" + str(len(content)) + " bytes)")

print("\nAll files written to " + ROOT)