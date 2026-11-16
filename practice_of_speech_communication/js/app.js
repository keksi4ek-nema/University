import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const ui = {
    propPanel: document.getElementById('prop-panel'), viewport: document.getElementById('viewport'),
    camMenu: document.getElementById('camera-menu'), camBtn: document.getElementById('btn-toggle-cams'),
    gostOverlay: document.getElementById('gost-overlay'),
    statusMsg: document.getElementById('status-msg'), statusBar: document.querySelector('.statusbar'),
    tourBtn: document.getElementById('btn-auto-tour'), tourIndicator: document.getElementById('tour-indicator'),
    labelsBtn: document.getElementById('btn-toggle-labels'), explodeBtn: document.getElementById('btn-explode'),
    timeSlider: document.getElementById('time-slider'), timeDisplay: document.getElementById('time-display')
};

ui.camBtn.addEventListener('click', () => ui.camMenu.style.display = ui.camMenu.style.display === 'none' ? 'flex' : 'none');
document.getElementById('btn-close-prop').addEventListener('click', () => { ui.propPanel.classList.remove('open'); ui.viewport.classList.remove('panel-open'); });

const DB = {
    "INT_DeskA2": { 
        tag: "Рабочее место", title: "Парта с доской А2", 
        desc: "Новая стандартная парта ПТПИТ, поверх которой установлен наклонный чертежный планшет формата А2. Оптимальное решение без лишних затрат.", 
        specs: [["Доска", "Формат А2 (600x400)"], ["Угол наклона", "Регулируемый"], ["Размещение", "1 парта - 1 студент"]], 
        camOffset: {x: 1.4, y: 1.2, z: 1.6}, labelPos: {x:-1.1, y:1.2, z:1.5}, labelText: "Планшеты А2", hasAnim: false
    },
    "INT_DocCam": { 
        tag: "Преподавание", title: "Стол с Док-камерой", 
        desc: "Рабочее место преподавателя, оснащенное док-камерой высокого разрешения. Позволяет транслировать процесс черчения.", 
        specs: [["Оборудование", "Док-камера 4K"], ["Связь", "Вывод на ТВ-панель"], ["Расположение", "У окна"]], 
        camOffset: {x: -1.6, y: 1.0, z: 1.2}, labelPos: {x:2.0, y:1.3, z:3.8}, labelText: "Док-камера", hasAnim: false
    },
    "INT_Board": { 
        tag: "Фронт", title: "Доска с ТВ-панелью", 
        desc: "Объединенная маркерная доска и ТВ-панель для вывода трансляции с док-камеры и показа презентаций.", 
        specs: [["Доска", "Маркерная белая"], ["Экран", "LED панель 65""]], 
        camOffset: {x: 0, y: 1.5, z: 3.0}, labelPos: {x:0, y:2.5, z:4.4}, labelText: "Фронтальная зона", hasAnim: false
    },
    "INT_BoltStand": { 
        tag: "Наглядное пособие", title: "Стенд «Чертёж и Деталь»", 
        desc: "Связка реального чертежа детали по ГОСТу и её физической распечатанной 3D-модели (например, болта с резьбой).", 
        specs: [["Чертеж", "Болт ГОСТ 7798-70"], ["Модель", "Физическая, разборная"], ["Назначение", "Чтение чертежей"]], 
        camOffset: {x: 0, y: 1.2, z: -2.0}, labelPos: {x:-2.2, y:2.2, z:-4.1}, labelText: "Стенд (Болт)", hasAnim: false
    }
};

const CAMS = {
    overview: { p: {x: 0, y: 3.5, z: 4.8}, t: {x: 0, y: 0.5, z: -1.5} }, 
    board: { p: {x: -0.5, y: 1.6, z: 1.0}, t: {x: 0, y: 1.4, z: 4.3} },
    kulman: { p: {x: -1.6, y: 1.5, z: 1.4}, t: {x: -0.2, y: 0.8, z: -0.2} }, 
    bolt: { p: {x: 0, y: 1.6, z: -0.5}, t: {x: -2.2, y: 1.8, z: -4.2} }
};
const tourKeys = ['overview', 'board', 'kulman', 'bolt'];

const container = document.getElementById('canvas-container');
const scene = new THREE.Scene(); scene.background = new THREE.Color(0x121316);
const aspect = container.clientWidth / container.clientHeight;
const perspCamera = new THREE.PerspectiveCamera(45, aspect, 0.1, 100);
perspCamera.position.set(CAMS.overview.p.x, CAMS.overview.p.y, CAMS.overview.p.z);
const fs = window.innerWidth < 768 ? 13 : 10;
const orthoCamera = new THREE.OrthographicCamera(-fs*aspect/2, fs*aspect/2, fs/2, -fs/2, 0.1, 50);
orthoCamera.position.set(0, 15, 0); orthoCamera.lookAt(0,0,0);
let activeCamera = perspCamera;

const renderer = new THREE.WebGLRenderer({ antialias: window.innerWidth > 768 });
renderer.setSize(container.clientWidth, container.clientHeight); renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; container.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(container.clientWidth, container.clientHeight);
labelRenderer.domElement.style.position = 'absolute'; labelRenderer.domElement.style.top = '0px'; labelRenderer.domElement.style.pointerEvents = 'none';
container.appendChild(labelRenderer.domElement);

const controls = new OrbitControls(perspCamera, renderer.domElement);
controls.enableDamping = true; controls.dampingFactor = 0.05; controls.target.set(CAMS.overview.t.x, CAMS.overview.t.y, CAMS.overview.t.z);
controls.minDistance = 0.5; controls.maxDistance = 8; controls.maxPolarAngle = Math.PI/2 - 0.05;

const B = { x1:-3.1, x2:3.1, y1:0.2, y2:3.0, z1:-4.3, z2:4.3 };
controls.addEventListener('change', () => {
    if(activeCamera !== perspCamera) return;
    perspCamera.position.x = THREE.MathUtils.clamp(perspCamera.position.x, B.x1, B.x2);
    perspCamera.position.y = THREE.MathUtils.clamp(perspCamera.position.y, B.y1, B.y2);
    perspCamera.position.z = THREE.MathUtils.clamp(perspCamera.position.z, B.z1, B.z2);
});

const ambientLight = new THREE.AmbientLight(0xffffff, 0.6); scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xfffae5, 1.5); 
sunLight.castShadow = true; sunLight.shadow.mapSize.set(1024, 1024); sunLight.shadow.bias = -0.001;
scene.add(sunLight);
const interiorLights = new THREE.PointLight(0xe0f2fe, 0, 10); 
interiorLights.position.set(0, 2.8, 0); scene.add(interiorLights);

function updateTimeOfDay(hour) {
    let h = parseFloat(hour);
    ui.timeDisplay.textContent = `${Math.floor(h)}:00`;
    let t = (h - 8) / 12; 
    sunLight.position.x = THREE.MathUtils.lerp(8, -8, t);
    sunLight.position.y = Math.sin(t * Math.PI) * 5 + 1;
    sunLight.position.z = 4;
    
    if (h < 10 || h > 18) {
        sunLight.color.setHex(0xffaa55); 
        sunLight.intensity = Math.max(0.2, Math.sin(t * Math.PI) * 1.5);
        interiorLights.intensity = 1.0; 
    } else {
        sunLight.color.setHex(0xfffae5); 
        sunLight.intensity = 1.8;
        interiorLights.intensity = 0.0; 
    }
}
ui.timeSlider.addEventListener('input', (e) => updateTimeOfDay(e.target.value));
updateTimeOfDay(12);

const grpProj = new THREE.Group(); const grpOld = new THREE.Group();
const blueprintGrid = new THREE.GridHelper(10, 20, 0x06b6d4, 0x1e3a8a); blueprintGrid.position.y = 0.02; blueprintGrid.visible = false;
scene.add(grpProj, grpOld, blueprintGrid);
const meshes = []; const labels = []; let showLabels = true;
let isExploded = false; const explodeParts = [];

const matF = new THREE.MeshStandardMaterial({color: 0x2f333c, roughness: 0.9});
const matW = new THREE.MeshStandardMaterial({color: 0x9499a3, roughness: 1});
const matWood = new THREE.MeshStandardMaterial({color: 0x8c7355, roughness: 0.7});
const matMet = new THREE.MeshStandardMaterial({color: 0x222, roughness: 0.3, metalness: 0.6});
const matBoltThread = new THREE.MeshStandardMaterial({color: 0xa1a1aa, roughness: 0.4, metalness: 0.7});
const matBoltHead = new THREE.MeshStandardMaterial({color: 0xd4d4d8, roughness: 0.3, metalness: 0.8});

function makeWall(w, h, d, x, y, z) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), matW); m.position.set(x, y, z); m.receiveShadow = true; return m; }
function reg(obj, k) { obj.traverse(c => { if(c.isMesh) { c.userData = {k: k, root: obj}; meshes.push(c); } }); }

