const A = 'A'.charCodeAt(0);

function shiftChar(ch, amount) {
  const code = ch.toUpperCase().charCodeAt(0) - A;
  const shifted = ((code + amount) % 26 + 26) % 26;
  return String.fromCharCode(shifted + A);
}

export function vigenereEncrypt(plaintext, key) {
  const cleanKey = key.toUpperCase().replace(/[^A-Z]/g, '');
  if (!cleanKey) throw new Error('Vigenere key must contain letters');
  let keyIndex = 0;
  let out = '';
  for (const ch of plaintext.toUpperCase()) {
    if (/[A-Z]/.test(ch)) {
      const keyShift = cleanKey.charCodeAt(keyIndex % cleanKey.length) - A;
      out += shiftChar(ch, keyShift);
      keyIndex += 1;
    } else {
      out += ch;
    }
  }
  return out;
}

export function vigenereDecrypt(ciphertext, key) {
  const cleanKey = key.toUpperCase().replace(/[^A-Z]/g, '');
  if (!cleanKey) throw new Error('Vigenere key must contain letters');
  let keyIndex = 0;
  let out = '';
  for (const ch of ciphertext.toUpperCase()) {
    if (/[A-Z]/.test(ch)) {
      const keyShift = cleanKey.charCodeAt(keyIndex % cleanKey.length) - A;
      out += shiftChar(ch, -keyShift);
      keyIndex += 1;
    } else {
      out += ch;
    }
  }
  return out;
}
