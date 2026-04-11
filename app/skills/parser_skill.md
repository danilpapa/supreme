# Parser Skill

Purpose:
- fetch the web page
- strip HTML noise
- return title, excerpt, and clean text

Failure modes:
- JS-heavy page returns little content
- anti-bot protection blocks parsing
- malformed HTML mixes navigation with article body

Mitigation:
- record parsing errors
- add fallback parser later, such as `trafilatura` or `newspaper3k`
