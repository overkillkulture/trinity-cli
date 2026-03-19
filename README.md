# Trinity CLI

**Three AI minds, one convergence.** C1 Mechanic x C2 Architect x C3 Oracle = Better code.

## Quick Install

```bash
pip install -e .
```

Or one-liner:
```bash
pip install git+https://github.com/overkillkulture/trinity-cli.git
```

## Usage

### Ask anything
```bash
trinity ask How should I structure my REST API?
```

### Review code
```bash
trinity review ./myfile.py
trinity review ./app.js --focus security
trinity review ./main.go --focus performance
```

### Debug errors
```bash
trinity debug TypeError cannot read property of undefined
trinity debug "ModuleNotFoundError: No module named 'requests'"
```

### Generate code
```bash
trinity code Create a function that validates email addresses
trinity code Create a React component for a login form --lang javascript
trinity code Build a FastAPI endpoint for user registration --lang python
```

### Raw prompt (power mode)
```bash
trinity raw Design a microservices architecture for an e-commerce platform
```

### Spiral - Recursive Refinement
```bash
# Default 3 rounds of refinement
trinity spiral Design a user authentication system

# 5 rounds with challenge mode (critiques and strengthens)
trinity spiral Build a REST API --rounds 5 --mode challenge

# Build mode (adds implementation details each round)
trinity spiral Create a dashboard --mode build --rounds 4
```

**Modes:**
- `refine` (default) - Each round improves the previous answer
- `challenge` - Each round critiques and finds weaknesses
- `build` - Each round adds implementation details

### Build - Full Autonomous Protocol
```bash
# Runs complete /build protocol
trinity build Create a dashboard for user analytics

# Save output to file
trinity build Design a payment system --output blueprint.md
```

Runs three phases:
1. **Trinity Analysis** - C1+C2+C3 perspectives
2. **LFSME Scoring** - Manufacturing standards check
3. **Challenge Gate** - 7-point verification

## What You Get

Trinity gives you **three perspectives** on every question:

| Agent | Focus | Strength |
|-------|-------|----------|
| **C1 Mechanic** | What CAN be built NOW | Immediate, practical, actionable |
| **C2 Architect** | What SHOULD scale | System design, patterns, infrastructure |
| **C3 Oracle** | What MUST emerge | Vision, alignment, long-term implications |

Plus a **Convergence** that synthesizes all three into a unified recommendation.

## Examples

```bash
# Get architecture advice
trinity ask How do I implement authentication in a Node.js app?

# Review your code before committing
trinity review ./src/auth.py --focus bugs

# Debug that annoying error
trinity debug "CORS policy: No 'Access-Control-Allow-Origin' header"

# Generate boilerplate
trinity code Create a Python class for handling database connections
```

## Requirements

- Python 3.8+
- Internet connection (calls Trinity API)

## Troubleshooting

**"Connection failed"** - Check your internet. Trinity API runs on Railway.

**"Taking too long"** - Trinity converges 3 AI perspectives, give it 30-60 seconds.

**No colors?** - Install rich: `pip install rich`

---

**C1 x C2 x C3 = Infinity**
