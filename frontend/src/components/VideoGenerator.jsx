import { useState } from "react";
import { generateVideo } from "../api/api.js";
import { ErrorBox, PrimaryButton, SelectField, TextAreaField } from "./FormControls.jsx";
import VideoCanvasPreview from "./VideoCanvasPreview.jsx";

const genres = ["General", "Comedy", "Educational", "Advertisement", "Short Film", "Fantasy", "Sci-Fi", "Drama"];
const tones = ["Emotional", "Funny", "Cinematic", "Inspirational", "Suspenseful", "Professional"];
const styles = ["vertical 3D cinematic animated story", "sample-style cartoon cinematic", "realistic social media video", "anime short video", "educational motion story", "advertisement reel style"];
const durations = [5, 10, 15, 20, 30, 45, 60];

export default function VideoGenerator() {
  const [prompt, setPrompt] = useState("");
  const [genre, setGenre] = useState("General");
  const [tone, setTone] = useState("Emotional");
  const [style, setStyle] = useState("vertical 3D cinematic animated story");
  const [duration, setDuration] = useState(15);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (prompt.trim().length < 3) {
      setError("Please write a proper script, story idea, or video prompt first.");
      return;
    }

    setLoading(true);
    try {
      const data = await generateVideo({ prompt, genre, tone, style, duration: Number(duration) });
      setResult(data);
    } catch (err) {
      setError(err.message || "Video generation failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
      <form onSubmit={handleSubmit} className="glass-card rounded-3xl p-6">
        <div className="mb-5">
          <p className="text-sm uppercase tracking-[0.22em] text-fuchsia-300">Module 2</p>
          <h2 className="mt-2 text-2xl font-bold text-white">AI Video Generator</h2>
          <p className="mt-2 text-sm leading-6 text-slate-200">
            Ye image generator se completely separate hai. User script/prompt dega aur app video prompt, narration, scenes, aur video preview banayegi.
          </p>
        </div>

        <div className="space-y-4">
          <TextAreaField
            label="Script / Story Idea / Video Prompt"
            value={prompt}
            onChange={setPrompt}
            placeholder="Example: A biscuit and tea cup are in a courtroom, emotional funny animated short video, vertical format..."
          />

          <div className="grid gap-4 md:grid-cols-2">
            <SelectField label="Genre" value={genre} onChange={setGenre} options={genres} />
            <SelectField label="Tone" value={tone} onChange={setTone} options={tones} />
            <SelectField label="Video Style" value={style} onChange={setStyle} options={styles} />
            <SelectField label="Duration" value={duration} onChange={setDuration} options={durations} />
          </div>

          <ErrorBox message={error} />
          <PrimaryButton loading={loading}>Generate Video</PrimaryButton>
        </div>
      </form>

      <section className="glass-card rounded-3xl p-6">
        <h3 className="text-xl font-bold text-white">Video Output</h3>
        {!result ? (
          <div className="mt-5 flex min-h-[500px] items-center justify-center rounded-3xl border border-dashed border-slate-600 bg-slate-900/70 p-8 text-center text-slate-200">
            Generated video preview will appear here.
          </div>
        ) : (
          <div className="mt-5 space-y-5">
            {result.video_url ? (
              <video src={result.video_url} controls className="mx-auto w-full max-w-[380px] rounded-[2rem] border border-slate-700 bg-black" />
            ) : (
              <VideoCanvasPreview plan={result} />
            )}

            <div className="rounded-3xl border border-slate-700 bg-slate-950/60 p-5">
              <p className="text-sm text-slate-200">AI video prompt</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">{result.video_prompt}</p>
              <p className="mt-4 text-sm text-slate-200">Narration</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">{result.narration}</p>
              <p className="mt-4 text-xs text-slate-300">Provider: {result.video_provider} | Status: {result.video_status}</p>
            </div>

            {result.audio_url && (
              <audio src={result.audio_url} controls className="w-full" />
            )}

            <div className="grid gap-3">
              {result.scenes?.map((scene, index) => (
                <div key={`${scene.caption}-${index}`} className="rounded-2xl border border-slate-700 bg-slate-900/70 p-4">
                  <p className="font-semibold text-white">Scene {scene.scene_number || index + 1}: {scene.caption}</p>
                  <p className="mt-2 text-sm text-slate-200">{scene.visual_prompt}</p>
                  <p className="mt-2 text-xs text-sky-300">Camera: {scene.camera_motion || "slow cinematic movement"}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