const floor = new THREE.Mesh(new THREE.PlaneGeometry(6.6, 9), matF); floor.rotation.x = -Math.PI/2; floor.receiveShadow = true;
scene.add(floor, makeWall(6.6, 3.2, 0.1, 0, 1.6, -4.55), makeWall(6.6, 3.2, 0.1, 0, 1.6, 4.55), makeWall(0.1, 3.2, 9, -3.35, 1.6, 0), makeWall(0.1, 3.2, 9, 3.35, 1.6, 0));

function createLabel(text, pos, key) {
    const div = document.createElement('div');
    div.className = 'hotspot-label';
    div.innerHTML = `<div class="hotspot-dot"></div><span>${text}</span>`;
    div.onpointerdown = (e) => { e.stopPropagation(); openProps(null, DB[key], true); };
    const label = new CSS2DObject(div);
    label.position.set(pos.x, pos.y, pos.z);
    grpProj.add(label);
    labels.push(div);
}

function bDeskA2(x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z);
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.03, 0.5), new THREE.MeshStandardMaterial({color:0xe5e7eb})); top.position.y = 0.74; top.castShadow = true; top.receiveShadow = true;
    const frame = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.02, 0.4), matMet); frame.position.y = 0.71;
    const legL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.71, 0.4), matMet); legL.position.set(-0.53, 0.355, 0); legL.castShadow = true;
    const legR = legL.clone(); legR.position.x = 0.53;
    
    const boardGroup = new THREE.Group();
    boardGroup.position.set(0, 0.755, 0.15);
    boardGroup.rotation.x = -0.4; 
    const boardBase = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.02, 0.45), matWood);
    boardBase.position.set(0, 0.01, -0.225);
    const paper = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.005, 0.4), new THREE.MeshStandardMaterial({color:0xffffff}));
    paper.position.set(0, 0.025, -0.225);
    boardGroup.add(boardBase, paper);

    g.add(top, frame, legL, legR, boardGroup);
    return g;
}

