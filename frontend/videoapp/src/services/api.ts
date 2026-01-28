const BASE_URL = "http://3.238.68.13:5000/api/v1";

/* ---------- AUTH ---------- */
export async function login(email: string, password: string) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  return response.json(); // { access_token, refresh_token }
}

/* ---------- VIDEOS ---------- */
export async function fetchVideos(token: string) {
  const response = await fetch(`${BASE_URL}/video`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch videos");
  }

  return response.json(); // { videos: [...] }
}

/* ---------- STREAM URL ---------- */
export function getStreamUrl(videoId: string) {
  return `${BASE_URL}/video/${videoId}/stream`;
}
