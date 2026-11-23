// 3D-Prototyp: Übungsauto zum Drehen, Motorhaube zum Öffnen, Motorraum mit Bauteilen.
import * as T from './vendor/three.min.js';

const box = document.getElementById('auto3d');
const info = document.getElementById('info3d');

const renderer = new T.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = T.SRGBColorSpace;
renderer.toneMapping = T.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = T.PCFSoftShadowMap;
box.appendChild(renderer.domElement);

const scene = new T.Scene();
scene.background = new T.Color('#2b3542');
scene.fog = new T.Fog('#2b3542', 14, 30);
const pmrem = new T.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new T.RoomEnvironment(), 0.04).texture;

const camera = new T.PerspectiveCamera(38, 1, 0.1, 100);
camera.position.set(5.2, 2.4, 4.6);
const controls = new T.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.7, 0);
controls.enableDamping = true;
controls.minDistance = 1.6;
controls.maxDistance = 10;
controls.maxPolarAngle = Math.PI * 0.49;
controls.enablePan = false;

// Licht
scene.add(new T.HemisphereLight('#dfe9f5', '#3b3f45', 0.6));
const sonne = new T.DirectionalLight('#ffffff', 2.2);
sonne.position.set(4, 7, 3);
sonne.castShadow = true;
sonne.shadow.mapSize.set(2048, 2048);
Object.assign(sonne.shadow.camera, { left: -4, right: 4, top: 4, bottom: -4, near: 1, far: 20 });
sonne.shadow.bias = -0.0005;
scene.add(sonne);
const werkstattLampe = new T.PointLight('#fff4dc', 6, 8);
werkstattLampe.position.set(1.4, 3.2, 0);
scene.add(werkstattLampe);

// Materialien
const M = {
  lack: new T.MeshPhysicalMaterial({ color: '#2f7884', metalness: 0.55, roughness: 0.32, clearcoat: 1, clearcoatRoughness: 0.08 }),
  glas: new T.MeshPhysicalMaterial({ color: '#0f1a24', metalness: 0.2, roughness: 0.05, transparent: true, opacity: 0.82, clearcoat: 1 }),
  schwarz: new T.MeshStandardMaterial({ color: '#16191d', roughness: 0.7 }),
  kunststoff: new T.MeshStandardMaterial({ color: '#23272c', roughness: 0.55 }),
  reifen: new T.MeshStandardMaterial({ color: '#141518', roughness: 0.9 }),
  felge: new T.MeshStandardMaterial({ color: '#c9d0d8', metalness: 0.9, roughness: 0.25 }),
  chrom: new T.MeshStandardMaterial({ color: '#e8ecf0', metalness: 1, roughness: 0.12 }),
  licht: new T.MeshStandardMaterial({ color: '#dfe7ef', metalness: 0.6, roughness: 0.1, emissive: '#000000' }),
  rueck: new T.MeshStandardMaterial({ color: '#7a0c12', roughness: 0.25, emissive: '#000000' }),
  blinker: new T.MeshStandardMaterial({ color: '#c46a0c', roughness: 0.3 }),
  boden: new T.MeshStandardMaterial({ color: '#5c6168', roughness: 0.85 }),
  motor: new T.MeshStandardMaterial({ color: '#3c434b', metalness: 0.6, roughness: 0.45 }),
  rot: new T.MeshStandardMaterial({ color: '#c0392b', roughness: 0.4 }),
  gelb: new T.MeshStandardMaterial({ color: '#f2c230', roughness: 0.5 }),
  rosa: new T.MeshPhysicalMaterial({ color: '#f5f5f5', roughness: 0.2, transparent: true, opacity: 0.75 }),
  graustecker: new T.MeshStandardMaterial({ color: '#6b737d', roughness: 0.5 })
};

const mesh = (geo, mat, x, y, z, name) => {
  const m = new T.Mesh(geo, mat);
  m.position.set(x || 0, y || 0, z || 0);
  m.castShadow = true; m.receiveShadow = true;
  if (name) m.userData.name = name;
  return m;
};

