import { useState } from "react";
import { API_BASE } from "./api/api.js";
import ImageGenerator from "./components/ImageGenerator.jsx";
import VideoGenerator from "./components/VideoGenerator.jsx";

export default function App() {
  const [activeTab, setActiveTab] = useState("image");

  return (
    <main className="min-h-screen px-4 py-6 text-slate-100 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 overflow-hidden rounded-[2rem] border border-slate-800 bg-slate-950/70 p-6 shadow-2xl sm:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.25em] text-sky-300">Multimedia AI System</p>
              <h1 className="mt-3 text-4xl font-black tracking-tight sm:text-5xl">
                AI <span className="gradient-text">Storyboard Creator</span>
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-7 text-slate-400">
                Professional dark theme app with two independent modules: one prompt to one image, and separate AI video generation flow.
              </p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-4 text-sm text-slate-400">
              <p className="font-semibold text-slate-200">Backend API</p>
              <p className="mt-1 break-all">{API_BASE}</p>
            </div>
          </div>

          <div className="mt-8 grid gap-3 rounded-3xl bg-slate-900/80 p-2 sm:grid-cols-2">
            <button
              onClick={() => setActiveTab("image")}
              className={`rounded-2xl px-5 py-4 font-bold transition ${activeTab === "image" ? "bg-sky-500 text-white shadow-glow" : "text-slate-300 hover:bg-slate-800"}`}
            >
              Image Generator
            </button>
            <button
              onClick={() => setActiveTab("video")}
              className={`rounded-2xl px-5 py-4 font-bold transition ${activeTab === "video" ? "bg-fuchsia-500 text-white shadow-glow" : "text-slate-300 hover:bg-slate-800"}`}
            >
              Video Generator
            </button>
          </div>
        </header>

        {activeTab === "image" ? <ImageGenerator /> : <VideoGenerator />}

        <footer className="mt-8 rounded-3xl border border-slate-800 bg-slate-950/70 p-5 text-center text-sm text-slate-500">
          Image module and video module are intentionally separate. API errors are handled with safe fallbacks for assignment demo.
        </footer>
      </div>
    </main>
  );
}
