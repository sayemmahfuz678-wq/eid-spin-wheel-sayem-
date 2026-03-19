from flask import Flask, render_template_string
import json

app = Flask(__name__)

WHEEL_ITEMS = [
    "10 tk salami",
    "20 tk salami",
    "30 tk salami",
    "NO salami but blessings from sayem"
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>EID MUBARAK from SAYEM</title>

    <meta property="og:title" content="EID MUBARAK from SAYEM" />
    <meta property="og:description" content="Spin the Eid salami wheel and try your luck!" />
    <meta property="og:type" content="website" />

    <style>
        :root {
            --bg1: #0b3b2f;
            --bg2: #165b44;
            --gold: #fad882;
            --gold-dark: #e5b13b;
            --cream: #fef9e9;
            --white: #ffffff;
            --card: rgba(255, 255, 255, 0.1);
            --moon-light: #fff1b8;
            --moon-dark: #f7d570;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            color: var(--white);
            background:
                radial-gradient(circle at 20% 30%, rgba(255, 215, 130, 0.15), transparent 40%),
                linear-gradient(145deg, var(--bg1), var(--bg2));
            overflow-x: hidden;
        }

        .stars::before,
        .stars::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                radial-gradient(circle, rgba(255, 255, 200, 0.8) 1px, transparent 1.5px),
                radial-gradient(circle, rgba(250, 216, 130, 0.5) 1px, transparent 2px);
            background-size: 100px 100px, 150px 150px;
            background-position: 0 0, 30px 30px;
            opacity: 0.3;
            animation: twinkle 8s infinite alternate;
        }

        @keyframes twinkle {
            0% { opacity: 0.2; }
            100% { opacity: 0.4; }
        }

        .page {
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px 16px 60px;
            position: relative;
            z-index: 1;
            text-align: center;
        }

        .lanterns {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }

        .lantern {
            width: 34px;
            height: 54px;
            border-radius: 10px 10px 6px 6px;
            background: linear-gradient(180deg, #fcd77e, #dba837);
            position: relative;
            box-shadow: 0 0 20px #fad882;
            animation: swing 2.8s ease-in-out infinite;
            transform-origin: top center;
        }

        .lantern::before {
            content: "";
            position: absolute;
            top: -18px;
            left: 15px;
            width: 4px;
            height: 18px;
            background: #dba837;
        }

        .lantern::after {
            content: "";
            position: absolute;
            bottom: -10px;
            left: 13px;
            width: 8px;
            height: 12px;
            background: #dba837;
            border-radius: 0 0 5px 5px;
        }

        .lantern:nth-child(2) { animation-delay: 0.5s; }
        .lantern:nth-child(3) { animation-delay: 1s; }

        @keyframes swing {
            0%, 100% { transform: rotate(3deg); }
            50% { transform: rotate(-3deg); }
        }

        .moon {
            width: 110px;
            height: 110px;
            margin: 10px auto 16px;
            border-radius: 50%;
            background: linear-gradient(145deg, var(--moon-light), var(--moon-dark));
            position: relative;
            box-shadow: 0 0 40px #fce39c;
        }

        .moon::after {
            content: "";
            position: absolute;
            top: 12px;
            left: 30px;
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--bg1), var(--bg2));
        }

        h1 {
            margin: 8px 0 0;
            color: var(--gold);
            font-size: clamp(2.4rem, 6vw, 4.2rem);
            letter-spacing: 2px;
            text-shadow: 0 0 6px #ffd966;
        }

        .subtitle {
            color: var(--cream);
            font-size: clamp(1rem, 2.2vw, 1.3rem);
            margin-bottom: 28px;
            font-style: italic;
        }

        .intro-box,
        .wheel-card {
            background: var(--card);
            border: 1px solid rgba(250, 216, 130, 0.3);
            border-radius: 32px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
        }

        .intro-box {
            max-width: 850px;
            margin: 0 auto 30px;
            padding: 22px 24px;
        }

        .badge {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 18px;
            border-radius: 50px;
            color: var(--gold);
            border: 1px solid rgba(250, 216, 130, 0.4);
            background: rgba(250, 216, 130, 0.15);
            font-weight: bold;
            font-size: 1.1rem;
        }

        .wheel-card {
            width: min(95vw, 600px);
            margin: 0 auto;
            padding: 24px 16px 30px;
        }

        .wheel-title {
            font-size: 1.7rem;
            color: var(--gold);
            margin-bottom: 20px;
            font-weight: 600;
        }

        .wheel-wrapper {
            position: relative;
            width: min(88vw, 440px);
            height: min(88vw, 440px);
            margin: 0 auto 25px;
        }

        .pointer {
            position: absolute;
            top: -2px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 24px solid transparent;
            border-right: 24px solid transparent;
            border-top: 46px solid #cf4e4e;
            z-index: 10;
            filter: drop-shadow(0 6px 8px rgba(0,0,0,0.4));
        }

        canvas {
            width: 100%;
            height: 100%;
            display: block;
            border-radius: 50%;
            box-shadow: 0 0 0 6px #ffe9b6, 0 20px 30px rgba(0,0,0,0.3);
        }

        .center-cap {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 90px;
            height: 90px;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #ffefc0, #e6b422);
            border: 6px solid #fff2cc;
            box-shadow: 0 0 30px #fad882;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #422d00;
            font-weight: bold;
            font-size: 1rem;
            text-align: center;
            z-index: 15;
            line-height: 1.3;
        }

        button {
            border: none;
            border-radius: 60px;
            padding: 16px 38px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            background: linear-gradient(180deg, #ffde8a, #e5ac2c);
            color: #2a1f03;
            box-shadow: 0 10px 24px rgba(0,0,0,0.25);
            transition: transform 0.2s, box-shadow 0.2s;
            letter-spacing: 1px;
        }

        button:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        }

        button:disabled {
            opacity: 0.5;
            transform: none;
            box-shadow: none;
            cursor: not-allowed;
        }

        .result {
            min-height: 100px;
            margin-top: 24px;
            padding: 18px;
            border-radius: 24px;
            background: rgba(0, 0, 0, 0.2);
            color: var(--cream);
            font-size: 1.15rem;
            line-height: 1.6;
            border: 1px solid rgba(250, 216, 130, 0.2);
        }

        .highlight {
            color: var(--gold);
            font-weight: 600;
        }

        .prize-list {
            margin-top: 24px;
            text-align: left;
            background: rgba(0, 0, 0, 0.15);
            border-radius: 24px;
            padding: 18px 22px;
            border: 1px solid rgba(250, 216, 130, 0.15);
        }

        .prize-list h3 {
            margin-top: 0;
            color: var(--gold);
            font-size: 1.4rem;
        }

        .prize-list ul {
            margin-bottom: 0;
            padding-left: 22px;
            font-size: 1.1rem;
        }

        .footer-note {
            margin-top: 20px;
            font-size: 0.95rem;
            color: #f5efdf;
        }
    </style>