// Werkstatt
const boden = mesh(new T.PlaneGeometry(40, 40), M.boden);
boden.rotation.x = -Math.PI / 2; boden.castShadow = false;
scene.add(boden);
const streifen = (z) => { const s = mesh(new T.PlaneGeometry(9, 0.12), new T.MeshStandardMaterial({ color: '#f2c230', roughness: 0.6 }), 0, 0.002, z); s.rotation.x = -Math.PI / 2; s.castShadow = false; scene.add(s); };
streifen(1.9); streifen(-1.9);
const wand = mesh(new T.PlaneGeometry(40, 10), new T.MeshStandardMaterial({ color: '#3a4553', roughness: 0.9 }), 0, 5, -7);
wand.castShadow = false; scene.add(wand);

// ---------- Auto ----------
const auto = new T.Group();
scene.add(auto);
const BREITE = 1.72;

// Seitenprofil (x nach vorne), mit Radausschnitten
function profil() {
  const s = new T.Shape();
  s.moveTo(-1.98, 0.3);
  s.lineTo(-1.66, 0.3); s.absarc(-1.3, 0.33, 0.38, Math.PI, 0, true);
  s.lineTo(0.94, 0.3); s.absarc(1.3, 0.33, 0.38, Math.PI, 0, true);
  s.lineTo(2.0, 0.3);
  s.quadraticCurveTo(2.1, 0.32, 2.08, 0.55);
  s.quadraticCurveTo(2.06, 0.66, 1.96, 0.62);  // vorne bis Haubenkante
  s.lineTo(0.95, 0.62);                         // Motorraum offen (Haube ist eigenes Teil)
  s.lineTo(0.88, 0.94);
  s.quadraticCurveTo(0.4, 1.32, 0.05, 1.4);
  s.lineTo(-1.25, 1.4);
  s.quadraticCurveTo(-1.72, 1.36, -1.86, 1.12);
  s.quadraticCurveTo(-2.02, 0.75, -1.98, 0.3);
  return s;
}
const rumpf = mesh(new T.ExtrudeGeometry(profil(), { depth: BREITE - 0.16, bevelEnabled: true, bevelThickness: 0.08, bevelSize: 0.06, bevelSegments: 5, curveSegments: 24 }), M.lack);
rumpf.position.z = -(BREITE - 0.16) / 2;
auto.add(rumpf);

// Fenster als dunkles Band rundum
const fs = new T.Shape();
fs.moveTo(0.84, 0.98); fs.quadraticCurveTo(0.4, 1.3, 0.06, 1.355); fs.lineTo(-1.24, 1.355); fs.quadraticCurveTo(-1.66, 1.32, -1.8, 1.1); fs.lineTo(-1.76, 0.99); fs.lineTo(0.84, 0.98);
const fenster = mesh(new T.ExtrudeGeometry(fs, { depth: BREITE + 0.005, bevelEnabled: false, curveSegments: 20 }), M.glas, 0, 0, -(BREITE + 0.005) / 2);
fenster.castShadow = false; auto.add(fenster);
[[-0.36, 0.06], [-1.0, 0.05]].forEach(([x, w]) => { auto.add(mesh(new T.BoxGeometry(w, 0.4, BREITE + 0.01), M.schwarz, x, 1.17, 0)); });

// Türfugen, Griffe, Spiegel
const fuge = (x, z) => auto.add(mesh(new T.BoxGeometry(0.008, 0.5, 0.01), M.schwarz, x, 0.7, z));
[0.86, -0.38, -1.1].forEach(x => { fuge(x, BREITE / 2 + 0.005); fuge(x, -BREITE / 2 - 0.005); });
[0.08, -0.82].forEach(x => { auto.add(mesh(new T.BoxGeometry(0.16, 0.03, 0.03), M.chrom, x, 0.86, BREITE / 2 + 0.01)); auto.add(mesh(new T.BoxGeometry(0.16, 0.03, 0.03), M.chrom, x, 0.86, -BREITE / 2 - 0.01)); });
[-1, 1].forEach(sz => { const sp = mesh(new T.BoxGeometry(0.16, 0.1, 0.16), M.lack, 0.72, 1.0, sz * (BREITE / 2 + 0.08)); auto.add(sp); });

