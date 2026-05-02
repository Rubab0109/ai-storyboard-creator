const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = { detail: "Server returned non-JSON response." };
  }

  if (!response.ok) {
    const message = Array.isArray(data.detail)
      ? data.detail.map((item) => item.msg).join(", ")
      : data.detail || "Request failed.";
    throw new Error(message);
  }
  return data;
}

export function generateImage(payload) {
  return request("/api/generate-image", payload);
}

export function generateVideo(payload) {
  return request("/api/generate-video", payload);
}

export { API_BASE };
