import { answerHash } from './hash.js';
import { STAGE_HASHES } from './stages.js';

function computeDepth() {
  // Stage pages live one directory below the site root
  // (e.g. /stage-3-ab12cd34/index.html), the portal lives at the root.
  const path = window.location.pathname.replace(/index\.html$/, '');
  const segments = path.split('/').filter(Boolean);
  return segments.length;
}

export function mountPortalWidget(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const depth = computeDepth();
  const prefix = depth > 0 ? '../'.repeat(depth) : '';

  container.innerHTML = `
    <form class="portal-form" autocomplete="off">
      <input id="portal-input" type="text" placeholder="..." spellcheck="false" />
      <button type="submit">Unlock</button>
      <p class="portal-feedback" id="portal-feedback" aria-live="polite"></p>
    </form>
  `;

  const form = container.querySelector('.portal-form');
  const input = container.querySelector('#portal-input');
  const feedback = container.querySelector('#portal-feedback');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const value = input.value;
    if (!value) return;

    feedback.textContent = 'Je checke...';
    const hash = await answerHash(value);
    const match = STAGE_HASHES.find((entry) => entry.hash === hash);

    if (match) {
      feedback.textContent = 'Bravooooo! Je t\'emmène au bon endroit...';
      window.location.href = prefix + match.next;
    } else {
      feedback.textContent = 'Ce n\'est pas ça. Essaie encore !';
      input.select();
    }
  });
}
