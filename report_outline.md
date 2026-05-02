# AI Storyboard Creator — 25–30 Page Report Outline

## Title Page
- Project title: AI Storyboard Creator
- Group members
- Roll numbers
- Department
- Semester
- Subject
- Teacher name
- University
- Submission date
- GitHub repository link
- Frontend deployed link
- Backend deployed link

## Abstract
AI Storyboard Creator is a creative AI web application that helps multimedia students and content creators generate professional image and video concepts from simple text prompts. The system has two independent modules: an AI Image Generator and an AI Video Generator. The image module creates one final image from a scene/script/prompt. The video module creates a separate short-form vertical video concept with narration, scene planning, and preview support.

## Page 1: Introduction
- Background of multimedia content creation
- Importance of storyboards in films, ads, education, and social media
- Problem faced by students and creators
- Need for AI-assisted creative tools

## Page 2: Problem Statement
- Manual storyboard creation is time-consuming
- Students may not have drawing or video production skills
- Creative planning requires script, visuals, narration, and preview
- Existing tools may be expensive or complex

## Page 3: Project Goal
- Convert text ideas into creative multimedia outputs
- Provide one-image generation
- Provide separate video generation workflow
- Build a working web prototype
- Make app beginner-friendly and deployable

## Page 4: Objectives
- Create a modern dark UI
- Integrate LLM for prompt enhancement
- Generate one image from user input
- Generate video prompt, narration, and preview from user input
- Add graceful fallback for missing APIs
- Deploy frontend and backend on Vercel

## Page 5: Scope of Project
- Text-to-image generation
- Text-to-video planning/generation
- Narration text generation
- Browser speech fallback
- Download support
- API error handling

## Page 6: Real-World Use Cases
- Short film planning
- Social media reels
- Educational videos
- Advertising campaigns
- YouTube story videos
- Classroom multimedia assignments

## Page 7: System Overview
- Frontend React interface
- Backend FastAPI API
- LLM service
- Image generation service
- Video generation service
- TTS service
- Storage service

## Page 8: System Architecture Diagram
Suggested diagram:
User → React Frontend → FastAPI Backend → LLM/Image/Video/TTS Services → Output Preview

## Page 9: Module 1 — AI Image Generator
- User enters scene/script/prompt
- Genre, tone, and style selection
- LLM refines prompt
- Image model generates one image
- Fallback image shown if API is unavailable

## Page 10: Module 2 — AI Video Generator
- User enters script/story idea/video prompt
- Genre, tone, style, and duration selection
- LLM creates video prompt
- LLM creates narration
- AI video API optional
- Canvas preview fallback

## Page 11: Why Image and Video Modules Are Separate
- Image generator creates one image only
- Video generator creates separate video plan/output
- Image output is not required for video
- Better UX and clearer assignment flow

## Page 12: Technology Stack
- React.js
- Tailwind CSS
- FastAPI
- Gemini/OpenAI/Groq optional
- OpenAI Image API optional
- Replicate video API optional
- ElevenLabs/browser speech
- Vercel deployment

## Page 13: Frontend Design
- Dark theme
- Tab-based layout
- Separate input forms
- Output cards
- Responsive layout
- Loading and error states

## Page 14: Backend Design
- REST API endpoints
- Request validation
- Service-based architecture
- Error handling
- Environment variables

## Page 15: LLM Prompt Engineering
- Image prompt enhancement
- Video prompt generation
- Narration generation
- Scene planning
- JSON response parsing
- Fallback prompt generation

## Page 16: Image Generation Workflow
1. User enters input
2. Backend validates input
3. LLM refines prompt
4. Image service tries API
5. Fallback placeholder generated if API fails
6. Frontend displays image

## Page 17: Video Generation Workflow
1. User enters script/prompt
2. Backend validates duration and input
3. LLM creates video prompt and scenes
4. Optional video API called
5. If unavailable, frontend creates animated preview
6. User can preview and record WebM

## Page 18: TTS and Narration
- LLM creates narration text
- ElevenLabs optional backend audio
- Browser Speech API fallback
- Audio improves multimedia experience

## Page 19: Storage Module
- Metadata storage in local folder
- Temporary storage on Vercel
- Future cloud storage recommendation

## Page 20: API Endpoints
### GET /api/health
Checks backend status.

### POST /api/generate-image
Generates one image result.

### POST /api/generate-video
Generates independent video result.

### POST /api/tts
Generates optional TTS audio.

## Page 21: Testing Strategy
- Empty input test
- Short prompt test
- Long prompt test
- Invalid duration test
- Image API failure test
- Video API failure test
- Missing API key fallback test

