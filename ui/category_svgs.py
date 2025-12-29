"""Inline SVG icons for emoji category buttons (used in the emoji picker UI)."""

from __future__ import annotations

CATEGORY_SVGS: dict[str, str] = {
    "Smileys": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <circle cx="12" cy="12" r="9"></circle>
  <path d="M8.3 14.2c1.2 1.6 2.6 2.4 3.7 2.4s2.5-.8 3.7-2.4"></path>
  <path d="M9 10h.01"></path>
  <path d="M15 10h.01"></path>
</svg>
    """.strip(),
    "Gestures": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M7 12V6a1.5 1.5 0 0 1 3 0v6"></path>
  <path d="M10 12V5a1.5 1.5 0 0 1 3 0v7"></path>
  <path d="M13 12V6a1.5 1.5 0 0 1 3 0v8"></path>
  <path d="M16 12.5V9.5a1.5 1.5 0 0 1 3 0V14c0 3-2 6-6 6H11c-2 0-4-1-5-3l-1-2"></path>
</svg>
    """.strip(),
    "Hearts": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M12 21s-7-4.5-9.5-9A5.7 5.7 0 0 1 12 5.5 5.7 5.7 0 0 1 21.5 12C19 16.5 12 21 12 21z"></path>
</svg>
    """.strip(),
    "Animals": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M7 14c-1.5 0-3 1.5-3 3s1.5 3 3 3c1.2 0 2.3-.8 2.8-1.9"></path>
  <path d="M17 14c1.5 0 3 1.5 3 3s-1.5 3-3 3c-1.2 0-2.3-.8-2.8-1.9"></path>
  <path d="M9.5 14.5c.7-.7 1.6-1.1 2.5-1.1s1.8.4 2.5 1.1"></path>
  <path d="M9 9.5c-.5-1.2-1.7-2-3-2-1.1 0-2 .9-2 2 0 1.3.8 2.5 2 3"></path>
  <path d="M15 9.5c.5-1.2 1.7-2 3-2 1.1 0 2 .9 2 2 0 1.3-.8 2.5-2 3"></path>
</svg>
    """.strip(),
    "Food": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M3 6h18"></path>
  <path d="M6 6l2 14h8l2-14"></path>
  <path d="M10 10h4"></path>
  <path d="M9.5 14h5"></path>
</svg>
    """.strip(),
    "Activities": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <circle cx="12" cy="12" r="9"></circle>
  <path d="M12 3v18"></path>
  <path d="M3 12h18"></path>
  <path d="M5.5 7.5c3 2 10 2 13 0"></path>
  <path d="M5.5 16.5c3-2 10-2 13 0"></path>
</svg>
    """.strip(),
    "Travel": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M2 16l20-8-20-8 5 8-5 8z"></path>
  <path d="M7 8h7"></path>
</svg>
    """.strip(),
    "Objects": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M9 18h6"></path>
  <path d="M10 22h4"></path>
  <path d="M8 14a6 6 0 1 1 8 0c-1 1-1.5 2-1.5 3H9.5c0-1-.5-2-1.5-3z"></path>
</svg>
    """.strip(),
    "Symbols": """
<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M12 2l2.2 6.7H21l-5.4 3.9 2.1 6.7L12 15.6 6.3 19.3l2.1-6.7L3 8.7h6.8L12 2z"></path>
</svg>
    """.strip(),
}


