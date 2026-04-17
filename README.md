<div align="center">

# 🌍 AI Damage Assessment Intel System
**A real-time, high-performance disaster intelligence and computer vision pipeline.**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React / Vite](https://img.shields.io/badge/React_Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Roboflow](https://img.shields.io/badge/Roboflow-6706CE?style=for-the-badge&logo=roboflow&logoColor=white)](https://roboflow.com/)

---

<p align="center">
  <img src="docs/demo.webp" alt="Scanning Animation" width="100%" style="border-radius: 12px; border: 1px solid rgba(255,183,3,0.3);"/>
</p>

### 📸 Application Interface

<p align="center">
  <img src="docs/hero.png" width="49%" style="border-radius: 8px;"/>
  <img src="docs/dashboard.png" width="49%" style="border-radius: 8px;"/>
</p>


</div>

## 🚀 Overview

The **Damage Assessment System** is an industry-grade, zero-trust web application designed for rapid disaster telemetry analysis. By utilizing **Roboflow's serverless workflows** and a custom **FastAPI proxy**, it analyzes airborne drone imagery or satellite feeds to classify disasters (Floods, Fires, Tornadoes) and assesses structural damage severity instantly.

### ✨ Key Features
- **Zero Secret Exposure**: Roboflow API keys are proxy-secured via the backend.
- **GSAP 3D Glitch Interface**: Deeply immersive, Awwwards-style frontend with real-time SVG intelligence gauges.
- **Base64 Inference Engine**: Serverless image chunking and streaming.
- **Dual-Mode Telemetry**: Choose between Single Scan or Before/After structural comparisons.

---

## 🏗️ Architecture

The project has been **segregated** into a strict Frontend (`Github repo`) and Backend (`packaged zip`) architecture for maximum security.

* **Frontend**: React, Vite, TSX, Tailwind CSS, GSAP
* **Backend Hub**: Python FastAPI, Uvicorn, Inference-SDK

---

## 💻 1. Frontend Setup (React/Vite)

This codebase controls the highly-interactive UI.

```bash
# 1. Clone the repository
git clone git@github.com:Aditgm/damage_assessment.git
cd damage_assessment

# 2. Install Dependencies
npm install

# 3. Launch Development Server
npm run dev
```
> The dashboard will spin up at `http://localhost:5173`. It expects the local backend gateway to be active on port `8000`.

---

## 🔒 2. Backend Setup (FastAPI Proxy)

> **Note**: For security, backend files are not stored in this GitHub repository. Obtain the `backend_release.zip` package.

Once extracted:

1. **Configure API Keys**: Rename `.env.example` -> `.env` and insert your actual `ROBOFLOW_API_KEY`.
2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the API Server**:
   ```bash
   python -m uvicorn app:app --host 127.0.0.1 --port 8000
   ```
The proxy runs natively holding endpoints at `/scan`. 

---

## 🎨 UI/UX Design System

- **Immersive GSAP Hero**: A 3D "Ultra Glitch" header synchronized with granular HTML Canvas `<PixelTrail />` elements.
- **Radar Scan Overlays**: Real-time sweeping animations mapped precisely to 8px CSS grid gradients.
- **Tactical Intel Cards**: Color-coded categorization modules representing `CRITICAL`, `MODERATE`, and `SAFE` severity contexts.

---

<div align="center">
  Generated with System Integration Protocols - AI Pipeline Edition
</div>
