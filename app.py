<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart RC Editor & Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .rc-card {
            width: 500px;
            height: 300px;
            background: linear-gradient(135deg, #ffffff 0%, #e5e7eb 100%);
            border: 2px solid #3b82f6;
            border-radius: 15px;
            position: relative;
            padding: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .watermark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 60px;
            color: rgba(59, 130, 246, 0.05);
            pointer-events: none;
            font-weight: bold;
            white-space: nowrap;
        }
        #preview-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
        }
        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="p-4 md:p-8">

    <div class="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col md:flex-row">
        
        <!-- Left Side: Controls -->
        <div class="w-full md:w-1/3 p-6 border-r border-gray-200">
            <h1 class="text-2xl font-bold text-blue-600 mb-2">RC Smart Editor</h1>
            <p class="text-sm text-gray-500 mb-6">Purani RC upload karein aur details update karein.</p>

            <!-- Step 1: Upload -->
            <div class="mb-6">
                <label class="block text-sm font-semibold mb-2">1. Purani RC Upload Karein</label>
                <input type="file" id="imageInput" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
                <button onclick="analyzeImage()" id="analyzeBtn" class="mt-3 w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition flex items-center justify-center gap-2">
                    <span>Data Extract Karein</span>
                    <div id="loader" class="loading-spinner hidden"></div>
                </button>
            </div>

            <hr class="my-6">

            <!-- Step 2: Edit Details -->
            <div class="space-y-4">
                <label class="block text-sm font-semibold">2. Details Check/Update Karein</label>
                <div>
                    <label class="text-xs text-gray-400">Owner Name</label>
                    <input type="text" id="ownerName" placeholder="Owner Name" class="w-full p-2 border rounded text-sm focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
                <div>
                    <label class="text-xs text-gray-400">Registration Number</label>
                    <input type="text" id="regNo" placeholder="Reg. No (e.g. DL 01 AB 1234)" class="w-full p-2 border rounded text-sm focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
                <div>
                    <label class="text-xs text-gray-400">Vehicle Model</label>
                    <input type="text" id="model" placeholder="Vehicle Model" class="w-full p-2 border rounded text-sm focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
                <div>
                    <label class="text-xs text-gray-400">Chassis Number</label>
                    <input type="text" id="chassis" placeholder="Chassis Number" class="w-full p-2 border rounded text-sm focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
                <button onclick="updatePreview()" class="w-full bg-green-600 text-white py-2 rounded-lg font-medium hover:bg-green-700 transition">
                    New RC Generate Karein
                </button>
            </div>
        </div>

        <!-- Right Side: Preview -->
        <div class="w-full md:w-2/3 bg-gray-50 p-6 flex flex-col items-center justify-center">
            <h2 class="text-lg font-semibold text-gray-700 mb-4">Live Preview (New RC)</h2>
            
            <div id="preview-container">
                <div id="rcCard" class="rc-card">
                    <div class="watermark">TRANSPORT DEPT</div>
                    
                    <!-- Header -->
                    <div class="flex justify-between items-start border-bottom border-gray-300 pb-2 mb-4">
                        <div>
                            <p class="text-[10px] font-bold text-blue-800">GOVERNMENT OF INDIA</p>
                            <p class="text-[8px] text-gray-600">CERTIFICATE OF REGISTRATION</p>
                        </div>
                        <div class="text-right">
                            <p id="display-regNo" class="text-sm font-bold text-red-600">MH 12 AB 0000</p>
                        </div>
                    </div>

                    <!-- Body -->
                    <div class="grid grid-cols-2 gap-y-3 text-[11px]">
                        <div>
                            <p class="text-gray-400 font-medium">Owner Name</p>
                            <p id="display-ownerName" class="font-bold text-gray-800">-----</p>
                        </div>
                        <div>
                            <p class="text-gray-400 font-medium">Vehicle Class</p>
                            <p class="font-bold text-gray-800">LMV - MOTOR CAR</p>
                        </div>
                        <div>
                            <p class="text-gray-400 font-medium">Maker Model</p>
                            <p id="display-model" class="font-bold text-gray-800">-----</p>
                        </div>
                        <div>
                            <p class="text-gray-400 font-medium">Chassis No.</p>
                            <p id="display-chassis" class="font-bold text-gray-800">-----</p>
                        </div>
                        <div>
                            <p class="text-gray-400 font-medium">Fuel Type</p>
                            <p class="font-bold text-gray-800">PETROL</p>
                        </div>
                        <div>
                            <p class="text-gray-400 font-medium">Validity</p>
                            <p class="font-bold text-green-700">15 YEARS</p>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="absolute bottom-4 left-4 right-4 flex justify-between items-end">
                        <div class="bg-gray-200 w-16 h-16 rounded border flex items-center justify-center text-[8px] text-gray-400">
                            PHOTO
                        </div>
                        <div class="text-[8px] text-right text-gray-500">
                            Digitally Signed by RTO Authority<br>
                            Generated on: <span id="currentDate"></span>
                        </div>
                    </div>
                </div>
            </div>

            <button onclick="downloadRC()" class="mt-6 flex items-center gap-2 bg-gray-800 text-white px-6 py-2 rounded-full hover:bg-black transition">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                    <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                </svg>
                Save as Image
            </button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        const apiKey = ""; // Runtime provides key

        async function analyzeImage() {
            const fileInput = document.getElementById('imageInput');
            if (!fileInput.files[0]) {
                alert("Pehle RC ki photo upload karein!");
                return;
            }

            const loader = document.getElementById('loader');
            const btn = document.getElementById('analyzeBtn');
            loader.classList.remove('hidden');
            btn.disabled = true;

            const reader = new FileReader();
            reader.onloadend = async () => {
                const base64Data = reader.result.split(',')[1];
                
                const prompt = "Extract Registration Number, Owner Name, Vehicle Model, and Chassis Number from this Registration Certificate image. Return only as JSON with keys: regNo, ownerName, model, chassis.";
                
                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{
                                parts: [
                                    { text: prompt },
                                    { inlineData: { mimeType: "image/png", data: base64Data } }
                                ]
                            }],
                            generationConfig: { responseMimeType: "application/json" }
                        })
                    });

                    const result = await response.json();
                    const data = JSON.parse(result.candidates[0].content.parts[0].text);

                    // Fill Inputs
                    document.getElementById('ownerName').value = data.ownerName || "";
                    document.getElementById('regNo').value = data.regNo || "";
                    document.getElementById('model').value = data.model || "";
                    document.getElementById('chassis').value = data.chassis || "";

                    updatePreview();
                } catch (error) {
                    console.error(error);
                    alert("AI data read nahi kar paya. Aap manually fill kar sakte hain.");
                } finally {
                    loader.classList.add('hidden');
                    btn.disabled = false;
                }
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        function updatePreview() {
            document.getElementById('display-ownerName').innerText = document.getElementById('ownerName').value || "-----";
            document.getElementById('display-regNo').innerText = document.getElementById('regNo').value || "MH 12 AB 0000";
            document.getElementById('display-model').innerText = document.getElementById('model').value || "-----";
            document.getElementById('display-chassis').innerText = document.getElementById('chassis').value || "-----";
            
            const date = new Date();
            document.getElementById('currentDate').innerText = date.toLocaleDateString();
        }

        function downloadRC() {
            const element = document.getElementById('rcCard');
            html2canvas(element, { scale: 3 }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'New_RC_Card.png';
                link.href = canvas.toDataURL();
                link.click();
            });
        }

        // Init date
        document.getElementById('currentDate').innerText = new Date().toLocaleDateString();
    </script>
</body>
</html>