function bTeacherDesk(x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z);
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.03, 0.5), new THREE.MeshStandardMaterial({color:0xe5e7eb})); top.position.y = 0.74; top.castShadow = true; top.receiveShadow = true;
    const frame = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.02, 0.4), matMet); frame.position.y = 0.71;
    const legL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.71, 0.4), matMet); legL.position.set(-0.53, 0.355, 0); legL.castShadow = true;
    const legR = legL.clone(); legR.position.x = 0.53;
    
    const dcBase = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.02, 0.15), matMet); dcBase.position.set(-0.4, 0.765, -0.15);
    const dcStand = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.4), matMet); dcStand.position.set(-0.4, 0.965, -0.2);
    const dcHead = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.02, 0.12), matMet); dcHead.position.set(-0.4, 1.165, -0.15);
    
    g.add(top, frame, legL, legR, dcBase, dcStand, dcHead);
    return g;
}

function bBoltStand() {
    const g = new THREE.Group(); g.position.set(-3.25, 1.6, -4.1);
    
    const poster = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.9, 1.4), new THREE.MeshStandardMaterial({color:0xffffff}));
    poster.position.set(0, 0.5, 0);
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.04, 1.4), matWood);
    shelf.position.set(0.1, 0, 0);
    
    const boltGroup = new THREE.Group();
    boltGroup.position.set(0.15, 0.1, 0);
    
    const hexHead = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.08, 6), matBoltHead);
    hexHead.rotation.x = Math.PI / 2; hexHead.rotation.z = Math.PI / 2; hexHead.position.set(-0.1, 0, 0);
    
    const threadBody = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.25, 16), matBoltThread);
    threadBody.rotation.z = Math.PI / 2; threadBody.position.set(0.065, 0, 0);
    
    boltGroup.add(hexHead, threadBody);
    
    explodeParts.push({mesh: hexHead, basePos: new THREE.Vector3(-0.1, 0, 0), explodePos: new THREE.Vector3(-0.3, 0, 0)});
    explodeParts.push({mesh: threadBody, basePos: new THREE.Vector3(0.065, 0, 0), explodePos: new THREE.Vector3(0.2, 0, 0)});
    
    g.add(poster, shelf, boltGroup);
    return g;
}

