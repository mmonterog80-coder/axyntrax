import QtQuick
import QtQuick.Controls
import QtQuick.Particles

ApplicationWindow {
    id: window
    visible: true
    width: 1280
    height: 720
    title: "JARVIS AX - AXYNTRAX Automation Suite"
    color: "#050510"
    visibility: "FullScreen"  // Cambiar a "Windowed" si se quiere ventana

    // Partículas de fondo
    ParticleSystem {
        id: particleSys
        anchors.fill: parent
        ImageParticle {
            source: "qrc:///particle.png"  // Si no existe, usar un color sólido
            color: "#0055aa"
            alpha: 0.3
        }
        Emitter {
            width: parent.width
            height: 10
            emitRate: 10
            lifeSpan: 8000
            velocity: PointDirection { y: 20; xVariation: 10 }
            size: 8
        }
    }

    // Anillos giratorios centrales
    Canvas {
        id: ringCanvas
        anchors.centerIn: parent
        width: 400
        height: 400
        rotation: 45
        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            ctx.strokeStyle = "#00b4d8";
            ctx.lineWidth = 2;
            ctx.shadowBlur = 20;
            ctx.shadowColor = "#00b4d8";
            ctx.beginPath();
            ctx.arc(200, 200, 150, 0, Math.PI * 2);
            ctx.stroke();
            ctx.strokeStyle = "#ff6b00";
            ctx.shadowColor = "#ff6b00";
            ctx.beginPath();
            ctx.arc(200, 200, 110, 0, Math.PI * 2);
            ctx.stroke();
        }
        RotationAnimation on rotation {
            from: 0; to: 360; duration: 12000; loops: Animation.Infinite
        }
    }

    // Panel superior (HUD)
    Rectangle {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 20
        width: 300
        height: 120
        color: "#10ffffff"
        border.color: "#00b4d8"
        border.width: 1
        radius: 8

        Column {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 8
            Text { text: "CPU: " + backend.cpuChanged.toFixed(1) + "%"; color: "#e0e0ff"; font.pixelSize: 16 }
            Text { text: "RAM: " + backend.ramChanged.toFixed(1) + "%"; color: "#e0e0ff"; font.pixelSize: 16 }
            Text { text: Qt.formatDateTime(new Date(), "hh:mm:ss"); color: "#e0e0ff"; font.pixelSize: 16 }
        }
    }

    // Consola de mensajes
    ListView {
        id: consoleList
        anchors.bottom: input.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        height: 200
        model: ListModel {}
        clip: true
        delegate: Text {
            text: model.text
            color: "#c0d0ff"
            font.pixelSize: 14
            anchors.left: parent.left
            anchors.right: parent.right
            wrapMode: Text.Wrap
        }
    }

    // Entrada de comandos
    TextField {
        id: input
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        height: 40
        placeholderText: "Escribe tu orden, señor..."
        color: "#ffffff"
        font.pixelSize: 18
        background: Rectangle {
            color: "#101020"
            border.color: "#00b4d8"
            border.width: 1
            radius: 4
        }
        Keys.onReturnPressed: {
            backend.sendCommand(text)
            text = ""
        }
    }

    // Conexiones con backend
    Connections {
        target: backend
        onConsoleOutput: {
            consoleList.model.append({"text": output})
            consoleList.positionViewAtEnd()
        }
    }
}
