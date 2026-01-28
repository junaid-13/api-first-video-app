const BASE_URL = 'http://<BACKEND_IP>:5000/api/v1';

let accessToken: string | null = null;

export const setAccessToken = (token: string) => {
  accessToken = token;
};

export const apiRequest = async (
  endpoint: string,
  method: string = 'GET',
  body?: any
) => {
  const headers: any = {
    'Content-Type': 'application/json',
  };

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.error?.message || 'API Error');
  }

  return data;
};
