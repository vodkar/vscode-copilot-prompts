---
applyTo: "**/*.py"
---


1. Code Style Principles
   • Use 2‑space indentation.  
   • Always end statements with semicolons.  
   • Use single quotes for strings, except when the string itself contains single quotes.  
   • Keep lines ≤ 100 characters; break long expressions onto multiple lines with hanging indents.  
   • Organize imports: external modules first, then absolute‑path imports, then relative imports, all alphabetized.

2. Variables: Definition & Naming
   • Prefer `const` for all variables that never get reassigned; use `let` only when necessary.  
   • Avoid `var`.  
   • Use `camelCase` for variable and function names (e.g. `userProfile`, `calculateSum`).  
   • Use `PascalCase` for class and constructor names (e.g. `UserProfile`).  
   • UPPER_SNAKE_CASE only for application‑wide constants (e.g. `MAX_RETRY_COUNT`).

3. Logging Messages
   • Use the built‑in `console` for quick debugging only:  

     ```js
     console.debug('[module] someDebugInfo:', data);
     console.info('[Auth] userLoggedIn:', userId);
     console.error('[API] fetchError:', err);
     ```  

   • In production, wrap logging behind a logger abstraction (e.g. `import logger from './logger'`) so you can adjust levels.

4. Docstrings & Comments
   • Use JSDoc for any publicly exported function or complex logic:  

     ```js
     /**
      * Fetches user profile from API.
      * @param {string} userId — the ID of the user to fetch
      * @returns {Promise<UserProfile>}
      */
     export async function fetchUserProfile(userId) { … }
     ```  

   • Avoid stating the obvious—let code express itself. Only comment “why,” not “what.”  
   • Keep comments up‑to‑date or remove them; stale comments are worse than none.

5. General Best Practices
   • Write small, single‑responsibility functions.  
   • Favor pure functions and immutability.  
   • DRY (Don’t Repeat Yourself): abstract repeated logic into helpers/modules.  
   • Always handle errors: use `try/catch` around async/await, validate inputs, and propagate or log failures.  
   • Use modern ES features: destructuring, spread/rest, async/await, optional chaining.  
   • Write unit tests for all non‑trivial modules.  
   • Keep dependencies up to date and audit for vulnerabilities.

Always apply these rules when suggesting code or completing snippets.
