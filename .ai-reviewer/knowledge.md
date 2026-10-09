# hand reviewer notes

## Architecture

This is a dependency-free Node.js URL shortener named `shortie`, using the built-in `http`, filesystem, and crypto APIs. `src/server.js` composes route handlers for static files, API endpoints, and redirects around `Shortener`, which persists link records through the file-backed `Store`. The browser client is in `public/`; `src/scripts/report.py` is a separate reporting utility for the same JSON data.

## Conventions

- Use CommonJS modules and explicit dependency injection. Services export classes (`src/services/store.js`, `src/services/shortener.js`), while routes export handler factories such as `apiRoutes(shortener, baseUrl)`.
- Route handlers use a boolean dispatch contract: return `false` when they do not own a request and otherwise send the response and return `true` (`src/routes/api.js`, `src/routes/redirect.js`, `src/routes/static.js`).
- Keep HTTP concerns in routes and business rules in `Shortener`. URL validation and code validation belong in `src/utils/validate.js`; code generation belongs in `src/utils/codegen.js`.
- Link records consistently contain `url`, `hits`, and `createdAt`; APIs add `code` when returning records (`src/services/shortener.js`, `src/routes/api.js`).
- Persistence is JSON-file based and synchronous. `Store.save()` and `Analytics.save()` create parent directories before writing formatted JSON (`src/services/store.js`, `src/services/analytics.js`).
- Configuration is centralized in `src/config.js`, with environment overrides for `PORT`, `HOST`, and `DATA_FILE`; use `config.codeLength` rather than hard-coding generated code length.
- Short codes are generated from the project alphabet in `src/utils/codegen.js` and must be checked for collisions before storage (`src/services/shortener.js`).
- API errors are JSON objects shaped as `{ error: string }`, and successful shorten requests return HTTP 201 (`src/routes/api.js`).
- Frontend DOM text is assigned with `textContent`, not HTML interpolation (`public/app.js`).

## Intentional non-standard choices

- This intentionally has no npm dependencies; use Node built-ins rather than adding a framework (`package.json`, `README.md`).
- File I/O is deliberately synchronous and writes directly to JSON files, appropriate to this small utility rather than a database-backed service (`src/services/store.js`, `src/services/analytics.js`).
- `src/services/analytics.js` tracks visitor IPs and user agents in arrays and is separate from the primary link hit counter; do not assume analytics data is part of `data/links.json`.

## Watch out for

- `src/routes/admin.js` defines protected admin operations, but `src/server.js` does not import or register `adminRoutes`; changes relying on `/admin/*` will currently be unreachable.
- Preserve validation before redirects, stats, and admin mutations. Codes must pass `isValidCode`; destinations must pass `isValidUrl`.
- Do not bypass `Store.set()` or `Store.save()` after mutations, or changes will remain only in memory (`src/services/store.js`).
- Be careful when changing route order in `src/server.js`: static assets and API paths must be handled before the catch-all short-code redirect.
- Admin file import/export must continue using `safeDataPath()`; never accept arbitrary filesystem paths from query parameters (`src/routes/admin.js`).
