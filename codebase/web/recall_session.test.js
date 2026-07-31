const assert = require('node:assert/strict');
const test = require('node:test');
const RecallSession = require('./recall_session.js');

test('a missed question returns after exactly one other question', () => {
  const session = RecallSession.create(4);
  RecallSession.record(session, 0, false);
  assert.deepEqual(session.queue, [1, 0, 2, 3]);

  RecallSession.record(session, 1, true);
  assert.deepEqual(session.queue, [0, 2, 3]);
});

test('a retry can be mastered without inflating first-try score', () => {
  const session = RecallSession.create(2);
  RecallSession.record(session, 0, false);
  RecallSession.record(session, 1, true);
  RecallSession.record(session, 0, true);

  assert.equal(session.mastered.size, 2);
  assert.equal(session.firstCorrect.size, 1);
  assert.equal(session.retryCount, 1);
  assert.equal(RecallSession.stats(session).firstRate, 50);
});

test('a final missed question is not silently dropped', () => {
  const session = RecallSession.create(1);
  RecallSession.record(session, 0, false);
  assert.deepEqual(session.queue, [0]);
});
