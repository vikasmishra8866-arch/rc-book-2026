<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RC Modification System - Gujarat Style</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .rc-canvas-container {
            position: relative;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border-radius: 8px;
            overflow: hidden;
            background: #fff;
        }
        canvas {
            max-width: 100%;
            height: auto;
        }
        .loading-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.7);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            z-index: 100;
        }
    </style>
</head>
<body class="bg-slate-900 text-gray-100 min-h-screen font-sans">

    <div id="loader" class="loading-overlay">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
        <p class="mt-4 text-lg">AI Processing Ho Raha Hai...</p>
    </div>

    <div class="max-w-6xl mx-auto p-4 md:p-8">
        <header class="mb-8 border-b border-gray-700 pb-4">
            <h1 class="text-3xl font-bold text-white flex items-center gap-3">
                📄 RC Modification System
            </h1>
            <p class="text-gray-400 mt-2">Apni purani RC upload karein aur naye details enter karke output download karein.</p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Side: Inputs -->
            <div class="space-y-6 bg-slate-800 p-6 rounded-xl border border-gray-700">
                
                <section>
                    <h2 class="text-xl font-semibold mb-4 text-blue-400">1. Upload Old RC</h2>
                    <div class="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-blue-500 transition cursor-pointer" onclick="document.getElementById('fileInput').click()">
                        <input type="file" id="fileInput" accept="image/*" class="hidden" onchange="handleImageUpload(event)">
                        <div id="uploadPlaceholder">
                            <p class="text-gray-400">Yahan click karein ya image drop karein</p>
                            <p class="text-xs text-gray-500 mt-1">(Support: JPG, PNG)</p>
                        </div>
                        <img id="imagePreview" class="hidden mx-auto max-h-32 rounded">
                    </div>
                </section>

                <section class="space-y-4">
                    <h2 class="text-xl font-semibold text-blue-400">2. Enter New Details</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Registration Number</label>
                            <input type="text" id="regNo" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="e.g. GJ05CX1234">
                        </div>
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Owner Name</label>
                            <input type="text" id="ownerName" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="Full Name">
                        </div>
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Chassis Number</label>
                            <input type="text" id="chassis" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="Chassis No.">
                        </div>
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Engine Number</label>
                            <input type="text" id="engine" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="Engine No.">
                        </div>
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Regn. Validity</label>
                            <input type="text" id="validity" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="DD-MMM-YYYY">
                        </div>
                        <div>
                            <label class="block text-xs text-gray-400 mb-1">Address</label>
                            <input type="text" id="address" class="w-full bg-slate-700 border border-gray-600 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500" placeholder="Full Address">
                        </div>
                    </div>
                    
                    <div class="pt-4 border-t border-gray-700 flex gap-4">
                        <button onclick="extractData()" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg transition">
                            AI Scan (Purani Data)
                        </button>
                        <button onclick="drawRC()" class="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg transition">
                            Update RC Preview
                        </button>
                    </div>
                </section>
            </div>

            <!-- Right Side: Live Output -->
            <div class="flex flex-col items-center">
                <h2 class="text-xl font-semibold mb-4 text-blue-400 self-start">3. Live Output</h2>
                <div id="canvasWrapper" class="rc-canvas-container">
                    <canvas id="rcCanvas"></canvas>
                </div>
                
                <div class="mt-6 flex gap-4">
                    <button onclick="downloadRC()" class="bg-gray-200 hover:bg-white text-black font-bold px-8 py-3 rounded-full flex items-center gap-2 transition">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                        Download Final RC
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const apiKey = ""; // API key managed by environment
        const canvas = document.getElementById('rcCanvas');
        const ctx = canvas.getContext('2d');
        let baseImage = null;

        // Photo load karne ka function
        function handleImageUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                baseImage = new Image();
                baseImage.onload = function() {
                    // Set canvas size to match uploaded image
                    canvas.width = baseImage.width;
                    canvas.height = baseImage.height;
                    drawRC();
                    
                    document.getElementById('imagePreview').src = e.target.result;
                    document.getElementById('imagePreview').classList.remove('hidden');
                    document.getElementById('uploadPlaceholder').classList.add('hidden');
                };
                baseImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        // AI se data nikalne ka function
        async function extractData() {
            if (!baseImage) {
                alert("Pehle purani RC upload karein!");
                return;
            }

            const loader = document.getElementById('loader');
            loader.style.display = 'flex';

            const base64Data = canvas.toDataURL('image/jpeg').split(',')[1];
            const prompt = "Is RC image se saari details nikaalo: Registration Number, Owner Name, Chassis Number, Engine Number, Validity, Address. Return JSON only.";

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: [{
                            parts: [
                                { text: prompt },
                                { inlineData: { mimeType: "image/jpeg", data: base64Data } }
                            ]
                        }],
                        generationConfig: { responseMimeType: "application/json" }
                    })
                });

                const result = await response.json();
                const data = JSON.parse(result.candidates[0].content.parts[0].text);

                // Fill inputs
                document.getElementById('regNo').value = data.regNo || data.registration_number || "";
                document.getElementById('ownerName').value = data.ownerName || data.owner_name || "";
                document.getElementById('chassis').value = data.chassis || data.chassis_number || "";
                document.getElementById('engine').value = data.engine || data.engine_number || "";
                document.getElementById('validity').value = data.validity || "";
                document.getElementById('address').value = data.address || "";

                drawRC();
            } catch (err) {
                console.error(err);
                alert("AI processing mein error aya. Manual fill kar sakte hain.");
            } finally {
                loader.style.display = 'none';
            }
        }

        // Canvas par text chhapne ka function (Gujarat RC Positions)
        function drawRC() {
            if (!baseImage) return;

            // Clear and Draw Original
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(baseImage, 0, 0);

            // Text Settings
            const scaleFactor = canvas.width / 1000; // Relative font size
            ctx.font = `bold ${16 * scaleFactor}px monospace`;
            ctx.fillStyle = "black";

            // Positions (Approximate as per Gujarat RC layout)
            const inputs = {
                regNo: { val: document.getElementById('regNo').value, x: 160, y: 250 },
                validity: { val: document.getElementById('validity').value, x: 380, y: 250 },
                chassis: { val: document.getElementById('chassis').value, x: 160, y: 310 },
                engine: { val: document.getElementById('engine').value, x: 160, y: 360 },
                ownerName: { val: document.getElementById('ownerName').value, x: 160, y: 410 },
                address: { val: document.getElementById('address').value, x: 160, y: 460 }
            };

            // Overlay with White Background first to "Hide" old text (optional)
            // ctx.fillStyle = "white";
            // ctx.fillRect(150 * scaleFactor, 230 * scaleFactor, 200 * scaleFactor, 30 * scaleFactor);

            ctx.fillStyle = "black";
            ctx.fillText(inputs.regNo.val, inputs.regNo.x * scaleFactor, inputs.regNo.y * scaleFactor);
            ctx.fillText(inputs.validity.val, inputs.validity.x * scaleFactor, inputs.validity.y * scaleFactor);
            ctx.fillText(inputs.chassis.val, inputs.chassis.x * scaleFactor, inputs.chassis.y * scaleFactor);
            ctx.fillText(inputs.engine.val, inputs.engine.x * scaleFactor, inputs.engine.y * scaleFactor);
            
            ctx.font = `bold ${14 * scaleFactor}px monospace`;
            ctx.fillText(inputs.ownerName.val.toUpperCase(), inputs.ownerName.x * scaleFactor, inputs.ownerName.y * scaleFactor);
            
            // Multi-line address logic
            ctx.font = `${12 * scaleFactor}px monospace`;
            const addr = inputs.address.val;
            if(addr.length > 40) {
                ctx.fillText(addr.substring(0, 40), inputs.address.x * scaleFactor, inputs.address.y * scaleFactor);
                ctx.fillText(addr.substring(40), inputs.address.x * scaleFactor, (inputs.address.y + 15) * scaleFactor);
            } else {
                ctx.fillText(addr, inputs.address.x * scaleFactor, inputs.address.y * scaleFactor);
            }
        }

        function downloadRC() {
            const link = document.createElement('a');
            link.download = 'Modified_RC_Gujarat.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }
    </script>
</body>
</html>
