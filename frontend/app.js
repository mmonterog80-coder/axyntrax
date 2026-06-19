/**
 * J.A.R.V.I.S. MARK VI - 8K 3D WEBGL ENGINE
 * Powered by Three.js & Web Audio API
 */

// ==========================================
// 1. AUDIO SYNTHESIZER (JarvisAudioSynth)
// ==========================================
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

const JarvisAudio = {
    playSweep: function() {
        if(audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(30, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 2.0);
        
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 1.0);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 2.0);

        osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 2.0);
    },
    playTick: function() {
        if(audioCtx.state === 'suspended') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

        osc.type = 'square';
        osc.frequency.setValueAtTime(1500, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(500, audioCtx.currentTime + 0.05);

        gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);

        osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 0.05);
    },
    playTargetLock: function() {
        if(audioCtx.state === 'suspended') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(2000, audioCtx.currentTime);
        osc.frequency.setValueAtTime(3000, audioCtx.currentTime + 0.1);

        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.1, audioCtx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);

        osc.start(audioCtx.currentTime); osc.stop(audioCtx.currentTime + 0.2);
    }
};

// ==========================================
// 2. BOOT SEQUENCE
// ==========================================
window.addEventListener('load', () => {
    document.body.addEventListener('click', initBootSequence, { once: true });
});

function initBootSequence() {
    JarvisAudio.playSweep();
    document.getElementById('startup-text').innerText = "BIOMETRIC ACCEPTED. BOOTING CORE...";
    
    let fill = 0;
    const bar = document.getElementById('startup-fill');
    
    const bootInterval = setInterval(() => {
        fill += Math.random() * 20;
        if(fill >= 100) {
            fill = 100;
            clearInterval(bootInterval);
            document.getElementById('startup-text').innerText = "SWARM ONLINE";
            setTimeout(() => {
                document.getElementById('startup-overlay').style.opacity = '0';
                document.getElementById('ui-layer').classList.add('active');
                setTimeout(() => document.getElementById('startup-overlay').remove(), 2000);
            }, 500);
        }
        bar.style.width = fill + '%';
    }, 100);
}

// ==========================================
// 3. THREE.JS 3D ENGINE & BLOOM POST-PROCESSING
// ==========================================
const canvas = document.getElementById('webgl-canvas');
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x020202, 0.015);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 25);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: false, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = THREE.ReinhardToneMapping;

// PostProcessing (Unreal Bloom Pass for Epic Glow)
const renderScene = new THREE.RenderPass(scene, camera);
const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 3.5, 0.8, 0.1);
const composer = new THREE.EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

// Group for the entire Core
const coreGroup = new THREE.Group();
scene.add(coreGroup);

// Materials
const matCyan = new THREE.MeshBasicMaterial({ color: 0x00e5ff, wireframe: true, transparent: true, opacity: 0.2 });
const matCyanBright = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true, transparent: true, opacity: 0.8 });
const matGold = new THREE.MeshBasicMaterial({ color: 0xffb300, wireframe: true, transparent: true, opacity: 0.4 });
const matSolidCyan = new THREE.MeshBasicMaterial({ color: 0x00e5ff });
const pointMat = new THREE.PointsMaterial({ color: 0x00e5ff, size: 0.05, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending });

// Central Core (JARVIS)
// 1. Inner Point Sphere
const innerSphereGeo = new THREE.SphereGeometry(3.8, 32, 32);
const innerSphere = new THREE.Points(innerSphereGeo, pointMat);
coreGroup.add(innerSphere);

// 2. Outer Wireframe Icosahedron
const jarvisCore = new THREE.Mesh(new THREE.IcosahedronGeometry(4.2, 3), matCyanBright);
coreGroup.add(jarvisCore);

// Outer Rings (Complex and Dashed)
const ringGeo1 = new THREE.TorusGeometry(8, 0.05, 16, 100);
const ring1 = new THREE.Mesh(ringGeo1, matGold);
ring1.rotation.x = Math.PI / 2;
coreGroup.add(ring1);

// Dashed Ring 2
const ringGeo2 = new THREE.TorusGeometry(12, 0.02, 16, 150);
const matDashed = new THREE.LineDashedMaterial({ color: 0x00e5ff, dashSize: 0.5, gapSize: 0.2, transparent: true, opacity: 0.8 });
const edges = new THREE.EdgesGeometry(ringGeo2);
const ring2 = new THREE.LineSegments(edges, matDashed);
ring2.computeLineDistances();
ring2.rotation.y = Math.PI / 4;
coreGroup.add(ring2);

// Ring 3 (Outer Gold)
const ringGeo3 = new THREE.TorusGeometry(15, 0.01, 16, 100);
const ring3 = new THREE.Mesh(ringGeo3, matGold);
ring3.rotation.x = Math.PI / 3;
coreGroup.add(ring3);

