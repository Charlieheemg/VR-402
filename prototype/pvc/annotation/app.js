'use strict';
const $ = id => document.getElementById(id);
let rater = '', clips = [], total = 0, completed = 0, busy = false, played = false;
async function request(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Request failed');
  return data;
}
function showClip() {
  $('rating-form').reset();
  played = false;
  $('save').disabled = true;
  $('audio').pause();
  $('rating').hidden = clips.length === 0;
  $('progress').textContent = `Clip ${completed + 1} of ${total}`;
  if (clips.length) {
    $('audio').src = '/audio?clip_id=' + encodeURIComponent(clips[0]);
    $('status').textContent = `${completed} of ${total} responses saved. Listen before rating.`;
  } else {
    $('audio').removeAttribute('src');
    $('audio').load();
    $('status').textContent = `Finished: ${completed} responses saved. Export your CSV below.`;
  }
}
$('start-form').addEventListener('submit', async event => {
  event.preventDefault();
  if (busy) return;
  busy = true;
  $('error').textContent = '';
  try {
    const id = $('rater').value.trim();
    const data = await request('/api/session?rater_id=' + encodeURIComponent(id));
    rater = id; clips = data.clips; total = data.total; completed = data.completed;
    $('start-form').hidden = true;
    $('identity').hidden = false;
    $('identity').textContent = 'Rater: ' + rater;
    $('export').hidden = false;
    $('export').href = '/export?rater_id=' + encodeURIComponent(rater);
    showClip();
  } catch (error) { $('error').textContent = error.message; }
  finally { busy = false; }
});
$('audio').addEventListener('playing', () => {
  played = true;
  $('save').disabled = busy;
});
$('audio').addEventListener('error', () => {
  if (clips.length) {
    played = false; $('save').disabled = true;
    $('error').textContent = 'Audio could not play. Check the recording, or mark unable to rate.';
  }
});
async function save(status) {
  if (busy || !clips.length || (status === 'rated' && !played)) return;
  busy = true;
  $('save').disabled = true; $('unrateable').disabled = true;
  $('error').textContent = '';
  try {
    const selected = document.querySelector('input[name="score"]:checked');
    if (status === 'rated' && !selected) throw new Error('Select a score from 1 to 5.');
    await request('/api/rating', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({clip_id: clips[0], rater_id: rater,
        pvc_score: status === 'rated' ? Number(selected.value) : null,
        notes: $('notes').value, rating_status: status})
    });
    clips.shift(); completed++; showClip();
  } catch (error) {
    $('error').textContent = error.message + ' Your current response is still on screen; retry or reload to resume.';
  } finally {
    busy = false; $('save').disabled = !played; $('unrateable').disabled = false;
  }
}
$('rating-form').addEventListener('submit', event => { event.preventDefault(); save('rated'); });
$('unrateable').addEventListener('click', () => save('unrateable'));
window.addEventListener('beforeunload', event => {
  if (busy || $('notes').value || document.querySelector('input[name="score"]:checked')) {
    event.preventDefault(); event.returnValue = '';
  }
});