// Stoßfänger, Grill, Kennzeichen
auto.add(mesh(new T.BoxGeometry(0.16, 0.2, BREITE - 0.1), M.kunststoff, 2.03, 0.36, 0));
auto.add(mesh(new T.BoxGeometry(0.12, 0.16, 0.8), M.schwarz, 2.08, 0.48, 0));
auto.add(mesh(new T.BoxGeometry(0.02, 0.11, 0.5), new T.MeshStandardMaterial({ color: '#f4f6f9' }), 2.12, 0.33, 0));
auto.add(mesh(new T.BoxGeometry(0.16, 0.2, BREITE - 0.1), M.kunststoff, -2.02, 0.38, 0));

// Scheinwerfer und Rückleuchten (z>0 = linke Fahrzeugseite)
const scheinwerfer = {}, rueckleuchten = {};
[['links', 1], ['rechts', -1]].forEach(([n, sz]) => {
  const sw = mesh(new T.BoxGeometry(0.12, 0.11, 0.36), M.licht.clone(), 2.0, 0.58, sz * 0.58, 'Scheinwerfer ' + n);
  sw.rotation.y = sz * 0.18; auto.add(sw); scheinwerfer[n] = sw;
  auto.add(mesh(new T.BoxGeometry(0.1, 0.05, 0.12), M.blinker, 1.98, 0.58, sz * 0.8));
  const rl = mesh(new T.BoxGeometry(0.06, 0.16, 0.3), M.rueck.clone(), -1.99, 0.95, sz * 0.62, 'Rückleuchte ' + n);
  auto.add(rl); rueckleuchten[n] = rl;
});

// Räder
[[1.3, 1], [1.3, -1], [-1.3, 1], [-1.3, -1]].forEach(([x, sz]) => {
  const r = new T.Group();
  const reifen = mesh(new T.CylinderGeometry(0.33, 0.33, 0.22, 40), M.reifen); reifen.rotation.x = Math.PI / 2; r.add(reifen);
  const felge = mesh(new T.CylinderGeometry(0.21, 0.21, 0.225, 32), new T.MeshStandardMaterial({ color: '#3a4047', metalness: 0.7, roughness: 0.4 })); felge.rotation.x = Math.PI / 2; r.add(felge);
  for (let i = 0; i < 5; i++) { const sp = mesh(new T.BoxGeometry(0.05, 0.19, 0.235), M.felge); sp.rotation.z = i * Math.PI * 2 / 5; sp.position.y = 0; const h = new T.Group(); h.add(sp); sp.position.y = 0.09; h.rotation.z = i * Math.PI * 2 / 5; r.add(h); }
  const nabe = mesh(new T.CylinderGeometry(0.06, 0.06, 0.24, 16), M.chrom); nabe.rotation.x = Math.PI / 2; r.add(nabe);
  r.position.set(x, 0.33, sz * (BREITE / 2 - 0.1));
  auto.add(r);
});