// AI Swarm Nodes
const aiNames = ["Gemini 1.5", "DeepSeek V3", "Qwen 2.5", "Claude 3.5", "GPT-4o", "Kimi", "Stitch", "Nano", "Banana2", "Llama 3", "AlphaFold", "JARVIS Core"];
const nodes = [];
const orbitRadius = 18;

aiNames.forEach((name, i) => {
    const angle = (i / aiNames.length) * Math.PI * 2;
    
    // Each node is a complex mini-core
    const nodeGroup = new THREE.Group();
    
    const mesh = new THREE.Mesh(new THREE.OctahedronGeometry(0.8, 1), matSolidCyan);
    const wire = new THREE.Mesh(new THREE.IcosahedronGeometry(1.2, 1), matGold);
    nodeGroup.add(mesh);
    nodeGroup.add(wire);
    
    // Position in orbit
    nodeGroup.position.x = Math.cos(angle) * orbitRadius;
    nodeGroup.position.z = Math.sin(angle) * orbitRadius;
    nodeGroup.position.y = (Math.random() - 0.5) * 6;
    
    // Use the inner mesh for raycasting
    mesh.userData = { name: name, angle: angle, speed: 0.003 + Math.random() * 0.004, parentGroup: nodeGroup };
    
    coreGroup.add(nodeGroup);
    nodes.push(mesh);
});

// Hexagonal Grid Floor
const gridHelper = new THREE.PolarGridHelper(30, 16, 8, 64, 0x00e5ff, 0x00e5ff);
gridHelper.position.y = -8;
gridHelper.material.opacity = 0.15;
gridHelper.material.transparent = true;
scene.add(gridHelper);

// Particles
const partsGeo = new THREE.BufferGeometry();
const partsCount = 1000;
const posArray = new Float32Array(partsCount * 3);
for(let i=0; i<partsCount*3; i++) {
    posArray[i] = (Math.random() - 0.5) * 60;
}
partsGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const partsMat = new THREE.PointsMaterial({ size: 0.1, color: 0x00e5ff, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending });
const particlesMesh = new THREE.Points(partsGeo, partsMat);
scene.add(particlesMesh);

// ==========================================
// 4. RAYCASTING & INTERACTION
// ==========================================
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hoveredNode = null;

const targetInfoBox = document.getElementById('target-info');
const tName = document.getElementById('t-name');
const tHex = document.getElementById('t-hex');
const tLat = document.getElementById('t-lat');

window.addEventListener('mousemove', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

// ==========================================
// 5. ANIMATION LOOP
// ==========================================
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Rotate Core
    jarvisCore.rotation.y += 0.002;
    jarvisCore.rotation.x += 0.001;
    
    // Rotate Rings
    ring1.rotation.z -= 0.005;
    ring2.rotation.x += 0.003;
    ring2.rotation.y += 0.002;
    
    // Orbit Nodes
    nodes.forEach(node => {
        const pGroup = node.userData.parentGroup;
        node.userData.angle += node.userData.speed;
        
        // Orbit the whole group
        pGroup.position.x = Math.cos(node.userData.angle) * orbitRadius;
        pGroup.position.z = Math.sin(node.userData.angle) * orbitRadius;
        
        // Rotate the individual geometries inside
        pGroup.rotation.x += 0.01;
        pGroup.rotation.y += 0.02;
    });

    // Particles float
    particlesMesh.rotation.y = elapsedTime * 0.02;

    // Raycaster Logic
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodes);
    
    if (intersects.length > 0) {
        const object = intersects[0].object;
        if (hoveredNode !== object) {
            if (hoveredNode) hoveredNode.material.color.setHex(0x00e5ff); // Reset prev
            hoveredNode = object;
            hoveredNode.material.color.setHex(0xffb300); // Highlight Gold
            JarvisAudio.playTargetLock();
            
            // Show UI
            targetInfoBox.classList.remove('hidden');
            tName.innerText = hoveredNode.userData.name;
            tHex.innerText = Math.floor(Math.random()*65535).toString(16).toUpperCase();
            tLat.innerText = Math.floor(Math.random()*20 + 2);
        }
    } else {
        if (hoveredNode) {
            hoveredNode.material.color.setHex(0x00e5ff);
            hoveredNode = null;
            targetInfoBox.classList.add('hidden');
        }
    }

    composer.render();
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
});

// ==========================================
// 6. TERMINAL LOGIC
// ==========================================
const chatInput = document.getElementById('chat-input');
const chatWindow = document.getElementById('chat-window');

