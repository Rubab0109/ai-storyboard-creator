import { useEffect, useRef, useState } from "react";

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const words = String(text || "").split(" ");
  let line = "";
  let currentY = y;

  for (let index = 0; index < words.length; index += 1) {
    const testLine = `${line}${words[index]} `;
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && index > 0) {
      ctx.fillText(line, x, currentY);
      line = `${words[index]} `;
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }
  ctx.fillText(line, x, currentY);
}

function drawScene(ctx, canvas, scene, title, frame) {
  const w = canvas.width;
  const h = canvas.height;
  const t = frame / 60;

  const gradient = ctx.createLinearGradient(0, 0, w, h);
  gradient.addColorStop(0, "#020617");
  gradient.addColorStop(0.45, "#312e81");
  gradient.addColorStop(1, "#0f172a");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, w, h);

  ctx.save();
  ctx.globalAlpha = 0.28;
  ctx.fillStyle = "#38bdf8";
  ctx.beginPath();
  ctx.arc(w * 0.26 + Math.sin(t) * 30, h * 0.25, 180, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#f472b6";
  ctx.beginPath();
  ctx.arc(w * 0.78 + Math.cos(t) * 40, h * 0.62, 210, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  const zoom = 1 + Math.sin(t / 2) * 0.025;
  ctx.save();
  ctx.translate(w / 2, h / 2);
  ctx.scale(zoom, zoom);
  ctx.translate(-w / 2, -h / 2);

  ctx.fillStyle = "rgba(15, 23, 42, 0.62)";
  ctx.roundRect(50, 130, w - 100, h - 260, 44);
  ctx.fill();
  ctx.strokeStyle = "rgba(147, 197, 253, 0.45)";
  ctx.lineWidth = 3;
  ctx.stroke();

  ctx.fillStyle = "rgba(255,255,255,0.10)";
  ctx.roundRect(125, 245, w - 250, 420, 50);
  ctx.fill();
  ctx.strokeStyle = "rgba(255,255,255,0.22)";
  ctx.stroke();

  ctx.fillStyle = "#ffffff";
  ctx.font = "700 42px Arial";
  ctx.textAlign = "center";
  wrapText(ctx, scene?.caption || title, w / 2, 760, w - 150, 52);

  ctx.fillStyle = "#bae6fd";
  ctx.font = "24px Arial";
  wrapText(ctx, scene?.visual_prompt || "AI cinematic vertical scene", w / 2, 895, w - 160, 34);
  ctx.restore();

  ctx.fillStyle = "rgba(2, 6, 23, 0.72)";
  ctx.roundRect(42, 42, w - 84, 82, 24);
  ctx.fill();
  ctx.fillStyle = "#e0f2fe";
  ctx.font = "700 28px Arial";
  ctx.textAlign = "left";
  ctx.fillText(title || "AI Video Preview", 72, 94);

  ctx.fillStyle = "rgba(2, 6, 23, 0.78)";
  ctx.roundRect(55, h - 150, w - 110, 92, 28);
  ctx.fill();
  ctx.fillStyle = "#ffffff";
  ctx.font = "700 34px Arial";
  ctx.textAlign = "center";
  wrapText(ctx, scene?.caption || "Generated cinematic moment", w / 2, h - 96, w - 150, 42);
}

export default function VideoCanvasPreview({ plan }) {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const recorderRef = useRef(null);
  const chunksRef = useRef([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");

  const scenes = plan?.scenes?.length ? plan.scenes : [{ caption: "AI generated scene", visual_prompt: plan?.video_prompt }];

  function renderFrame(frame = 0) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const sceneIndex = Math.floor(frame / 120) % scenes.length;
    drawScene(ctx, canvas, scenes[sceneIndex], plan?.title || "AI Video Preview", frame);
  }

  useEffect(() => {
    renderFrame(0);
    return () => cancelAnimationFrame(animationRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [plan]);

  function playPreview() {
    setIsPlaying(true);
    let frame = 0;
    const loop = () => {
      renderFrame(frame);
      frame += 1;
      animationRef.current = requestAnimationFrame(loop);
    };
    loop();
  }

  function stopPreview() {
    setIsPlaying(false);
    cancelAnimationFrame(animationRef.current);
    renderFrame(0);
  }

  function speakNarration() {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(plan?.narration || plan?.video_prompt || "AI video preview generated.");
    utterance.rate = 0.95;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  function startRecording() {
    const canvas = canvasRef.current;
    if (!canvas || !canvas.captureStream || !window.MediaRecorder) {
      alert("Your browser does not support canvas video recording. Use Chrome or Edge.");
      return;
    }

    chunksRef.current = [];
    const stream = canvas.captureStream(30);
    const recorder = new MediaRecorder(stream, { mimeType: "video/webm" });
    recorderRef.current = recorder;

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunksRef.current.push(event.data);
    };
    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: "video/webm" });
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
    };

    playPreview();
    recorder.start();
    setTimeout(() => {
      recorder.stop();
      stopPreview();
    }, Math.max(5, Number(plan?.duration || 15)) * 1000);
  }

  return (
    <div className="space-y-4">
      <div className="mx-auto w-full max-w-[360px] overflow-hidden rounded-[2rem] border border-slate-700 bg-black shadow-2xl">
        <canvas ref={canvasRef} width="720" height="1280" className="h-auto w-full" />
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <button onClick={isPlaying ? stopPreview : playPreview} className="rounded-2xl border border-sky-400/30 bg-sky-400/10 px-4 py-3 font-semibold text-sky-100 hover:bg-sky-400/20">
          {isPlaying ? "Stop Preview" : "Play Preview"}
        </button>
        <button onClick={speakNarration} className="rounded-2xl border border-violet-400/30 bg-violet-400/10 px-4 py-3 font-semibold text-violet-100 hover:bg-violet-400/20">
          Play Narration
        </button>
        <button onClick={startRecording} className="rounded-2xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3 font-semibold text-emerald-100 hover:bg-emerald-400/20">
          Record Preview
        </button>
      </div>
      {downloadUrl && (
        <a href={downloadUrl} download="ai-video-preview.webm" className="block rounded-2xl bg-emerald-500 px-5 py-3 text-center font-bold text-white">
          Download Recorded Preview
        </a>
      )}
    </div>
  );
}