[-2.4, -1.1, 0.2, 1.5].forEach(z => {
    const k1 = bDeskA2(-2, z); reg(k1, "INT_DeskA2"); 
    const k2 = bDeskA2(-0.2, z); reg(k2, "INT_DeskA2"); 
    grpProj.add(k1, k2);
});
[-1.1, 0.2, 1.5].forEach(z => {
    const c = bDeskA2(2, z); reg(c, "INT_DeskA2"); grpProj.add(c);
});

const tDesk = bTeacherDesk(2.0, 3.8); tDesk.rotation.y = Math.PI; reg(tDesk, "INT_DocCam"); grpProj.add(tDesk);
const brd = new THREE.Mesh(new THREE.BoxGeometry(3, 1.2, 0.05), new THREE.MeshStandardMaterial({color: 0xeeeeee})); brd.position.set(-0.3, 1.6, 4.45); reg(brd, "INT_Board");
const cab = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.9, 0.6), matWood); cab.position.set(2.1, 0.45, 4.1);
const bStand = bBoltStand(); reg(bStand, "INT_BoltStand");
grpProj.add(brd, cab, bStand);

Object.keys(DB).forEach(k => { if(DB[k].labelPos) createLabel(DB[k].labelText, DB[k].labelPos, k); });

function createOldDesk(x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z);
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.03, 0.5), new THREE.MeshStandardMaterial({color:0xe5e7eb})); top.position.y = 0.74;
    g.add(top); return g;
}
[-2.0, 0, 2.0].forEach(x => { [-2.8, -1.5, -0.2, 1.1, 2.4].forEach(z => { grpOld.add(createOldDesk(x, z)); });});
grpOld.visible = false;

const bA = document.getElementById('btn-mode-after'); const bB = document.getElementById('btn-mode-before'); const bC = document.getElementById('btn-mode-blueprint');

function setMode(m) {
    [bA, bB, bC].forEach(b => b.classList.remove('active'));
    if(m !== 'blueprint' && activeCamera === orthoCamera) { activeCamera = perspCamera; blueprintGrid.visible = false; ui.gostOverlay.classList.remove('active'); }
    if(m === 'proj') { bA.classList.add('active'); grpProj.visible = true; grpOld.visible = false; ui.statusMsg.textContent = "Режим: Утвержденный Проект"; }
    else if(m === 'old') { bB.classList.add('active'); grpProj.visible = false; grpOld.visible = true; ui.statusMsg.textContent = "Режим: Исходник (Пусто)"; ui.propPanel.classList.remove('open'); ui.viewport.classList.remove('panel-open'); }
    else { bC.classList.add('active'); activeCamera = orthoCamera; blueprintGrid.visible = true; ui.gostOverlay.classList.add('active'); ui.statusMsg.textContent = "Режим: Чертеж (Вид сверху)"; ui.propPanel.classList.remove('open'); ui.viewport.classList.remove('panel-open'); }
    if(tourActive) toggleTour();
}
bA.addEventListener('click', () => setMode('proj')); bB.addEventListener('click', () => setMode('old')); bC.addEventListener('click', () => setMode('blueprint'));