chatInput.addEventListener('keydown', (e) => {
    JarvisAudio.playTick();
    if(e.key === 'Enter' && chatInput.value.trim() !== '') {
        const text = chatInput.value.trim();
        chatInput.value = '';
        
        // Add User MSG
        appendMsg('USER', text, 'user');
        JarvisAudio.playTargetLock();
        
        // Mock JARVIS Reply
        setTimeout(() => {
            appendMsg('J.A.R.V.I.S.', `Directive [${text}] synced across all ${nodes.length} nodes via WebGL pipeline.`, 'system');
            JarvisAudio.playTick();
        }, 600);
    }
});

function appendMsg(author, text, type) {
    const div = document.createElement('div');
    div.className = `message ${type}`;
    div.innerHTML = `<span class="msg-author">${author}:</span> ${text}`;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ==========================================
// 7. MARK VII - TACTICAL PANELS LOGIC
// ==========================================

// Chronos Clock
function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
    const dateStr = now.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
    const elTime = document.getElementById('c-time');
    const elDate = document.getElementById('c-date');
    if(elTime) elTime.innerText = timeStr;
    if(elDate) elDate.innerText = dateStr.replace(/\//g, '-');
}
setInterval(updateClock, 1000);
updateClock();

// Fetch Swarm Status
async function fetchSwarmStatus() {
    try {
        const res = await fetch('/api/swarm/status');
        const data = await res.json();
        const list = document.getElementById('swarm-list');
        if(!list) return;
        
        list.innerHTML = '';
        data.swarm.forEach(dept => {
            // Render Department (Director)
            list.innerHTML += `
                <div class="swarm-node-item" style="border-left-color: #ffb300;">
                    <div>
                        <div class="sn-name" style="color: #ffb300;">[DIR] ${dept.name}</div>
                        <div class="sn-role">${dept.role}</div>
                    </div>
                    <div class="sn-status">
                        <span style="font-size:0.7rem;">${dept.mem}</span>
                        <div class="led ${dept.status}"></div>
                    </div>
                </div>
            `;
            
            // Render Sub-Agents
            if(dept.sub_agents && dept.sub_agents.length > 0) {
                dept.sub_agents.forEach(sub => {
                    list.innerHTML += `
                        <div class="swarm-node-item" style="margin-left: 15px; border-left-color: #00e5ff; background: rgba(0, 229, 255, 0.02);">
                            <div>
                                <div class="sn-name" style="font-size: 0.75rem;">└ ${sub.name}</div>
                                <div class="sn-role" style="font-size: 0.6rem;">${sub.role}</div>
                            </div>
                            <div class="sn-status">
                                <span style="font-size:0.6rem;">${sub.mem}</span>
                                <div class="led ${sub.status}" style="width:6px; height:6px;"></div>
                            </div>
                        </div>
                    `;
                });
            }
        });
    } catch(err) {
        console.error("Swarm Fetch Error:", err);
    }
}

// Fetch Inbox
async function fetchInbox() {
    try {
        const res = await fetch('/api/mail/inbox');
        const data = await res.json();
        const list = document.getElementById('inbox-list');
        if(!list) return;
        
        list.innerHTML = '';
        data.inbox.forEach(mail => {
            const isUnread = mail.status === 'unread' ? 'unread' : '';
            const btnHtml = mail.status !== 'replied' ? 
                `<button class="cyber-btn-sm" onclick="respondToMail('${mail.id}')">AUTO-REPLY (JARVIS)</button>` : 
                `<span style="color:#00ff00; font-size:0.7rem;">[REPLIED]</span>`;
                
            list.innerHTML += `
                <div class="mail-item ${isUnread}">
                    <div class="m-from">${mail.from}</div>
                    <div class="m-subject">${mail.subject}</div>
                    <div class="m-body">${mail.body}</div>
                    ${btnHtml}
                </div>
            `;
        });
    } catch(err) {
        console.error("Inbox Fetch Error:", err);
    }
}

// Auto-Reply Logic
window.respondToMail = async function(mailId) {
    JarvisAudio.playTick();
    appendMsg('J.A.R.V.I.S.', `Processing mail ${mailId}... Routing to DeepSeek V3 for response generation.`, 'system');
    
    try {
        const res = await fetch('/api/mail/respond', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mail_id: mailId})
        });
        const data = await res.json();
        
        if(data.status === 'success') {
            JarvisAudio.playTargetLock();
            appendMsg('J.A.R.V.I.S.', `Response sent: "${data.jarvis_response}"`, 'system');
            fetchInbox(); // Refresh UI
        }
    } catch (err) {
        appendMsg('J.A.R.V.I.S.', `Error responding to mail: ${err.message}`, 'system');
    }
}

// Initial Fetchs
window.addEventListener('load', () => {
    setTimeout(fetchSwarmStatus, 3000);
    setTimeout(fetchInbox, 3500);
    // Poll swarm status every 10s
    setInterval(fetchSwarmStatus, 10000);
});
