#!/bin/bash

# コンパイルと実行の一連の流れを順に行うスクリプト

# Step 1: Compile and run att_suc_checker
g++ -std=c++11 -o att_suc_checker.out att_suc_checker.cpp
if [ $? -eq 0 ]; then
    echo "Successfully compiled att_suc_checker.cpp"
    ./att_suc_checker.out
else
    echo "Failed to compile att_suc_checker.cpp"
    exit 1
fi

# Step 2: Compile and run att_success_summary
g++ -std=c++11 -o att_success_summary.out att_success_summary.cpp
if [ $? -eq 0 ]; then
    echo "Successfully compiled att_success_summary.cpp"
    ./att_success_summary.out
else
    echo "Failed to compile att_success_summary.cpp"
    exit 1
fi

# Step 3: Compile and run pr_binominal
g++ -std=c++11 -o pr_binominal.out pr_binominal.cpp
if [ $? -eq 0 ]; then
    echo "Successfully compiled pr_binominal.cpp"
    ./pr_binominal.out
else
    echo "Failed to compile pr_binominal.cpp"
    exit 1
fi

# Step 4: Run the Python scripts
python3 sucRate_vs_s.py
if [ $? -eq 0 ]; then
    echo "Successfully executed sucRate_vs_s.py"
else
    echo "Failed to execute sucRate_vs_s.py"
    exit 1
fi

python3 nakamoto_sec_matrix.py
if [ $? -eq 0 ]; then
    echo "Successfully executed nakamoto_sec_matrix.py"
else
    echo "Failed to execute nakamoto_sec_matrix.py"
    exit 1
fi

# Step 5: Remove all .out files
echo "Cleaning up .out files..."
rm -f att_suc_checker.out att_success_summary.out pr_binominal.out
if [ $? -eq 0 ]; then
    echo "Successfully removed .out files"
else
    echo "Failed to remove .out files"
    exit 1
fi
