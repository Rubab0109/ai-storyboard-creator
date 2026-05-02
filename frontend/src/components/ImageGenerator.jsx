import { useState } from "react";
import { generateImage } from "../api/api.js";
import { ErrorBox, PrimaryButton, SelectField, TextAreaField } from "./FormControls.jsx";

const genres = ["General", "Comedy", "Educational", "Advertisement", "Short Film", "Fantasy", "Sci-Fi", "Drama"];
const tones = ["Cinematic", "Funny", "Emotional", "Professional", "Suspenseful", "Inspirational"];
const styles = ["3D animated cinematic", "Pixar-like 3D style", "Realistic cinematic", "Anime style", "Digital art", "Poster design", "Cartoon style"];

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState("");
  const [genre, setGenre] = useState("General");
  const [tone, setTone] = useState("Cinematic");
  const [style, setStyle] = useState("3D animated cinematic");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (prompt.trim().length < 3) {
      setError("Please write a proper scene, script, or prompt first.");
      return;
    }

    setLoading(true);
    try {
      const data = await generateImage({ prompt, genre, tone, style });
      setResult(data);
    } catch (err) {
      setError(err.message || "Image generation failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
      <form onSubmit={handleSubmit} className="glass-card rounded-3xl p-6">
        <div className="mb-5">
          <p className="text-sm uppercase tracking-[0.22em] text-sky-300">Module 1</p>
          <h2 className="mt-2 text-2xl font-bold text-white">AI Image Generator</h2>
          <p className="mt-2 text-sm leading-6 text-slate-200">
            User scene/script/prompt dega aur app us ke mutabik exactly one final image generate karegi.
          </p>
        </div>

        <div className="space-y-4">
          <TextAreaField
            label="Scene / Script / Prompt"
            value={prompt}
            onChange={setPrompt}
            placeholder="Example: A scared biscuit standing in a courtroom while a tea cup defends him, emotional 3D cartoon style..."
          />

          <div className="grid gap-4 md:grid-cols-3">
            <SelectField label="Genre" value={genre} onChange={setGenre} options={genres} />
            <SelectField label="Tone" value={tone} onChange={setTone} options={tones} />
            <SelectField label="Style" value={style} onChange={setStyle} options={styles} />
          </div>

          <ErrorBox message={error} />
          <PrimaryButton loading={loading}>Generate One Image</PrimaryButton>
        </div>
      </form>

      <section className="glass-card rounded-3xl p-6">
        <h3 className="text-xl font-bold text-white">Image Output</h3>
        {!result ? (
          <div className="mt-5 flex min-h-[420px] items-center justify-center rounded-3xl border border-dashed border-slate-600 bg-slate-900/70 p-8 text-center text-slate-200">
            Generated image preview will appear here.
          </div>
        ) : (
          <div className="mt-5 space-y-5">
            <img
              src={result.image_url}
              alt={result.title}
              className="w-full rounded-3xl border border-slate-700 object-cover shadow-2xl"
            />
            <div className="rounded-3xl border border-slate-700 bg-slate-950/60 p-5">
              <p className="text-sm text-slate-200">Refined prompt</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">{result.refined_prompt}</p>
              <p className="mt-4 text-xs text-slate-300">Provider: {result.image_provider} | Status: {result.image_status}</p>
            </div>
            <a
              href={result.image_url}
              download="ai-generated-image.svg"
              className="block rounded-2xl border border-sky-400/30 bg-sky-400/10 px-5 py-3 text-center font-semibold text-sky-200 transition hover:bg-sky-400/20"
            >
              Download Image
            </a>
          </div>
        )}
      </section>
    </div>
  );
}