// ---------- Motorraum ----------
const raum = new T.Group();
auto.add(raum);
raum.add(mesh(new T.BoxGeometry(1.0, 0.02, BREITE - 0.2), M.schwarz, 1.45, 0.625, 0));
const bauteil = (g, mat, x, y, z, name) => { const m = mesh(g, mat, x, y, z, name); raum.add(m); return m; };
// Motor
bauteil(new T.BoxGeometry(0.4, 0.14, 0.62), M.motor, 1.25, 0.70, -0.05, 'Motor');
bauteil(new T.BoxGeometry(0.36, 0.03, 0.56), M.kunststoff, 1.25, 0.785, -0.05, 'Motorabdeckung');
bauteil(new T.CylinderGeometry(0.035, 0.035, 0.02, 20), M.gelb, 1.33, 0.805, -0.25, 'Öleinfülldeckel');
// Batterie
const batt = bauteil(new T.BoxGeometry(0.26, 0.16, 0.18), M.schwarz, 1.2, 0.71, 0.6, 'Batterie 12 V');
bauteil(new T.CylinderGeometry(0.022, 0.022, 0.04, 16), M.rot, 1.12, 0.80, 0.6, 'Batterie Pluspol');
bauteil(new T.CylinderGeometry(0.022, 0.022, 0.04, 16), M.kunststoff, 1.28, 0.80, 0.6, 'Batterie Minuspol');
// E-Box
bauteil(new T.BoxGeometry(0.24, 0.12, 0.2), M.kunststoff, 1.15, 0.7, -0.6, 'E-Box (Sicherungen und Relais)');
// Kühlmittelbehälter
bauteil(new T.BoxGeometry(0.14, 0.1, 0.16), M.rosa, 1.5, 0.68, 0.55, 'Kühlmittelbehälter');
// Hupe
const hupe = bauteil(new T.CylinderGeometry(0.06, 0.06, 0.03, 24), M.schwarz, 1.92, 0.66, 0.0, 'Hupe H1');
hupe.rotation.z = Math.PI / 2;
// Scheinwerferrückseiten und Stecker
[['X4 (Scheinwerfer links)', 0.58], ['X5 (Scheinwerfer rechts)', -0.58]].forEach(([n, z]) => {
  bauteil(new T.BoxGeometry(0.16, 0.14, 0.34), M.kunststoff, 1.86, 0.64, z, 'Scheinwerfer Rückseite');
  bauteil(new T.BoxGeometry(0.05, 0.05, 0.07), M.graustecker, 1.76, 0.66, z, 'Stecker ' + n);
});
// Massepunkte
bauteil(new T.CylinderGeometry(0.018, 0.018, 0.03, 12), M.chrom, 1.6, 0.645, 0.78, 'Massepunkt M1');
bauteil(new T.CylinderGeometry(0.018, 0.018, 0.03, 12), M.chrom, 1.6, 0.645, -0.78, 'Massepunkt M2');
// Leitungen
const leitung = (punkte, farbe, d) => {
  const kurve = new T.CatmullRomCurve3(punkte.map(p => new T.Vector3(...p)));
  raum.add(mesh(new T.TubeGeometry(kurve, 40, d || 0.008, 8, false), new T.MeshStandardMaterial({ color: farbe, roughness: 0.6 })));
};
leitung([[1.12, 0.82, 0.6], [1.05, 0.84, 0.4], [1.0, 0.76, 0.0], [1.1, 0.72, -0.55]], '#c0392b', 0.014);
leitung([[1.28, 0.82, 0.6], [1.35, 0.76, 0.75], [1.6, 0.66, 0.78]], '#141414', 0.014);
leitung([[1.73, 0.66, 0.58], [1.5, 0.68, 0.45], [1.1, 0.68, 0.0], [1.15, 0.68, -0.5]], '#e8c43a', 0.007);
leitung([[1.73, 0.66, -0.58], [1.45, 0.66, -0.5], [1.2, 0.68, -0.55]], '#e8c43a', 0.007);
leitung([[1.9, 0.66, 0.0], [1.7, 0.68, -0.2], [1.25, 0.7, -0.55]], '#d32f2f', 0.007);

// ---------- Motorhaube ----------
const haubeDreh = new T.Group();
haubeDreh.position.set(0.9, 0.95, 0);
auto.add(haubeDreh);
const hs = new T.Shape();
hs.moveTo(1.98 - 0.9, 0.64 - 0.95); hs.quadraticCurveTo(1.5 - 0.9, 0.78 - 0.95, 0.9 - 0.9, 0.95 - 0.95); hs.lineTo(0.9 - 0.9, 0.92 - 0.95); hs.quadraticCurveTo(1.5 - 0.9, 0.75 - 0.95, 1.98 - 0.9, 0.61 - 0.95);
const haube = mesh(new T.ExtrudeGeometry(hs, { depth: BREITE - 0.14, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 3, curveSegments: 20 }), M.lack, 0, 0, -(BREITE - 0.14) / 2, 'Motorhaube');
haubeDreh.add(haube);

