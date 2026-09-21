const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Low-level fetch wrapper: adds JSON headers, base URL, and normalized errors.
 */
async function request(path, { method = "GET", body } = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined
    });
  } catch {
    throw new ApiError("Could not reach the backend. Check your connection or try again.", 0);
  }

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json().catch(() => null) : null;

  if (!response.ok) {
    const message = payload?.detail || payload?.message || `Request failed (${response.status})`;
    throw new ApiError(message, response.status);
  }

  return payload;
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export const api = {
  checkHealth: () => request("/api/health"),

  /** @param {import('../types').PatientInput} patient */
  predict: (patient) => request("/api/predict", { method: "POST", body: patient }),
  assess: (patient) => request("/api/assess", { method: "POST", body: patient }),

  /** @param {import('../types').PatientInput} patient */
  explain: (patient) => request("/api/explain", { method: "POST", body: patient }),

  /** @param {string} question @param {import('../types').PatientInput=} context */
  askAgent: (question, context) =>
    request("/api/agent/ask", { method: "POST", body: { question, context } }),

  getModelInfo: () => request("/api/model-info")
};