</head>
<body>
    <div class="stars"></div>

    <div class="page">
        <div class="lanterns">
            <div class="lantern"></div>
            <div class="lantern"></div>
            <div class="lantern"></div>
        </div>

        <div class="moon"></div>

        <h1>EID MUBARAK from SAYEM</h1>
        <div class="subtitle">
            ✨ Spin & receive barakah – one try per person ✨
        </div>

        <div class="intro-box">
            <p style="font-size: 1.2rem;">
                🌙 Wishing you and your family a blessed Eid filled with peace, happiness,
                and endless barakah. Give the wheel a spin and see what Eid has written for you.
            </p>
            <div class="badge">🎁 One spin only (saved in your browser)</div>
        </div>

        <div class="wheel-card">
            <div class="wheel-title">🎡 Eid Salami Wheel</div>

            <div class="wheel-wrapper">
                <div class="pointer"></div>
                <canvas id="wheelCanvas" width="500" height="500"></canvas>
                <div class="center-cap">EID<br>SPIN</div>
            </div>

            <button id="spinBtn">Spin Now</button>

            <div class="result" id="resultBox">
                Press <span class="highlight">Spin Now</span> and try your Eid luck 🌙
            </div>

            <div class="prize-list">
                <h3>🎁 Prizes</h3>
                <ul>
                    <li>10 tk salami</li>
                    <li>20 tk salami</li>
                    <li>30 tk salami</li>
                    <li>NO salami but blessings from sayem</li>
                </ul>
            </div>

            <div class="footer-note">
                * One spin per browser – results are saved locally.
            </div>
        </div>
    </div>

    <script>
        (function() {
            const items = {{ items|safe }};
            const spinBtn = document.getElementById("spinBtn");
            const resultBox = document.getElementById("resultBox");
            const canvas = document.getElementById("wheelCanvas");
            const ctx = canvas.getContext("2d");

            const total = items.length;
            const arcSize = (2 * Math.PI) / total;
            const radius = 220;
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;

            let currentRotation = 0;
            let spinning = false;

            // Aesthetic Eid color palette
            const colors = ["#FFB347", "#66BB77", "#FF8A80", "#BA7FD0"];  // orange, green, coral, lavender

            // Helper: draw wrapped text centered at (x, y)
            function drawWrappedText(context, text, x, y, maxWidth, lineHeight) {
                const words = text.split(' ');
                let lines = [];
                let currentLine = words[0];

                for (let i = 1; i < words.length; i++) {
                    const testLine = currentLine + ' ' + words[i];
                    const metrics = context.measureText(testLine);
                    if (metrics.width > maxWidth) {
                        lines.push(currentLine);
                        currentLine = words[i];
                    } else {
                        currentLine = testLine;
                    }
                }
                lines.push(currentLine);

                // Calculate vertical start position to center the block
                const totalHeight = lines.length * lineHeight;
                let startY = y - totalHeight / 2 + lineHeight / 2;

                for (let i = 0; i < lines.length; i++) {
                    context.fillText(lines[i], x, startY + i * lineHeight);
                }
            }

            function drawWheel(rotation = 0) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < total; i++) {
                    const startAngle = rotation + i * arcSize - Math.PI / 2;
                    const endAngle = startAngle + arcSize;

                    // Draw segment
                    ctx.beginPath();
                    ctx.moveTo(cx, cy);
                    ctx.arc(cx, cy, radius, startAngle, endAngle);
                    ctx.closePath();
                    ctx.fillStyle = colors[i % colors.length];
                    ctx.fill();

                    // Draw text in the middle of the segment, facing outward
                    ctx.save();
                    ctx.translate(cx, cy);
                    const midAngle = startAngle + arcSize / 2;
                    ctx.rotate(midAngle);
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "bold 18px 'Segoe UI', Arial, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    // Position text at 70% of the radius
                    const textRadius = radius * 0.7;
                    drawWrappedText(ctx, items[i], textRadius, 0, 140, 24);
                    ctx.restore();
                }

                // Draw inner circle accent
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.lineWidth = 12;
                ctx.strokeStyle = "#FFF4D6";
                ctx.stroke();

                // Small decorative dots
                for (let i = 0; i < total; i++) {
                    const angle = rotation + i * arcSize - Math.PI / 2 + arcSize / 2;
                    const dotX = cx + Math.cos(angle) * 30;
                    const dotY = cy + Math.sin(angle) * 30;
                    ctx.beginPath();
                    ctx.arc(dotX, dotY, 8, 0, 2 * Math.PI);
                    ctx.fillStyle = "#FFF9E6";
                    ctx.shadowColor = '#FFE5A3';
                    ctx.shadowBlur = 10;
                    ctx.fill();
                    ctx.shadowColor = 'transparent';
                }
            }

            // Check if already spun
            function getStoredResult() {
                return localStorage.getItem("eid_spin_result");
            }

            function setStoredResult(result) {
                localStorage.setItem("eid_spin_result", result);
            }

            function showAlreadySpun(result) {
                resultBox.innerHTML = `
                    🕌 You already used your Eid spin.<br><br>
                    <span class="highlight">Your result:</span> ${result}
                `;
                spinBtn.disabled = true;
                spinBtn.textContent = "Already Spun";
            }

            function showResult(result) {
                if (result.includes("tk salami")) {
                    resultBox.innerHTML = `
                        🎉 <span class="highlight">Mubarak!</span><br>
                        You got: <span class="highlight">${result}</span><br>
                        Eid Mubarak from Sayem 💛
                    `;
                } else {
                    resultBox.innerHTML = `
                        🌙 <span class="highlight">Blessings for you!</span><br>
                        ${result}<br>
                        Eid Mubarak from Sayem 🤍
                    `;
                }
            }

            function spinWheel() {
                if (spinning) return;

                const previous = getStoredResult();
                if (previous) {
                    showAlreadySpun(previous);
                    return;
                }

                spinning = true;
                spinBtn.disabled = true;
                resultBox.innerHTML = "The wheel is spinning... ✨ بسم الله";

                // Pick random winning index
                const winningIndex = Math.floor(Math.random() * total);
                const selectedItem = items[winningIndex];

                // 60 RPM = 1 revolution per second. Spin for 5 seconds => 5 full spins.
                const fullSpins = 5;   // 5 rotations
                // Target rotation so that pointer (at -PI/2) aligns with center of winning segment
                // center of segment = -PI/2 + i*arcSize + arcSize/2
                // required rotation R = - (i*arcSize + arcSize/2)  (mod 2PI)
                // we add fullSpins * 2PI to get many spins
                const targetAngle = (2 * Math.PI * fullSpins) - (winningIndex * arcSize + arcSize / 2);

                const startRotation = currentRotation % (2 * Math.PI);
                const duration = 5000; // 5 seconds
                const startTime = performance.now();

                function animate(now) {
                    const elapsed = now - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    // Smooth ease-out for a natural stop
                    const easeOut = 1 - Math.pow(1 - progress, 3);

                    currentRotation = startRotation + (targetAngle * easeOut);
                    drawWheel(currentRotation);

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    } else {
                        spinning = false;
                        setStoredResult(selectedItem);
                        showResult(selectedItem);
                        spinBtn.textContent = "Spin Used";
                        spinBtn.disabled = true;  // already disabled, but for safety
                    }
                }

                requestAnimationFrame(animate);
            }

            // Initial draw
            drawWheel();

            // Check if user already spun
            const savedResult = getStoredResult();
            if (savedResult) {
                showAlreadySpun(savedResult);
            }

            spinBtn.addEventListener("click", spinWheel);
        })();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, items=json.dumps(WHEEL_ITEMS))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)