// ---------- Bedienung ----------
const ziele = [];
auto.traverse(o => { if (o.isMesh && o.userData.name) ziele.push(o); });
let haubeZiel = 0, haubeIst = 0, kameraZiel = null, markiert = null;

function zeige(text) { info.innerHTML = text; }
function markiere(o) {
  if (markiert && markiert.material.emissive) markiert.material.emissive.set(markiert.userData.alt || '#000000');
  markiert = o;
  if (o && o.material.emissive) {
    if (!o.userData.eigen) { o.material = o.material.clone(); o.userData.eigen = true; }
    o.userData.alt = '#' + o.material.emissive.getHexString();
    o.material.emissive.set('#2f6bff');
  }
}

const ray = new T.Raycaster(), maus = new T.Vector2();
let start = null;
renderer.domElement.addEventListener('pointerdown', e => { start = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!start || Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 6) return;
  const r = renderer.domElement.getBoundingClientRect();
  maus.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(maus, camera);
  const treffer = ray.intersectObjects(ziele, false)[0];
  if (!treffer) return;
  const o = treffer.object, n = o.userData.name;
  if (n === 'Motorhaube') { haubeZiel = haubeZiel ? 0 : 1; zeige(haubeZiel ? 'Motorhaube geöffnet. Tippe die Bauteile im Motorraum an.' : 'Motorhaube geschlossen.'); if (haubeZiel) kameraZiel = { pos: new T.Vector3(3.3, 2.2, 1.6), ziel: new T.Vector3(1.4, 0.7, 0) }; return; }
  markiere(o);
  zeige('<b>' + n + '</b>');
});

document.querySelectorAll('[data-3d]').forEach(b => b.addEventListener('click', () => {
  const a = b.dataset['3d'];
  if (a === 'haube') { haubeZiel = haubeZiel ? 0 : 1; if (haubeZiel) kameraZiel = { pos: new T.Vector3(3.3, 2.2, 1.6), ziel: new T.Vector3(1.4, 0.7, 0) }; }
  if (a === 'gesamt') kameraZiel = { pos: new T.Vector3(5.2, 2.4, 4.6), ziel: new T.Vector3(0, 0.7, 0) };
  if (a === 'licht') {
    const an = !scheinwerfer.links.userData.an;
    Object.values(scheinwerfer).forEach(s => { s.userData.an = an; s.material.emissive.set(an ? '#fff4c8' : '#000000'); s.material.emissiveIntensity = 2.5; });
    Object.values(rueckleuchten).forEach(s => { s.material.emissive.set(an ? '#ff1a1a' : '#000000'); s.material.emissiveIntensity = 1.2; });
  }
}));

function groesse() {
  const w = box.clientWidth, h = Math.round(Math.min(560, Math.max(300, w * 0.75)));
  renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
}
addEventListener('resize', groesse); groesse();

const uhr = new T.Clock();
renderer.setAnimationLoop(() => {
  const dt = Math.min(0.05, uhr.getDelta());
  haubeIst += (haubeZiel - haubeIst) * Math.min(1, dt * 5);
  haubeDreh.rotation.z = haubeIst * 1.05;
  if (kameraZiel) {
    camera.position.lerp(kameraZiel.pos, Math.min(1, dt * 3));
    controls.target.lerp(kameraZiel.ziel, Math.min(1, dt * 3));
    if (camera.position.distanceTo(kameraZiel.pos) < 0.02) kameraZiel = null;
  }
  controls.update();
  renderer.render(scene, camera);
});
zeige('Mit einem Finger drehen, mit zwei Fingern zoomen. Tippe auf die Motorhaube.');
