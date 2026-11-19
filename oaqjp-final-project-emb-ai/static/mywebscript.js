const form = document.querySelector('#emotion-form');
const button = form.querySelector('button');
const results = document.querySelector('#results');
const reply = document.querySelector('#system_response');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const params = new URLSearchParams(new FormData(form));
  button.disabled = true;
  results.dataset.state = 'loading';
  reply.textContent = 'Analyzing…';

  try {
    const response = await fetch(`${form.action}?${params}`);
    reply.textContent = await response.text();
    results.dataset.state = response.ok ? 'success' : 'error';
  } catch {
    reply.textContent = 'Could not reach the application. Please try again.';
    results.dataset.state = 'error';
  } finally {
    button.disabled = false;
  }
});