## Page 22: Deployment
- GitHub repository
- Backend Vercel deployment
- Frontend Vercel deployment
- Environment variables
- API URL connection

## Page 23: Sample Input and Output
### Image Input
A scared biscuit standing in a courtroom while a tea cup defends him.

### Image Output
One generated image with refined prompt.

### Video Input
A biscuit and a tea cup are in a courtroom. Make it funny and emotional.

### Video Output
Video prompt, narration, scenes, and preview.

## Page 24: Screenshots Section
Add screenshots of:
- Home page
- Image generator form
- Image output
- Video generator form
- Video output
- Backend health endpoint
- Vercel deployment dashboard

## Page 25: Advantages
- Beginner-friendly
- Fast creative planning
- Dark professional UI
- Separate image/video flows
- Works without paid APIs using fallbacks
- Vercel deployable

## Page 26: Limitations
- Real AI video generation requires API key
- Vercel storage is temporary
- Browser preview is not full production video rendering
- WebM recording may not include narration audio
- Prompt quality depends on user input and LLM

## Page 27: Future Improvements
- Real MP4 rendering pipeline
- Cloud storage
- User authentication
- Project history
- Character consistency
- Subtitle editor
- Voice selection
- Multiple aspect ratios
- Advanced AI video models

## Page 28: Conclusion
AI Storyboard Creator provides a practical AI-based solution for multimedia students and creators. It reduces the time required for visual planning and supports both single-image generation and independent video generation. The project demonstrates LLM integration, image generation, video planning, TTS fallback, frontend-backend architecture, testing, deployment, and documentation.

---

# 5–7 Minute Demo Video Script

## 0:00–0:30 — Introduction
Assalam o Alaikum. Our project name is AI Storyboard Creator. This is a Generative AI web application for multimedia students and content creators. It helps users generate either a single AI image or a separate AI video concept from a simple text prompt.

## 0:30–1:10 — Problem Explanation
Multimedia students often need storyboards, visuals, and video ideas for short films, ads, educational videos, and social media. Creating these manually takes time and design skills. Our app solves this problem using AI.

## 1:10–1:50 — App Overview
The app has a professional dark theme UI. There are two main modules: AI Image Generator and AI Video Generator. These modules are separate. The image generator creates one image only, while the video generator creates a separate video plan and preview.

## 1:50–2:50 — Image Generator Demo
Now I open the Image Generator tab. I enter a scene prompt: “A scared biscuit standing in a courtroom while a tea cup defends him.” Then I select genre, tone, and style. After clicking Generate One Image, the backend refines the prompt and generates one image. If the image API is unavailable, the app shows a fallback preview instead of crashing.

## 2:50–4:10 — Video Generator Demo
Now I open the Video Generator tab. I enter a video story idea. I select genre, tone, video style, and duration. After clicking Generate Video, the backend creates a video prompt, narration, and scene plan. If a real video API is configured, the app can show the generated video. If not, the frontend creates a vertical animated preview using Canvas.

## 4:10–5:00 — Backend Explanation
The backend is built with FastAPI. It has endpoints for image generation, video generation, TTS, and health checking. The backend uses separate services for LLM, image, video, TTS, and storage. API keys are stored safely in environment variables.

## 5:00–5:45 — Testing and Error Handling
The project includes tests for empty input, short prompt, invalid duration, image API failure, video API failure, and fallback behavior. This makes the app stable for demo and deployment.

## 5:45–6:30 — Deployment
The frontend and backend are deployed separately on Vercel. The frontend uses Vite React, and the backend uses FastAPI Python runtime. The frontend connects to the backend using VITE_API_URL.

## 6:30–7:00 — Conclusion
In conclusion, AI Storyboard Creator is a practical Generative AI application for multimedia content creation. It supports image generation, video planning, narration, preview, testing, deployment, and professional documentation.

---

# Sample Generated Storyboard Output

## Image Module Output
Input:
A scared biscuit standing in a courtroom while a tea cup defends him.

Output:
- Title: Generated Image
- Refined prompt: Create one high-quality 3D animated cinematic image of a scared biscuit in a courtroom...
- Image: one generated image or fallback preview

## Video Module Output
Input:
A biscuit and a tea cup are in a courtroom. The biscuit is blamed for breaking a plate, but the tea cup proves he is innocent.

Output:
- Title: AI Video Story
- Video prompt: Generate a vertical 9:16 animated cinematic short video...
- Narration: A funny emotional courtroom story unfolds...
- Scenes:
  1. Opening visual introduction
  2. Main character appears
  3. Conflict moment
  4. Emotional turning point
  5. Final reveal
