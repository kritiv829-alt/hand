/**
 * True for null, undefined, empty strings, empty arrays, and objects with no own keys.
 */
function isEmpty(value) {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string' || Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
}

function clone(value) {
  return structuredClone(value);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function capitalize(text) {
  if (typeof text !== 'string' || text.length === 0) return '';
  return text[0].toUpperCase() + text.slice(1);
}

function merge(...sources) {
  return Object.assign({}, ...sources);
}

function unique(items) {
  return [...new Set(items)];
}

function parseBool(value, fallback = false) {
  if (typeof value === 'boolean') return value;
  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'on'].includes(normalized)) return true;
  if (['false', '0', 'no', 'off'].includes(normalized)) return false;
  return fallback;
}

function sum(numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

function daysBetween(a, b) {
  const start = new Date(a);
  const end = new Date(b);
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    throw new TypeError('daysBetween expects two valid dates');
  }
  return Math.abs(end - start) / (24 * 60 * 60 * 1000);
}

async function retry(fn, { times = 3, delayMs = 0 } = {}) {
  let lastError;
  for (let attempt = 1; attempt <= times; attempt++) {
    try {
      return await fn(attempt);
    } catch (err) {
      lastError = err;
      if (attempt < times && delayMs > 0) await sleep(delayMs);
    }
  }
  throw lastError;
}

function getNested(obj, keyPath, fallback) {
  const keys = Array.isArray(keyPath) ? keyPath : String(keyPath).split('.');
  let current = obj;
  for (const key of keys) {
    if (current === null || current === undefined) return fallback;
    current = current[key];
  }
  return current === undefined ? fallback : current;
}

module.exports = {
  isEmpty,
  clone,
  sleep,
  randomInt,
  capitalize,
  merge,
  unique,
  parseBool,
  sum,
  daysBetween,
  retry,
  getNested,
};
