import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";
import { Streamlit } from "streamlit-component-lib";

// ==========================================
// 1. STREAMLIT COMPONENT COMMUNICATION
// ==========================================

const COMPONENT_HEIGHT = 650;

Streamlit.setComponentReady();
Streamlit.setFrameHeight(COMPONENT_HEIGHT);


// ==========================================
// 2. SCENE SETUP
// ==========================================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101827);

const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

camera.position.set(6, 5, 8);

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

document.body.style.margin = "0";
document.body.style.padding = "0";
document.body.style.overflow = "hidden";
document.body.style.background = "#101827";

document.body.appendChild(renderer.domElement);


// ==========================================
// 3. CAMERA CONTROLS
// ==========================================

const orbit = new OrbitControls(
    camera,
    renderer.domElement
);

orbit.enableDamping = true;
orbit.target.set(0, 0, 0);

orbit.minDistance = 5;
orbit.maxDistance = 15;


// ==========================================
// 4. LIGHTING
// ==========================================

scene.add(
    new THREE.AmbientLight(0xffffff, 1.5)
);

const directionalLight = new THREE.DirectionalLight(
    0xffffff,
    3
);

directionalLight.position.set(5, 8, 6);
directionalLight.castShadow = true;

scene.add(directionalLight);


// ==========================================
// 5. MATERIALS
// ==========================================

const discMaterial = new THREE.MeshStandardMaterial({
    color: 0xb87333,
    metalness: 0.85,
    roughness: 0.3
});

const steelMaterial = new THREE.MeshStandardMaterial({
    color: 0x9ca3af,
    metalness: 0.9,
    roughness: 0.25
});

const motorMaterial = new THREE.MeshStandardMaterial({
    color: 0x334155,
    metalness: 0.65,
    roughness: 0.4
});


// ==========================================
// 6. ROTATING DISC ASSEMBLY
// ==========================================

const rotatingAssembly = new THREE.Group();
scene.add(rotatingAssembly);


// Copper disc

const discGeometry = new THREE.CylinderGeometry(
    2,
    2,
    0.16,
    96
);

const disc = new THREE.Mesh(
    discGeometry,
    discMaterial
);

disc.rotation.x = Math.PI / 2;
disc.castShadow = true;
disc.receiveShadow = true;

rotatingAssembly.add(disc);


// Radial marker

const markerGeometry = new THREE.BoxGeometry(
    0.09,
    1.55,
    0.035
);

const markerMaterial = new THREE.MeshStandardMaterial({
    color: 0xfacc15,
    metalness: 0.4,
    roughness: 0.35
});

const marker = new THREE.Mesh(
    markerGeometry,
    markerMaterial
);

marker.position.set(0.75, 0, 0.095);

rotatingAssembly.add(marker);


// Central hub

const hubGeometry = new THREE.CylinderGeometry(
    0.35,
    0.35,
    0.22,
    48
);

const hub = new THREE.Mesh(
    hubGeometry,
    steelMaterial
);

hub.rotation.x = Math.PI / 2;

rotatingAssembly.add(hub);


// ==========================================
// 7. STATIONARY SHAFT
// ==========================================

const shaftGeometry = new THREE.CylinderGeometry(
    0.13,
    0.13,
    2.4,
    32
);

const shaft = new THREE.Mesh(
    shaftGeometry,
    steelMaterial
);

shaft.rotation.x = Math.PI / 2;
shaft.position.z = -1.1;

scene.add(shaft);


// ==========================================
// 8. STATIONARY MOTOR
// ==========================================

const motorGeometry = new THREE.CylinderGeometry(
    0.65,
    0.65,
    1.1,
    48
);

const motor = new THREE.Mesh(
    motorGeometry,
    motorMaterial
);

motor.rotation.x = Math.PI / 2;
motor.position.z = -2;

scene.add(motor);


// ==========================================
// 9. MAGNET ASSEMBLIES
// ==========================================

function createMagnet(
    bodyColor,
    poleColor,
    poleLabel,
    zPosition
) {

    const group = new THREE.Group();

    const bodyGeometry = new THREE.BoxGeometry(
        0.75,
        0.75,
        0.45
    );

    const bodyMaterial = new THREE.MeshStandardMaterial({
        color: bodyColor,
        metalness: 0.35,
        roughness: 0.4
    });

    const body = new THREE.Mesh(
        bodyGeometry,
        bodyMaterial
    );

    group.add(body);


    const poleGeometry = new THREE.BoxGeometry(
        0.55,
        0.55,
        0.12
    );

    const poleMaterial = new THREE.MeshStandardMaterial({
        color: poleColor,
        metalness: 0.2,
        roughness: 0.4
    });

    const pole = new THREE.Mesh(
        poleGeometry,
        poleMaterial
    );

    pole.position.z = (
        poleLabel === "N" ? -0.27 : 0.27
    );

    group.add(pole);

    group.position.set(1.2, 0, zPosition);

    scene.add(group);

    return group;
}


