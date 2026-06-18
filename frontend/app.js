/**
 * J.A.R.V.I.S. MARK V - CORE LOGIC & AUDIO SYNTHESIS
 * Architecture by Google AI Studio (LLM Council)
 */

// ==========================================
// 1. AUDIO SYNTHESIZER (Web Audio API)
// ==========================================
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

const JarvisAudio = {
    playSweep: function() {
        if(audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        // Power up sweep sound
        osc.type = 'sine';
        osc.frequency.setValueAtTime(50, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 1.5);
        
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.5);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1.5);

        osc.start(audioCtx.currentTime);
        osc.stop(audioCtx.currentTime + 1.5);
    },

    playHoverTick: function() {
        if(audioCtx.state === 'suspended') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.type = 'square';
        osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.05);

        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);

        osc.start(audioCtx.currentTime);
        osc.stop(audioCtx.currentTime + 0.05);
    },

    playTypeSound: function() {
        if(audioCtx.state === 'suspended') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(600 + Math.random()*200, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.03);

        osc.start(audioCtx.currentTime);
        osc.stop(audioCtx.currentTime + 0.03);
    },

    playConfirm: function() {
        if(audioCtx.state === 'suspended') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
        osc.frequency.setValueAtTime(1760, audioCtx.currentTime + 0.1); // A6

        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);

        osc.start(audioCtx.currentTime);
        osc.stop(audioCtx.currentTime + 0.3);
    }
};

// ==========================================
// 2. STARTUP SEQUENCE
// ==========================================
window.addEventListener('load', () => {
    // Requires a click to start audio context due to browser policies
    document.body.addEventListener('click', initBootSequence, { once: true });
    document.getElementById('startup-text').innerText = "CLICK TO INITIALIZE J.A.R.V.I.S. PROTOCOLS";
});

function initBootSequence() {
    JarvisAudio.playSweep();
    document.getElementById('startup-text').innerText = "POWERING ON CORE SYSTEMS...";
    
    let fill = 0;
    const bar = document.getElementById('startup-fill');
    
    const bootInterval = setInterval(() => {
        fill += Math.random() * 15;
        if(fill >= 100) {
            fill = 100;
            clearInterval(bootInterval);
            document.getElementById('startup-text').innerText = "SYSTEMS ONLINE";
            setTimeout(() => {
                document.getElementById('startup-overlay').style.opacity = '0';
                document.querySelector('.hud-container').classList.add('active');
                setTimeout(() => document.getElementById('startup-overlay').remove(), 1500);
            }, 500);
        }
        bar.style.width = fill + '%';
    }, 100);
}

// ==========================================
// 3. 3D BACKGROUND ENGINE (Three.js)
// ==========================================
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

// Iron Man Core Wireframe Sphere
const geometry = new THREE.IcosahedronGeometry(4, 2);
const material = new THREE.MeshBasicMaterial({ 
    color: 0x00e5ff, 
    wireframe: true, 
    transparent: true, 
    opacity: 0.15 
});
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Outer Ring
const ringGeo = new THREE.TorusGeometry(6, 0.05, 16, 100);
const ringMat = new THREE.MeshBasicMaterial({ color: 0xffb300, transparent: true, opacity: 0.3 });
const ring = new THREE.Mesh(ringGeo, ringMat);
ring.rotation.x = Math.PI / 2;
scene.add(ring);

camera.position.z = 10;

function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.y += 0.002;
    sphere.rotation.x += 0.001;
    ring.rotation.z -= 0.005;
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ==========================================
// 4. UI INTERACTIONS & BINDINGS
// ==========================================

// Hover sounds for buttons and elements
document.querySelectorAll('.cyber-btn, .ai-node').forEach(el => {
    el.addEventListener('mouseenter', () => JarvisAudio.playHoverTick());
});

// Chat logic
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatWindow = document.getElementById('chat-window');

chatInput.addEventListener('keydown', (e) => {
    JarvisAudio.playTypeSound();
    if(e.key === 'Enter') {
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

function sendMessage() {
    const text = chatInput.value.trim();
    if(!text) return;
    
    JarvisAudio.playConfirm();

    // User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.innerHTML = `<div class="msg-author">USER</div><div class="msg-text">${text}</div>`;
    chatWindow.appendChild(userMsg);
    
    chatInput.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Simulate JARVIS Network Response via REST API (Using the /api/chat endpoint from FastAPI if it existed, or just mock it)
    setTimeout(() => {
        const sysMsg = document.createElement('div');
        sysMsg.className = 'message system';
        sysMsg.innerHTML = `<div class="msg-author">J.A.R.V.I.S.</div><div class="msg-text">Directiva "${text}" recibida. Enrutando al nodo correspondiente del enjambre...</div>`;
        chatWindow.appendChild(sysMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        JarvisAudio.playHoverTick();
    }, 800);
}

// Random telemetry updates to simulate live data
setInterval(() => {
    document.querySelectorAll('.t-bar-fill').forEach(bar => {
        if(!bar.classList.contains('warning')) {
            const current = parseFloat(bar.style.width);
            const delta = (Math.random() - 0.5) * 5;
            bar.style.width = Math.max(10, Math.min(100, current + delta)) + '%';
        }
    });
}, 2000);
