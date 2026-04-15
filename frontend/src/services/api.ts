const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// ─── Helper ──────────────────────────────────────────────────────────────────
async function apiFetch(url: string, options?: RequestInit) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error de red' }));
    throw new Error(error.detail || `Error ${response.status}`);
  }
  return response.json();
}

// ─── Dataset Crimes ───────────────────────────────────────────────────────────
export async function fetchAllCrimes(limit = 20, offset = 0, params = "") {
  return apiFetch(`${API_BASE_URL}/crimes?limit=${limit}&offset=${offset}${params}`);
}

export async function fetchCrimesMeta() {
  return apiFetch(`${API_BASE_URL}/crimes/meta`);
}

export async function fetchUserCases(limit = 20, offset = 0) {
  return apiFetch(`${API_BASE_URL}/user-cases?limit=${limit}&offset=${offset}`);
}

export async function fetchCrimeById(id: number) {
  return apiFetch(`${API_BASE_URL}/crimes/${id}`);
}

// ─── Predict ──────────────────────────────────────────────────────────────────
export async function predictCrime(datosCrimen: any) {
  return apiFetch(`${API_BASE_URL}/predict/new`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datosCrimen),
  });
}

export async function predictCrimeById(id: number) {
  return apiFetch(`${API_BASE_URL}/predict/${id}`);
}

// ─── Classify ────────────────────────────────────────────────────────────────
export async function classifyCrime(datosCrimen: any, prediccionMl: any) {
  return apiFetch(`${API_BASE_URL}/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ datos_crimen: datosCrimen, prediccion_ml: prediccionMl }),
  });
}

// ─── Narrate ──────────────────────────────────────────────────────────────────
export async function narrateCrime(datosCrimen: any, prediccionMl: any, etiquetas: any) {
  return apiFetch(`${API_BASE_URL}/narrate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      datos_crimen: datosCrimen,
      prediccion_ml: prediccionMl,
      etiquetas_huggingface: etiquetas
    }),
  });
}

// ─── Full Case ────────────────────────────────────────────────────────────────
export async function submitFullCase(datosCrimen: any) {
  return apiFetch(`${API_BASE_URL}/full-case/new`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ datos_crimen: datosCrimen }),
  });
}

export async function fetchFullCaseById(id: number) {
  return apiFetch(`${API_BASE_URL}/full-case/${id}`);
}
