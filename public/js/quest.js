// ── QUEST SHARED LOGIC ──

// Progress tracking via localStorage
const Quest = {
  getProgress() {
    try { return JSON.parse(localStorage.getItem('nms_easter_progress') || '{}'); }
    catch { return {}; }
  },
  saveProgress(data) {
    const p = this.getProgress();
    Object.assign(p, data);
    localStorage.setItem('nms_easter_progress', JSON.stringify(p));
  },
  markComplete(stop) {
    this.saveProgress({ [`stop${stop}_complete`]: true, lastStop: stop });
  },
  isComplete(stop) {
    return !!this.getProgress()[`stop${stop}_complete`];
  }
};

// Reveal riddle after puzzle complete
function revealRiddle(stopNum) {
  Quest.markComplete(stopNum);
  const riddlePanel = document.getElementById('riddle-section');
  const collectPanel = document.getElementById('collect-section');
  const puzzlePanel = document.getElementById('puzzle-section');

  if (puzzlePanel) {
    puzzlePanel.style.opacity = '0.4';
    puzzlePanel.style.pointerEvents = 'none';
  }

  if (riddlePanel) {
    riddlePanel.classList.remove('hidden');
    riddlePanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  if (collectPanel) {
    collectPanel.classList.remove('hidden');
  }

  // Play a soft sound cue via AudioContext
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.frequency.setValueAtTime(523, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1047, ctx.currentTime + 0.3);
    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.5);
    osc.start(); osc.stop(ctx.currentTime + 1.5);
  } catch(e) {}
}

// Answer checking helper
function checkAnswer(inputId, correctAnswers, stopNum) {
  const raw = document.getElementById(inputId).value.trim().toLowerCase();
  const correct = correctAnswers.some(a => raw.includes(a.toLowerCase()));
  const fb = document.getElementById('answer-feedback');
  if (correct) {
    fb.className = 'feedback correct';
    fb.textContent = '✦ SEQUENCE CONFIRMED — ATLAS ACKNOWLEDGES ✦';
    document.getElementById('answer-feedback').style.display = 'block';
    setTimeout(() => revealRiddle(stopNum), 800);
  } else {
    fb.className = 'feedback wrong';
    fb.textContent = '✦ SIGNAL REJECTED — RECALIBRATE AND TRY AGAIN ✦';
    fb.style.display = 'block';
  }
}

// Multiple choice helper
function choiceCheck(btn, isCorrect, stopNum) {
  const allBtns = document.querySelectorAll('.choice-btn');
  allBtns.forEach(b => b.classList.remove('selected', 'wrong-choice'));
  if (isCorrect) {
    btn.classList.add('selected');
    const fb = document.getElementById('answer-feedback');
    fb.className = 'feedback correct';
    fb.textContent = '✦ SEQUENCE CONFIRMED — ATLAS ACKNOWLEDGES ✦';
    fb.style.display = 'block';
    setTimeout(() => revealRiddle(stopNum), 900);
  } else {
    btn.classList.add('wrong-choice');
    const fb = document.getElementById('answer-feedback');
    fb.className = 'feedback wrong';
    fb.textContent = '✦ SIGNAL REJECTED — RECALIBRATE AND TRY AGAIN ✦';
    fb.style.display = 'block';
  }
}

// Sequence drag-and-drop (simple touch-friendly version)
function initSequence(containerId, correctOrder, stopNum) {
  const list = document.getElementById(containerId);
  if (!list) return;

  let dragging = null;
  let touchItem = null;
  let touchStartY = 0;
  let clone = null;

  list.querySelectorAll('.sequence-item').forEach(item => {
    // Touch
    item.addEventListener('touchstart', e => {
      dragging = item;
      touchStartY = e.touches[0].clientY;
      clone = item.cloneNode(true);
      clone.style.cssText = `position:fixed;opacity:0.7;pointer-events:none;z-index:9999;width:${item.offsetWidth}px;left:${item.getBoundingClientRect().left}px;top:${item.getBoundingClientRect().top}px;`;
      document.body.appendChild(clone);
    }, { passive: true });

    item.addEventListener('touchmove', e => {
      if (!clone) return;
      const dy = e.touches[0].clientY - touchStartY;
      clone.style.top = (parseInt(clone.style.top) + dy) + 'px';
      touchStartY = e.touches[0].clientY;

      const target = document.elementFromPoint(e.touches[0].clientX, e.touches[0].clientY);
      if (target && target.classList.contains('sequence-item') && target !== dragging) {
        const rect = target.getBoundingClientRect();
        const mid = rect.top + rect.height / 2;
        if (e.touches[0].clientY < mid) {
          list.insertBefore(dragging, target);
        } else {
          list.insertBefore(dragging, target.nextSibling);
        }
      }
    }, { passive: true });

    item.addEventListener('touchend', () => {
      if (clone) { clone.remove(); clone = null; }
      dragging = null;
    });

    // Mouse
    item.addEventListener('dragstart', e => { dragging = item; setTimeout(() => item.style.opacity='0.3',0); });
    item.addEventListener('dragend', () => { item.style.opacity='1'; dragging = null; });
    item.addEventListener('dragover', e => { e.preventDefault(); });
    item.addEventListener('drop', e => {
      e.preventDefault();
      if (dragging && dragging !== item) {
        const rect = item.getBoundingClientRect();
        const mid = rect.top + rect.height / 2;
        if (e.clientY < mid) list.insertBefore(dragging, item);
        else list.insertBefore(dragging, item.nextSibling);
      }
    });
    item.setAttribute('draggable', true);
  });

  document.getElementById(`check-seq-${containerId}`)?.addEventListener('click', () => {
    const items = [...list.querySelectorAll('.sequence-item')].map(i => i.dataset.val);
    const correct = JSON.stringify(items) === JSON.stringify(correctOrder);
    const fb = document.getElementById('answer-feedback');
    if (correct) {
      fb.className = 'feedback correct';
      fb.textContent = '✦ SEQUENCE CONFIRMED — ATLAS ACKNOWLEDGES ✦';
      fb.style.display = 'block';
      setTimeout(() => revealRiddle(stopNum), 900);
    } else {
      fb.className = 'feedback wrong';
      fb.textContent = '✦ SIGNAL REJECTED — RECALIBRATE AND TRY AGAIN ✦';
      fb.style.display = 'block';
    }
  });
}