const northMagnet = createMagnet(
    0x991b1b,
    0xef4444,
    "N",
    0.65
);

const southMagnet = createMagnet(
    0x1e40af,
    0x3b82f6,
    "S",
    -0.65
);


// ==========================================
// 10. AIR GAP CALCULATION
// ==========================================

const MIN_MAGNET_CENTER = 0.45;
const MAX_MAGNET_CENTER = 1.5;

const GEOMETRY_OFFSET = 0.41;

const REFERENCE_GAP = 0.24;

function getAirGap() {

    return Math.max(
        0.04,
        Math.abs(northMagnet.position.z) - GEOMETRY_OFFSET
    );
}


function setMagnetGap(airGap) {

    const centerDistance = THREE.MathUtils.clamp(
        airGap + GEOMETRY_OFFSET,
        MIN_MAGNET_CENTER,
        MAX_MAGNET_CENTER
    );

    northMagnet.position.z = centerDistance;
    southMagnet.position.z = -centerDistance;
}


// ==========================================
// 11. FLOOR GRID
// ==========================================

const grid = new THREE.GridHelper(
    12,
    20,
    0x475569,
    0x334155
);

grid.position.y = -2.3;

scene.add(grid);


// ==========================================
// 12. MAGNET TRANSFORM CONTROLS
// ==========================================

const transform = new TransformControls(
    camera,
    renderer.domElement
);

transform.setMode("translate");

transform.showX = false;
transform.showY = false;
transform.showZ = true;

transform.setSize(0.8);

scene.add(transform.getHelper());


// Disable camera movement while dragging magnets.

transform.addEventListener(
    "dragging-changed",
    (event) => {

        orbit.enabled = !event.value;

        if (!event.value) {
            reportMagnetGap();
        }
    }
);


// Keep magnets symmetrical.

transform.addEventListener(
    "objectChange",
    () => {

        const selected = transform.object;

        if (!selected) return;

        const centerDistance = THREE.MathUtils.clamp(
            Math.abs(selected.position.z),
            MIN_MAGNET_CENTER,
            MAX_MAGNET_CENTER
        );

        northMagnet.position.z = centerDistance;
        southMagnet.position.z = -centerDistance;
    }
);


// ==========================================
// 13. SEND MAGNET GAP TO PYTHON
// ==========================================

function reportMagnetGap() {

    const airGap = getAirGap();

    Streamlit.setComponentValue({

        air_gap: Number(airGap.toFixed(4)),

        north_position: Number(
            northMagnet.position.z.toFixed(4)
        ),

        south_position: Number(
            southMagnet.position.z.toFixed(4)
        )
    });
}


// ==========================================
// 14. MAGNET SELECTION
// ==========================================

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

renderer.domElement.addEventListener(
    "pointerdown",
    (event) => {

        if (transform.dragging) return;

        const rect = renderer.domElement.getBoundingClientRect();

        pointer.x = (
            (event.clientX - rect.left) / rect.width
        ) * 2 - 1;

        pointer.y = -(
            (event.clientY - rect.top) / rect.height
        ) * 2 + 1;

        raycaster.setFromCamera(pointer, camera);

        const hits = raycaster.intersectObjects(
            [northMagnet, southMagnet],
            true
        );

        if (hits.length > 0) {

            const selectedObject = hits[0].object;

            const magnet =
                selectedObject.parent === northMagnet
                    ? northMagnet
                    : southMagnet;

            transform.attach(magnet);
        }
    }
);


// Double-click to deselect.

renderer.domElement.addEventListener(
    "dblclick",
    () => {
        transform.detach();
    }
);


// ==========================================
// 15. CONTINUOUS PHYSICS SIMULATION STATE
// ==========================================

let simulationRunning = false;

let currentOmega = 0;

let initialOmega = 100;

let momentOfInertia = 0.02;

let baseMagneticField = 0.5;

let systemConstant = 0.05;

let elapsedSimulationTime = 0;

let simulationStartTime = null;

let lastFrameTime = performance.now();

let lastRunId = null;


// Practical visual stopping threshold.
// The mathematical model approaches zero asymptotically.

const STOP_THRESHOLD = 0.03;


// ==========================================
// 16. CALCULATE EFFECTIVE MAGNETIC FIELD
// ==========================================

function calculateEffectiveField() {

    const gap = getAirGap();

    const effectiveField = (
        baseMagneticField *
        Math.pow(
            REFERENCE_GAP / Math.max(gap, 0.04),
            2
        )
    );

    return THREE.MathUtils.clamp(
        effectiveField,
        0.1,
        1.0
    );
}


// ==========================================
// 17. CALCULATE BRAKING COEFFICIENT
// ==========================================

