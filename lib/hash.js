// Small SHA-256 helper built on the native crypto.subtle API

export function normalizeAnswer(raw) {
  return raw.trim().toLowerCase().replace(/\s+/g, ' ');
}

export async function sha256Hex(text) {
  const data = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

export async function answerHash(raw) {
  return sha256Hex(normalizeAnswer(raw));
}
