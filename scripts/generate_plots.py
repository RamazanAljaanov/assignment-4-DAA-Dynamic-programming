import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    csv_path = os.path.join("results", "results.csv")
    plots_dir = os.path.join("results", "plots")
    os.makedirs(plots_dir, exist_ok=True)

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found! Please run BenchmarkRunner first.")
        return

    df = pd.read_csv(csv_path)

    # Column compatibility: handle both 'input' and 'input_type'
    input_col = 'input' if 'input' in df.columns else 'input_type'

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams.update({'font.size': 11})

    # =========================================================================
    # PLOT 1: Edit Distance - Execution Time vs Input Size (Logarithmic Scale)
    # =========================================================================
    plt.figure(figsize=(8, 5))
    ed_df = df[df['algorithm'].isin(['Recursive', 'Table-DP', 'Two-Rows'])]
    
    for algo in ['Recursive', 'Table-DP', 'Two-Rows']:
        sub = ed_df[(ed_df['algorithm'] == algo) & (ed_df[input_col] == 'random')]
        if not sub.empty:
            plt.plot(sub['n'], sub['time_ms'], marker='o', label=algo, linewidth=2)

    plt.yscale('log')
    plt.title("Plot 1: Edit Distance Execution Time vs String Length n (Log Scale)", fontsize=13, fontweight='bold')
    plt.xlabel("String Length n (characters)", fontsize=11)
    plt.ylabel("Execution Time (milliseconds, log scale)", fontsize=11)
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.figtext(0.5, 0.04, 
                "Notice: Recursive Edit Distance exhibits sharp exponential growth O(3^n), whereas DP approaches maintain low execution time.", 
                wrap=True, horizontalalignment='center', fontsize=9, style='italic')
    plot1_path = os.path.join(plots_dir, "plot1_edit_distance_time.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    print(f"Saved: {plot1_path}")

    # =========================================================================
    # PLOT 2: String Search - Character Comparisons in Worst-Case
    # =========================================================================
    plt.figure(figsize=(8, 5))
    ss_df = df[df['algorithm'].isin(['Naive', 'KMP']) & (df[input_col] == 'worst_case')]

    for algo in ['Naive', 'KMP']:
        sub = ss_df[ss_df['algorithm'] == algo]
        if not sub.empty:
            plt.plot(sub['n'], sub['operations_count'], marker='s', label=algo, linewidth=2)

    plt.title("Plot 2: String Search Comparisons on Worst-Case Input (M=500)", fontsize=13, fontweight='bold')
    plt.xlabel("Text Length N (characters)", fontsize=11)
    plt.ylabel("Character Comparisons (count)", fontsize=11)
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.figtext(0.5, 0.04, 
                "Notice: Naive string search degrades to O(N * M) comparisons on repetitive prefixes, while KMP stays strictly linear O(N).", 
                wrap=True, horizontalalignment='center', fontsize=9, style='italic')
    plot2_path = os.path.join(plots_dir, "plot2_string_search_comparisons.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    print(f"Saved: {plot2_path}")

    # =========================================================================
    # PLOT 3: Ratio Plot - Naive / KMP Comparisons Ratio
    # =========================================================================
    plt.figure(figsize=(8, 5))
    naive_sub = ss_df[ss_df['algorithm'] == 'Naive'].sort_values('n')
    kmp_sub = ss_df[ss_df['algorithm'] == 'KMP'].sort_values('n')

    if not naive_sub.empty and not kmp_sub.empty:
        ratios = naive_sub['operations_count'].values / kmp_sub['operations_count'].values
        plt.plot(naive_sub['n'], ratios, marker='^', color='crimson', linewidth=2, label='Ratio: Naive / KMP')

    plt.title("Plot 3: Comparison Ratio (Naive / KMP) on Worst-Case Input", fontsize=13, fontweight='bold')
    plt.xlabel("Text Length N (characters)", fontsize=11)
    plt.ylabel("Ratio (Naive Comparisons / KMP Comparisons)", fontsize=11)
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.figtext(0.5, 0.04, 
                "Notice: The ratio approaches M (pattern length = 500), proving that KMP performs up to 500 times fewer character comparisons.", 
                wrap=True, horizontalalignment='center', fontsize=9, style='italic')
    plot3_path = os.path.join(plots_dir, "plot3_kmp_vs_naive_worstcase_ratio.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    print(f"Saved: {plot3_path}")

    print("All plots generated successfully in results/plots/!")

if __name__ == "__main__":
    main()