function calculateBrakingCoefficient() {

    const effectiveField = calculateEffectiveField();

    return systemConstant * effectiveField ** 2;
}


// ==========================================
// 18. START SIMULATION
// ==========================================

function startSimulation() {

    currentOmega = initialOmega;

    elapsedSimulationTime = 0;

    simulationStartTime = performance.now();

    lastFrameTime = simulationStartTime;

    rotatingAssembly.rotation.z = 0;

    simulationRunning = true;
}


// ==========================================
// 19. RESET SIMULATION
// ==========================================

function resetSimulation() {

    simulationRunning = false;

    currentOmega = 0;

    elapsedSimulationTime = 0;

    simulationStartTime = null;

    lastFrameTime = performance.now();

    rotatingAssembly.rotation.z = 0;
}


// ==========================================
// 20. CONTINUOUS PHYSICS UPDATE
// ==========================================

function updatePhysics() {

    if (!simulationRunning) {
        return;
    }

    const now = performance.now();

    // Time difference between animation frames.

    const dt = Math.min(
        (now - lastFrameTime) / 1000,
        0.05
    );

    lastFrameTime = now;

    if (dt <= 0) {
        return;
    }

    elapsedSimulationTime += dt;


    // ------------------------------------------
    // GET CURRENT MAGNETIC FIELD
    // ------------------------------------------

    const effectiveField = calculateEffectiveField();


    // ------------------------------------------
    // CALCULATE CURRENT BRAKING COEFFICIENT
    // ------------------------------------------

    const effectiveK = (
        systemConstant * effectiveField ** 2
    );


    // ------------------------------------------
    // APPLY EQUATION OF MOTION
    // ------------------------------------------

    // I(dω/dt) = -kω
    //
    // Exact solution over a small time interval:
    //
    // ω(new) = ω(old) * exp(-k*dt/I)

    const previousOmega = currentOmega;

    currentOmega *= Math.exp(
        -(effectiveK / momentOfInertia) * dt
    );


    // ------------------------------------------
    // CALCULATE ANGULAR DISPLACEMENT
    // ------------------------------------------

    const averageOmega = (
        previousOmega + currentOmega
    ) / 2;

    const angularStep = averageOmega * dt;

    rotatingAssembly.rotation.z += angularStep;


    // ------------------------------------------
    // PRACTICAL STOPPING CONDITION
    // ------------------------------------------

    if (currentOmega <= STOP_THRESHOLD) {

        currentOmega = 0;

        simulationRunning = false;
    }
}


// ==========================================
// 21. RECEIVE PYTHON PARAMETERS
// ==========================================

Streamlit.events.addEventListener(
    Streamlit.RENDER_EVENT,
    (event) => {

        const args = event.detail.args;


        // --------------------------------------
        // UPDATE EXPERIMENTAL PARAMETERS
        // --------------------------------------

        if (args.initial_angular_velocity !== undefined) {

            initialOmega = Math.max(
                0,
                Number(args.initial_angular_velocity)
            );
        }

        if (args.moment_of_inertia !== undefined) {

            momentOfInertia = Math.max(
                0.000001,
                Number(args.moment_of_inertia)
            );
        }

        if (args.magnetic_field !== undefined) {

            baseMagneticField = Math.max(
                0,
                Number(args.magnetic_field)
            );
        }

        if (args.system_constant !== undefined) {

            systemConstant = Math.max(
                0,
                Number(args.system_constant)
            );
        }


        // --------------------------------------
        // INITIAL MAGNET POSITION
        // --------------------------------------

        if (
            args.air_gap !== undefined &&
            !window.eddylabInitialGapSet
        ) {

            setMagnetGap(Number(args.air_gap));

            window.eddylabInitialGapSet = true;
        }


        // --------------------------------------
        // START A NEW SIMULATION
        // --------------------------------------

        const incomingRunId = args.run_id;

        if (
            args.run_simulation === true &&
            incomingRunId !== undefined &&
            incomingRunId !== lastRunId
        ) {

            lastRunId = incomingRunId;

            startSimulation();
        }


        // --------------------------------------
        // RESET
        // --------------------------------------

        if (args.run_simulation === false) {

            resetSimulation();

            lastRunId = null;
        }


        Streamlit.setFrameHeight(
            COMPONENT_HEIGHT
        );
    }
);


// ==========================================
// 22. ANIMATION LOOP
// ==========================================

function animate() {

    requestAnimationFrame(animate);

    updatePhysics();

    orbit.update();

    renderer.render(
        scene,
        camera
    );
}

animate();


// ==========================================
// 23. WINDOW RESIZE
// ==========================================

window.addEventListener(
    "resize",
    () => {

        camera.aspect = (
            window.innerWidth / window.innerHeight
        );

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );

        Streamlit.setFrameHeight(
            COMPONENT_HEIGHT
        );
    }
);