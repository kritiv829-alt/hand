const test = require('node:test');
const assert = require('node:assert');
const os = require('os');
const path = require('path');
const fs = require('fs');
const Store = require('../src/services/store');
const Shortener = require('../src/services/shortener');

function tempStore() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shortie-'));
  return new Store(path.join(dir, 'links.json'));
}

test('shortens and resolves a URL', () => {
  const shortener = new Shortener(tempStore());
  const link = shortener.shorten('https://example.com');
  assert.equal(link.code.length, 6);
  assert.equal(shortener.resolve(link.code), 'https://example.com');
  assert.equal(shortener.stats(link.code).hits, 1);
});

test('throws on invalid URL', () => {
  const shortener = new Shortener(tempStore());
  assert.throws(() => shortener.shorten('nope'), /Invalid URL/);
});

test('returns null for unknown code', () => {
  const shortener = new Shortener(tempStore());
  assert.equal(shortener.resolve('zzzzzz'), null);
});

test('persists across store reloads', () => {
  const store = tempStore();
  const link = new Shortener(store).shorten('https://example.org');
  const reloaded = new Store(store.file);
  assert.equal(reloaded.get(link.code).url, 'https://example.org');
});
