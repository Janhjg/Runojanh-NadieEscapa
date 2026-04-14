const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export async function fetchAllCrimes(limit = 20, offset = 0) {
  const response = await fetch(`${API_BASE_URL}/crimes?limit=${limit}&offset=${offset}`);
  if (!response.ok) throw new Error('Failed to fetch crimes');
  return response.json();
}

export async function submitFullCase(datosCrimen: any) {
  const response = await fetch(`${API_BASE_URL}/full-case/new`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ datos_crimen: datosCrimen }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to process full case');
  }
  return response.json();
}

export async function predictCrime(datosCrimen: any) {
  const response = await fetch(`${API_BASE_URL}/predict/new`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datosCrimen),
  });
  if (!response.ok) throw new Error('Failed to predict');
  return response.json();
}

export async function classifyCrime(datosCrimen: any, prediccionMl: any) {
  const response = await fetch(`${API_BASE_URL}/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ datos_crimen: datosCrimen, prediccion_ml: prediccionMl }),
  });
  if (!response.ok) throw new Error('Failed to classify');
  return response.json();
}

export async function narrateCrime(datosCrimen: any, prediccionMl: any, etiquetas: any) {
  const response = await fetch(`${API_BASE_URL}/narrate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      datos_crimen: datosCrimen, 
      prediccion_ml: prediccionMl, 
      etiquetas_huggingface: etiquetas 
    }),
  });
  if (!response.ok) throw new Error('Failed to narrate');
  return response.json();
}

export async function fetchFullCaseById(id: number) {
  const response = await fetch(`${API_BASE_URL}/full-case/${id}`);
  if (!response.ok) throw new Error('Failed to fetch full case by ID');
  return response.json();
}