ui.labelsBtn.addEventListener('click', () => {
    showLabels = !showLabels;
    ui.labelsBtn.classList.toggle('active', showLabels);
    labels.forEach(l => l.classList.toggle('hidden', !showLabels));
});

ui.explodeBtn.addEventListener('click', () => {
    isExploded = !isExploded;
    ui.explodeBtn.classList.toggle('active', isExploded);
    
    if (isExploded && activeCamera === perspCamera) {
        gsap.to(perspCamera.position, {x: -1.5, y: 1.8, z: -2.0, duration: 1.2, ease: "power2.out"});
        gsap.to(controls.target, {x: -3.2, y: 1.7, z: -4.1, duration: 1.2, ease: "power2.out"});
        ui.statusBar.classList.add('warning');
        ui.statusMsg.textContent = "Анализ: Устройство болтового соединения";
    } else {
        ui.statusBar.classList.remove('warning');
        ui.statusMsg.textContent = "Готово";
    }

    explodeParts.forEach(part => {
        const targetPos = isExploded ? part.explodePos : part.basePos;
        gsap.to(part.mesh.position, {x: targetPos.x, y: targetPos.y, z: targetPos.z, duration: 0.8, ease: "back.out(1.2)"});
    });
});

let tourActive = false; let tourTimer = null; let tourIdx = 0;
function nextTourStep() {
    if(!tourActive) return;
    const v = CAMS[tourKeys[tourIdx]];
    if(activeCamera === orthoCamera) setMode('proj');
    gsap.to(perspCamera.position, {x: v.p.x, y: v.p.y, z: v.p.z, duration: 2.8, ease: "power2.inOut"});
    gsap.to(controls.target, {x: v.t.x, y: v.t.y, z: v.t.z, duration: 2.8, ease: "power2.inOut"});
    tourIdx = (tourIdx + 1) % tourKeys.length;
    tourTimer = setTimeout(nextTourStep, 5000);
}
function toggleTour() {
    tourActive = !tourActive;
    if(tourActive) {
        ui.tourBtn.classList.add('active'); ui.tourIndicator.classList.add('visible'); ui.statusMsg.textContent = "Автопилот";
        ui.propPanel.classList.remove('open'); ui.viewport.classList.remove('panel-open'); ui.camMenu.style.display = 'none';
        tourIdx = 0; nextTourStep();
    } else {
        ui.tourBtn.classList.remove('active'); ui.tourIndicator.classList.remove('visible');
        clearTimeout(tourTimer); ui.statusMsg.textContent = "Готово";
    }
}
ui.tourBtn.addEventListener('click', toggleTour);

document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', e => {
        if(tourActive) toggleTour();
        const v = CAMS[e.target.dataset.view]; if(!v) return;
        if(activeCamera === orthoCamera) setMode('proj');
        gsap.to(perspCamera.position, {x: v.p.x, y: v.p.y, z: v.p.z, duration: 1.2, ease: "power2.inOut"});
        gsap.to(controls.target, {x: v.t.x, y: v.t.y, z: v.t.z, duration: 1.2, ease: "power2.inOut"});
        ui.camMenu.style.display = 'none';
    });
});

