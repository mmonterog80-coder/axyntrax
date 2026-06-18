// 3D Background with Three.js
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

// Particles
const geometry = new THREE.BufferGeometry();
const particlesCount = 1500;
const posArray = new Float32Array(particlesCount * 3);

for(let i = 0; i < particlesCount * 3; i++) {
    // Spread particles around
    posArray[i] = (Math.random() - 0.5) * 10;
}

geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

// Particle Material (Cyan/Purple glow)
const material = new THREE.PointsMaterial({
    size: 0.02,
    color: 0x00f3ff,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
});

const particlesMesh = new THREE.Points(geometry, material);
scene.add(particlesMesh);

camera.position.z = 3;

// Mouse tracking
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) - 0.5;
    mouseY = (event.clientY / window.innerHeight) - 0.5;
});

const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    particlesMesh.rotation.y = elapsedTime * 0.05;
    particlesMesh.rotation.x = elapsedTime * 0.02;

    // Interactive mouse movement
    particlesMesh.rotation.y += mouseX * 0.1;
    particlesMesh.rotation.x += mouseY * 0.1;

    // Color shifting based on time
    const hue = Math.abs(Math.sin(elapsedTime * 0.2)) * 0.2 + 0.5; // shift between cyan and purple
    material.color.setHSL(hue, 1.0, 0.5);

    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// UI Logic
const ais = [
    { name: "DeepSeek Coder", status: "ONLINE", color: "#0f0" },
    { name: "Gemini 2.5 Pro", status: "STANDBY", color: "#ffaa00" },
    { name: "Kimi (Moonshot)", status: "STANDBY", color: "#ffaa00" },
    { name: "Qwen 3 Max", status: "ONLINE", color: "#0f0" },
    { name: "ElevenLabs", status: "READY", color: "#0f0" },
    { name: "Fish Audio", status: "ONLINE", color: "#0f0" },
    { name: "Supabase DB", status: "SYNCED", color: "#0f0" }
];

const aiList = document.getElementById('ai-nodes');
ais.forEach(ai => {
    const div = document.createElement('div');
    div.className = 'ai-node';
    div.innerHTML = `
        <span class="ai-name">${ai.name}</span>
        <span class="ai-status" style="color: ${ai.color}; text-shadow: 0 0 5px ${ai.color}">${ai.status}</span>
    `;
    aiList.appendChild(div);
});

// Chat Logic
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(sender, text) {
    const msg = document.createElement('div');
    msg.className = `message ${sender.toLowerCase()}`;
    msg.innerText = sender === 'JARVIS' ? `[JARVIS] ${text}` : `[USER] ${text}`;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    addMessage('USER', text);
    chatInput.value = '';

    // Typing indicator
    const typing = document.createElement('div');
    typing.className = `message jarvis`;
    typing.innerText = `[JARVIS] Procesando consulta en el enjambre...`;
    chatWindow.appendChild(typing);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        
        // Remove typing
        chatWindow.removeChild(typing);
        addMessage('JARVIS', data.reply);

        if (data.audio) {
            const snd = new Audio("data:audio/mp3;base64," + data.audio);
            snd.play();
        }
    } catch (err) {
        chatWindow.removeChild(typing);
        addMessage('JARVIS', 'Error de conexión con el núcleo lógico.');
    }
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
