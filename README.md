# AI Storyboard Creator

AI Storyboard Creator is a dark-theme web application for creative multimedia generation. It contains two independent modules:

1. **AI Image Generator** — user gives a scene/script/prompt and the app generates exactly one image.
2. **AI Video Generator** — user gives a script/story/video prompt and the app generates an independent vertical AI video plan with optional AI video API output and a browser-based animated preview fallback.

The image and video modules do not depend on each other.

---

## Features

### Image Generator
- Scene/script/prompt input
- Genre, tone, and style selectors
- LLM prompt enhancement
- One-image generation
- Download image option
- Placeholder fallback if image API key is missing

### Video Generator
- Script/story/video prompt input
- Genre, tone, style, and duration selectors
- LLM video prompt generation
- Narration generation
- Scene/caption planning
- Optional Replicate video API support
- Browser animated 9:16 preview fallback
- Browser narration playback
- WebM preview recording and download

---

## Technology Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Browser Speech API
- Canvas + MediaRecorder fallback preview

### Backend
- FastAPI
- Python
- Gemini/OpenAI optional LLM integration
- OpenAI image API optional
- Replicate video API optional
- ElevenLabs optional TTS
- Local metadata storage fallback

---

## Project Structure

```text
AI-Storyboard-Creator/
├── backend/
│   ├── index.py
│   ├── requirements.txt
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── image_service.py
│   │   ├── video_service.py
│   │   ├── tts_service.py
│   │   └── storage_service.py
│   └── tests/
│       └── test_app.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── api/api.js
│   │   └── components/
│   ├── package.json
│   ├── index.html
│   ├── tailwind.config.js
│   └── postcss.config.js
├── README.md
├── .env.example
└── report_outline.md
```

---

## Local Setup

### 1. Run Backend

```bash
cd backend
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Create `.env` file inside `backend/`:

```bash
copy .env.example .env
```

Run backend:

```bash
python -m uvicorn index:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/api/health
```

---

### 2. Run Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

## Environment Variables

The app works without keys using safe fallback mode. For real AI output, add keys in backend `.env`.

```env
FRONTEND_URL=http://localhost:5173
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
REPLICATE_API_TOKEN=your_replicate_token
REPLICATE_VIDEO_MODEL=owner/model-name
ELEVENLABS_API_KEY=your_elevenlabs_key
```

Frontend `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

---

## Deploy Backend on Vercel

1. Push this project to GitHub.
2. Open Vercel.
3. Add New Project.
4. Import GitHub repository.
5. Set **Root Directory** to:

```text
backend
```

6. Keep framework as Other / automatic.
7. Add environment variables:

```env
FRONTEND_URL=https://your-frontend-vercel-url.vercel.app
GEMINI_API_KEY=optional
OPENAI_API_KEY=optional
REPLICATE_API_TOKEN=optional
REPLICATE_VIDEO_MODEL=optional
ELEVENLABS_API_KEY=optional
```

8. Deploy.
9. After deployment, open:

```text
https://your-backend-url.vercel.app/api/health
```

Expected response:

```json
{"status":"ok"}
```

---

## Deploy Frontend on Vercel

1. Add New Project in Vercel.
2. Import the same GitHub repository again.
3. Set **Root Directory** to:

```text
frontend
```

4. Framework should detect Vite.
5. Add environment variable:

```env
VITE_API_URL=https://your-backend-url.vercel.app
```

6. Deploy.

---

## Testing

Run backend tests:

```bash
cd backend
pytest
```

Tests include:
- Empty input validation
- Very short prompt validation
- Invalid duration validation
- Image API fallback
- Video API fallback
- Health endpoint

---

## Sample Input

### Image Generator Input

```text
A scared biscuit standing in a courtroom while a tea cup defends him, funny emotional 3D animated style.
```

Expected output:
- One image only
- Refined image prompt
- Download button

### Video Generator Input

```text
A biscuit and a tea cup are in a courtroom. The biscuit is blamed for breaking a plate, but the tea cup proves he is innocent. Make it funny, emotional, and vertical cinematic.
```

Expected output:
- Video prompt
- Narration
- Scene plan
- Animated vertical preview
- Optional video URL if video API is configured

---

## How It Works

### LLM
The backend sends the user input to Gemini or OpenAI. The LLM improves prompts, creates video narration, and builds a scene plan.

### Image Generation
The backend tries OpenAI image generation. If no key exists, the app returns a generated SVG placeholder so the UI still works.

### Video Generation
The backend can call a Replicate video model if configured. If no video API is configured, the frontend uses Canvas and MediaRecorder to create a vertical animated preview from the LLM video plan.

### TTS
The backend can use ElevenLabs if configured. If no TTS key exists, the frontend uses browser speech synthesis.

---

## Limitations

- Real AI video generation requires a paid or configured video API.
- Vercel serverless storage is temporary, so permanent storage should use Supabase, Firebase, or S3 in production.
- Browser-recorded WebM preview may not include narration audio.
- Placeholder image mode is for testing/demo only.

---

## Future Improvements

- Add user login
- Add project history dashboard
- Add cloud storage
- Add real video model provider selection
- Add MP4 export with cloud rendering
- Add subtitle burn-in
- Add character consistency controls
- Add aspect ratio controls
- Add payment/subscription support