const ray = new THREE.Raycaster(); const ms = new THREE.Vector2(); let pt = {x:0, y:0};
// ИСПРАВЛЕНИЕ: Клик обрабатывается на основном холсте (отключен pointer-events на метках для мыши)
renderer.domElement.addEventListener('pointerdown', e => { pt = {x: e.clientX, y: e.clientY}; });
renderer.domElement.addEventListener('pointerup', e => {
    if(Math.hypot(e.clientX - pt.x, e.clientY - pt.y) > 5 || !grpProj.visible) return;
    if(tourActive) toggleTour();
    const bR = container.getBoundingClientRect();
    ms.x = ((e.clientX - bR.left) / bR.width) * 2 - 1; ms.y = -((e.clientY - bR.top) / bR.height) * 2 + 1;
    ray.setFromCamera(ms, activeCamera);
    const hit = ray.intersectObjects(meshes, false)[0];
    if(hit && DB[hit.object.userData.k]) openProps(hit.object.userData.root, DB[hit.object.userData.k]);
});

function openProps(grp, d, fromLabel=false) {
    if(tourActive) toggleTour();
    if(activeCamera === perspCamera && grp && !fromLabel) {
        const b = new THREE.Box3().setFromObject(grp); const c = new THREE.Vector3(); b.getCenter(c);
        gsap.to(perspCamera.position, {x: c.x+d.camOffset.x, y: c.y+d.camOffset.y, z: c.z+d.camOffset.z, duration: 0.8, ease: "power2.out"});
        gsap.to(controls.target, {x: c.x, y: c.y, z: c.z, duration: 0.8, ease: "power2.out"});
    }
    document.getElementById('prop-tag').textContent = d.tag; document.getElementById('prop-title').textContent = d.title; document.getElementById('prop-desc').textContent = d.desc;
    
    const sp = document.getElementById('prop-specs'); sp.style.display = 'grid';
    sp.innerHTML = d.specs.map(s => `<div class="specs-cell">${s[0]}</div><div class="specs-cell">${s[1]}</div>`).join('');
    
    ui.propPanel.classList.add('open'); if(window.innerWidth > 768) ui.viewport.classList.add('panel-open');
}

const loader = new GLTFLoader(); const draco = new DRACOLoader(); draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/'); loader.setDRACOLoader(draco);
document.getElementById('file-upload').addEventListener('change', e => {
    const f = e.target.files[0]; if(!f) return;
    const l = document.getElementById('loader'); document.getElementById('loader-text').textContent = 'Парсинг геометрии...';
    l.style.display = 'flex'; setTimeout(() => l.style.opacity = '1', 10);
    loader.load(URL.createObjectURL(f), gltf => {
        grpProj.clear(); meshes.length = 0;
        labels.forEach(l => l.remove()); labels.length = 0;
        gltf.scene.traverse(c => {
            if(c.isMesh) {
                c.castShadow = true; c.receiveShadow = true;
                Object.keys(DB).forEach(k => { if(c.name.startsWith(k)) { c.userData = {k: k, root: c}; meshes.push(c); } });
            }
        });
        grpProj.add(gltf.scene); setMode('proj');
        setTimeout(() => { l.style.opacity = '0'; setTimeout(() => l.style.display = 'none', 300); }, 500);
    });
});

window.addEventListener('resize', () => {
    const w = container.clientWidth, h = container.clientHeight, a = w / h;
    perspCamera.aspect = a; perspCamera.updateProjectionMatrix();
    const ffs = w < 768 ? 13 : 10; orthoCamera.left = -ffs*a/2; orthoCamera.right = ffs*a/2; orthoCamera.top = ffs/2; orthoCamera.bottom = -ffs/2; orthoCamera.updateProjectionMatrix();
    renderer.setSize(w, h); labelRenderer.setSize(w, h);
});

// ИСПРАВЛЕНИЕ: Безопасное скрытие лоадера, защита от ошибки null
setTimeout(() => {
    const l = document.getElementById('loader'); 
    if (l) {
        l.style.opacity = '0'; 
        setTimeout(() => { if (l) l.style.display = 'none'; }, 300);
    }
}, 800);

function animate() { 
    requestAnimationFrame(animate); 
    if(activeCamera === perspCamera) controls.update(); 
    renderer.render(scene, activeCamera); 
    if(showLabels && activeCamera === perspCamera) labelRenderer.render(scene, activeCamera);
}
animate();
