# Forward vs Backward Analysis: Impact Direction Comparison

## Quick Answer to Your Question

**"What is the entire economic impact of 철강 in 경남 to the entire country?"**

This means: **Forward Analysis** - Where do steel outputs from Gyeongnam flow to?

## Visual Comparison

### FORWARD Analysis (Current config.json)
```
철강 (경남) → All Sectors (All Regions)
                  ↓
        "What sectors use our steel?"
```

**Configuration:**
```json
{
  "filters": {
    "output_sectors": ["1200"],    // Steel
    "output_region": "경남",       // Gyeongnam
    "input_region": null,           // All regions
    "input_sectors": null           // All sectors
  },
  "analysis": {
    "direction": "forward"
  }
}
```

**What you get:**
- Iron ore from 강원 → Steel in 경남 (0.2 coefficient)
- Coal from 강원 → Steel in 경남 (0.15 coefficient)
- Electricity from 경북 → Steel in 경남 (0.3 coefficient)
- Labor from 경남 → Steel in 경남 (0.25 coefficient)

**Economic Impact (with 1M KRW):**
- Need 200K KRW of iron ore (0.2 × 1M)
- Need 150K KRW of coal (0.15 × 1M)
- Need 300K KRW of electricity (0.3 × 1M)
- Total upstream impact: 650K KRW to supply steel production

---

### BACKWARD Analysis (Previous config)
```
All Sectors (All Regions) → 철강 (경남)
                ↓
    "Which sectors buy our steel?"
```

**Configuration:**
```json
{
  "filters": {
    "input_sectors": ["1200"],    // Steel
    "input_region": "경남",       // Gyeongnam
    "output_region": null,         // All regions
    "output_sectors": null         // All sectors
  },
  "analysis": {
    "direction": "backward"
  }
}
```

**What you get:**
- Steel (경남) → Automobiles (경남) (0.3 coefficient)
- Steel (경남) → Construction (서울) (0.2 coefficient)
- Steel (경남) → Machinery (경기) (0.25 coefficient)
- Steel (경남) → Shipbuilding (경남) (0.4 coefficient)

**Economic Impact (with 1M KRW):**
- Automobiles need 300K KRW of steel (0.3 × 1M)
- Construction needs 200K KRW of steel (0.2 × 1M)
- Machinery needs 250K KRW of steel (0.25 × 1M)
- Total downstream impact: 2.15M KRW to using sectors

---

## Conceptual Difference

| Aspect | FORWARD (What you want) | BACKWARD |
|--------|------------------------|----------|
| **Supply Chain** | Upstream | Downstream |
| **Question** | "What does 철강 need?" | "What needs 철강?" |
| **Sectors shown** | Input suppliers | Output customers |
| **Regions** | All regions supply 경남 | 경남 supplies all regions |
| **Use case** | Production dependency analysis | Market impact analysis |
| **Total Impact** | Cost to produce steel | Revenue from steel sales |

## Real-World Example

Imagine Gyeongnam Steel increases production by 1 million KRW:

**FORWARD (Production needs):**
- "We need more iron ore, coal, electricity, labor to produce this extra steel"
- Shows suppliers across the country
- Economic ripple: Supply chain expands
- Total impact = 650K KRW (to suppliers)

**BACKWARD (Market impact):**
- "Automobile, construction, and machinery factories need our extra steel"
- Shows customers across the country
- Economic ripple: Demand chain expands
- Total impact = 2.15M KRW (from customers)

## Complete Economic Impact Calculation

To get the **ENTIRE ECONOMIC IMPACT** including all multiplier effects:

### Step 1: Primary Effect (Direct)
```
Gyeongnam Steel Output = 1,000,000 KRW
```

### Step 2: Downstream Effect (Forward)
```
Which sectors use this steel?
- Automobiles: 300K KRW
- Construction: 200K KRW
- Machinery: 250K KRW
- Shipbuilding: 400K KRW
Total downstream: 1,150K KRW
```

### Step 3: Upstream Effect (Backward)
```
What do these steel-using sectors need from other sectors?
- Automobiles need aluminum: 150K KRW
- Construction needs cement: 100K KRW
- Machinery needs electronics: 200K KRW
(This requires another round of analysis)
Total upstream of downstream: 450K KRW
```

### Total Multiplier Effect
```
Direct (Steel) = 1,000K KRW
+ Downstream (Steel users) = 1,150K KRW
+ Upstream (Input suppliers) = 650K KRW
+ Higher order effects = [requires iterative analysis]
= Total Economic Impact
```

## How to Use Both Analyses

### Scenario 1: Analyze Current Setup (Forward)
```bash
# Current config.json is already set to forward
python3 main.py
python3 calculate_impact.py
```

**Output:** "To produce 1M KRW of steel in Gyeongnam, we need 650K KRW of inputs across all regions"

### Scenario 2: Switch to Backward Analysis
```bash
# Edit config.json: change output_sectors to input_sectors, etc.
# Or create a separate config file:
cp config.json config_backward.json
# Edit config_backward.json and run:
python3 main.py
python3 calculate_impact.py direction=backward
```

**Output:** "1M KRW of steel from Gyeongnam serves 2.15M KRW of output sectors"

### Scenario 3: Compare Both Directions
```bash
# Run main.py with direction: "both" in config.json
# This creates both forward_analysis.csv and backward_analysis.csv
```

## Updated Workflow

```bash
# 1. Run analysis (uses forward by default now)
python3 main.py
# Output: forward_analysis.csv (suppliers), backward_analysis.csv (customers)

# 2. Calculate impact
python3 calculate_impact.py
# With forward: shows input needs
# Can change to backward for customer impact

# 3. View results
cat analysis_results/economic_impact.csv
```

## Summary

Your question: **"Economic impact of 철강 (경남) to entire country"**

✅ **Answer: Use FORWARD Analysis** (current config)
- Shows: Which sectors supply inputs to steel in Gyeongnam
- All 경남 steel production relies on inputs from all regions
- Economic multiplier: Input supply chain across country

If you also want to know: **"Economic impact when Gyeongnam steel is used"**

✅ **Use BACKWARD Analysis** (switch config)
- Shows: Which sectors consume steel from Gyeongnam
- All sectors using 경남 steel across the country
- Economic multiplier: Output customer chain across country

**For complete economic impact analysis, you typically use BOTH directions and calculate the multiplier effects.**
