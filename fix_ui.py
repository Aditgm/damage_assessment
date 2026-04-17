import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '</head>'
end_marker = '    <script>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_html = r'''</head>
<body class="bg-background text-white font-body min-h-screen flex flex-col items-center pb-12 selection:bg-primary selection:text-black">

    <!-- Top Navigation -->
    <header class="w-full px-8 py-4 flex items-center justify-between border-b border-white/5 bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-primary text-3xl">public</span>
            <h1 class="font-headline text-lg font-bold tracking-[0.2em] text-white uppercase">
                Damage<span class="text-primary font-normal">Assessment</span>
            </h1>
        </div>
        
        <div class="flex items-center gap-6">
            <!-- Mode Toggle (Single / Compare) -->
            <div class="flex bg-white/5 rounded-full p-1 border border-white/10 relative">
                <div id="modeTogglePill" class="absolute left-1 top-1 bottom-1 w-[calc(50%-4px)] bg-primary rounded-full transition-all duration-300 pointer-events-none"></div>
                <button id="btnSingleMode" class="relative z-10 px-4 py-1.5 text-xs font-headline font-bold uppercase tracking-wider text-black rounded-full transition-colors w-28 text-center mix-blend-difference focus:outline-none" onclick="setMode('single')">
                    Single
                </button>
                <button id="btnCompareMode" class="relative z-10 px-4 py-1.5 text-xs font-headline font-bold uppercase tracking-wider text-white/70 hover:text-white rounded-full transition-colors w-28 text-center mix-blend-difference focus:outline-none" onclick="setMode('compare')">
                    Before/After
                </button>
            </div>
            
            <div class="text-xs font-mono text-primary/70 uppercase lg:flex items-center gap-2 hidden">
                <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                Roboflow Engine Linked
            </div>
        </div>
    </header>

    <!-- GSAP Hero Section -->
    <section class="relative w-full h-[60vh] carousel-view bg-black">
        <div class="carousel-ring" id="carouselRing"></div>
        <div class="absolute inset-0 z-10 flex flex-col items-center justify-center pointer-events-none px-4" style="background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.75) 100%);">
            <div class="relative flex flex-col items-center">
                <h2 class="glitch font-elegant text-4xl md:text-7xl font-black uppercase text-center leading-tight tracking-[0.15em] text-white/90 z-10 drop-shadow-[0_0_40px_rgba(255,183,3,0.25)]" data-text="DAMAGE">DAMAGE</h2>
                <h2 class="glitch font-elegant text-4xl md:text-7xl font-black uppercase text-center leading-tight tracking-[0.15em] text-primary z-10 drop-shadow-[0_0_30px_rgba(255,183,3,0.5)] mt-1" data-text="ASSESSMENT">ASSESSMENT</h2>
                <div class="absolute inset-0 font-elegant text-4xl md:text-7xl font-black uppercase text-center leading-tight tracking-[0.15em] text-primary opacity-30 blur-[25px] z-0 flex flex-col items-center justify-center" aria-hidden="true">
                    <span>DAMAGE</span>
                    <span>ASSESSMENT</span>
                </div>
            </div>
            <div class="mt-6 flex items-center justify-center gap-3 opacity-80">
                <div class="h-[1px] w-10 md:w-20 bg-gradient-to-r from-transparent to-primary"></div>
                <h3 class="font-elegant text-xs md:text-sm tracking-[0.5em] text-primary/80 uppercase">MODEL</h3>
                <div class="h-[1px] w-10 md:w-20 bg-gradient-to-l from-transparent to-primary"></div>
            </div>
            <p class="mt-4 text-white/30 text-xs md:text-sm font-body tracking-widest uppercase">AI-Powered Disaster Intelligence</p>
        </div>
        <div class="absolute bottom-0 w-full h-32 bg-gradient-to-t from-background to-transparent z-20"></div>
    </section>

    <!-- Main Content -->
    <main class="w-full max-w-6xl flex flex-col lg:flex-row gap-8 px-4 mt-8 relative z-30">
        
        <!-- Left Panel: Scanning Interface -->
        <div class="glass-panel p-6 md:p-8 rounded-3xl flex-1 flex flex-col relative overflow-hidden transition-all duration-500 shadow-2xl">
            <div class="flex justify-between items-end mb-6">
                <div>
                    <h2 class="font-headline text-2xl font-bold uppercase tracking-widest text-white">Input Telemetry</h2>
                    <p class="text-white/50 text-sm mt-1">Upload disaster imagery for AI segmentation analysis.</p>
                </div>
                <span class="material-symbols-outlined text-primary/50 text-4xl">cloud_upload</span>
            </div>
            
            <label id="dropZone" class="upload-area flex-1 flex flex-col items-center justify-center min-h-[300px] w-full aspect-video md:aspect-[16/9] rounded-2xl relative overflow-hidden border-2 border-dashed border-white/10 hover:border-primary/50 transition-colors duration-500 group cursor-pointer bg-black/40">
                
                <!-- SINGLE MODE VIEW -->
                <div id="singleModeView" class="w-full h-full flex flex-col items-center justify-center">
                    <div id="previewContainer" class="absolute inset-0 hidden bg-surface">
                        <div class="scanner-container w-full h-full">
                            <img id="imagePreview" src="" alt="Target" class="w-full h-full object-cover opacity-60" />
                            <div class="scan-grid"></div>
                            <div class="scan-line"></div>
                        </div>
                    </div>

                    <div id="uploadPrompt" class="text-center space-y-4 z-10 group-hover:scale-105 transition-transform duration-500">
                        <div class="w-20 h-20 mx-auto rounded-full bg-primary/10 flex items-center justify-center shadow-[0_0_30px_rgba(255,183,3,0.1)] mb-4 border border-primary/20">
                            <span class="material-symbols-outlined text-primary text-5xl group-hover:-translate-y-1 transition-transform duration-300">add_photo_alternate</span>
                        </div>
                        <p class="font-headline font-bold text-lg text-primary tracking-widest uppercase glow-primary">Initialize Scan</p>
                        <p class="font-mono text-xs text-white/40 tracking-widest uppercase">Drag & Drop or Click to Browse</p>
                    </div>
                </div>

                <!-- COMPARISON MODE VIEW -->
                <div id="compareModeView" class="w-full h-full hidden compare-grid p-4 md:p-6 gap-4 md:gap-6 bg-transparent pointer-events-auto">
                    <!-- Before Slot -->
                    <div id="slotBefore" class="image-slot group/slot w-full h-full flex flex-col items-center justify-center relative border border-white/10 bg-black/40 hover:bg-black/60 rounded-xl transition-colors cursor-pointer" onclick="event.stopPropagation(); event.preventDefault(); document.getElementById('fileInputBefore').click();">
                        <img id="previewBefore" src="" class="absolute inset-0 w-full h-full object-cover hidden opacity-60 rounded-xl">
                        <div class="z-10 text-center pointer-events-none p-4 w-full h-full flex flex-col items-center justify-center">
                            <span class="material-symbols-outlined text-primary/50 text-4xl mb-2 group-hover/slot:text-primary transition-colors">history</span>
                            <p class="text-sm font-headline font-bold tracking-widest text-primary uppercase">Before Scan</p>
                            <p class="text-[10px] font-mono text-white/40 mt-1 uppercase tracking-wider">Select Image</p>
                        </div>
                    </div>
                    
                    <!-- After Slot -->
                    <div id="slotAfter" class="image-slot group/slot w-full h-full flex flex-col items-center justify-center relative border border-white/10 bg-black/40 hover:bg-black/60 rounded-xl transition-colors cursor-pointer" onclick="event.stopPropagation(); event.preventDefault(); document.getElementById('fileInputAfter').click();">
                        <img id="previewAfter" src="" class="absolute inset-0 w-full h-full object-cover hidden opacity-60 rounded-xl">
                        <div class="z-10 text-center pointer-events-none p-4 w-full h-full flex flex-col items-center justify-center">
                            <span class="material-symbols-outlined text-primary/50 text-4xl mb-2 group-hover/slot:text-primary transition-colors">trending_up</span>
                            <p class="text-sm font-headline font-bold tracking-widest text-primary uppercase">Recent Scan</p>
                            <p class="text-[10px] font-mono text-white/40 mt-1 uppercase tracking-wider">Select Image</p>
                        </div>
                    </div>
                </div>

                <input type="file" id="fileInput" class="hidden" accept="image/*">
            </label>
            
            <input type="file" id="fileInputBefore" class="hidden" accept="image/*">
            <input type="file" id="fileInputAfter" class="hidden" accept="image/*">

            <div class="mt-6 flex justify-between items-center h-8">
                <button id="resetBtn" class="text-white/50 hover:text-white text-sm font-headline uppercase tracking-widest transition-colors hidden focus:outline-none flex items-center gap-1 group">
                    <span class="material-symbols-outlined text-base group-hover:-rotate-180 transition-transform duration-500">restart_alt</span> Reset
                </button>
                <div id="statusIndicator" class="text-primary text-xs font-mono uppercase tracking-widest flex items-center gap-2 ml-auto">
                    <span class="material-symbols-outlined text-base hidden" id="statusIcon">hourglass_empty</span>
                    <span id="statusText">Awaiting Input...</span>
                </div>
            </div>
        </div>
        
        <!-- Right Panel: Results -->
        <div class="glass-panel p-6 md:p-8 rounded-3xl lg:w-96 flex flex-col relative overflow-hidden transition-all duration-500 shadow-2xl min-h-[400px]">
            <!-- Background element -->
            <div class="absolute right-0 bottom-0 opacity-[0.03] pointer-events-none">
                <span class="material-symbols-outlined text-[200px] transform rotate-12">radar</span>
            </div>
            
            <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
            
            <h2 class="font-headline text-2xl font-black uppercase tracking-widest mb-6 text-white text-center border-b border-white/10 pb-4">
                INTEL REPORT
            </h2>
            
            <div id="resultsContainer" class="flex-1 flex flex-col z-10 transition-opacity duration-300">
                <!-- Initial State -->
                <div id="noDataState" class="flex flex-col items-center justify-center flex-1 opacity-50 py-12">
                    <span class="material-symbols-outlined text-5xl mb-4 text-primary/30">monitoring</span>
                    <p class="text-xs font-mono tracking-widest text-center uppercase text-white/50">Awaiting scan data<br/>for analysis</p>
                </div>
                
                <!-- Results UI injects here -->
                <div id="resultsList" class="w-full space-y-3 flex-1 overflow-y-auto hidden pr-2 scrollbar-hide py-2"></div>
            </div>
        </div>
    </main>

\n'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content[:start_idx] + new_html + content[end_idx:])
    print('Replaced layout successfully.')
else:
    print('Failed to find markers.')
