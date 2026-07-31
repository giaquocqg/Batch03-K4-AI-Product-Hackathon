(function attachRecallSession(root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.RecallSession = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, () => {
  function create(questionCount) {
    if (!Number.isInteger(questionCount) || questionCount < 1) {
      throw new Error('questionCount must be a positive integer.');
    }
    return {
      queue: Array.from({ length: questionCount }, (_, index) => index),
      attempts: Array(questionCount).fill(0),
      firstCorrect: new Set(),
      mastered: new Set(),
      retryCount: 0,
    };
  }

  function stats(session) {
    const firstAttempts = session.attempts.filter((count) => count > 0).length;
    const firstCorrect = session.firstCorrect.size;
    return {
      total: session.attempts.length,
      firstAttempts,
      firstCorrect,
      mastered: session.mastered.size,
      retryCount: session.retryCount,
      firstRate: firstAttempts ? Math.round((firstCorrect / firstAttempts) * 100) : null,
    };
  }

  function record(session, questionIndex, remembered) {
    const currentQuestion = session.queue.shift();
    if (currentQuestion !== questionIndex) {
      throw new Error('Only the visible question can be recorded.');
    }
    const isFirstAttempt = session.attempts[questionIndex] === 0;
    session.attempts[questionIndex] += 1;
    if (remembered) {
      if (isFirstAttempt) session.firstCorrect.add(questionIndex);
      session.mastered.add(questionIndex);
      return session;
    }

    session.retryCount += 1;
    // A miss is shown after one other queued question. If there is no other
    // question left, it is shown immediately rather than being dropped.
    const retryPosition = session.queue.length > 0 ? 1 : 0;
    session.queue.splice(retryPosition, 0, questionIndex);
    return session;
  }

  return { create, record, stats };
}));
