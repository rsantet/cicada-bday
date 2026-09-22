import { answerHash } from './hash.js';
import { STAGE_HASHES } from './stages.js';

// lib/ always sits exactly one level below the site root, no matter
// which page (portal or a stage) imports this module, and no matter
// how that page's own URL happens to be formatted (with or without a
// trailing slash - which changes how *relative* links resolve). So we
// anchor redirects to this script's own fixed location instead of
// trying to infer a path depth from window.location.
const SITE_ROOT = new URL('..', import.meta.url);

export function mountPortalWidget(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

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
      window.location.href = new URL(match.next, SITE_ROOT).href;
    } else {
      feedback.textContent = 'Ce n\'est pas ça. Essaie encore !';
      input.select();
    }
  });
}
