## Source code 3

## What is Sec_pr_calculator?

Sec_pr_calculator is a program designed to calculate the Nakamoto Security Matrix and Security Probability based on the decentralization parameter `s`.

## How to Use

`node10_T600s005` calculates values at `s = 0.05` intervals, while `node10_T600s0025` calculates values at `s = 0.025` intervals. Below is a guide on how to use `node10_T600s0025`.

```bash
cd node10_T600s0025
chmod +x run_all.sh
./run_all.sh
```

This will generate a graph of the Security Probability at p = 0.3, both with and without considering the impact of stale blocks. Following this, the Nakamoto Security Matrix will be displayed. The Nakamoto Security Matrix is more visually comprehensible in node10_T600s005. You can also see graphs for other probabilities by adjusting the p parameter in sucRate_vs_s.py.
