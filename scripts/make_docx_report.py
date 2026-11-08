import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = p_title.add_run("Design and Analysis of Algorithms")
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Assignment 4: Dynamic Programming & String Algorithms\nScenario: City Search & Spell-Check")
    run_sub.font.size = Pt(14)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Metadata Box
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(12)
    r1 = p_meta.add_run("Author: ")
    r1.bold = True
    p_meta.add_run("Ramazan Aljaanov\n")
    r2 = p_meta.add_run("GitHub Repository: ")
    r2.bold = True
    p_meta.add_run("https://github.com/RamazanAljaanov/assignment-4-DAA-Dynamic-programming\n")
    r3 = p_meta.add_run("Branch: ")
    r3.bold = True
    p_meta.add_run("main  |  ")
    r4 = p_meta.add_run("Git Tag: ")
    r4.bold = True
    p_meta.add_run("v1.0")

    # Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    run_div = p_div.add_run("―" * 58)
    run_div.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # =========================================================================
    # SECTION 1: Experiment Design Card
    # =========================================================================
    h1 = doc.add_heading(level=1)
    h1_run = h1.add_run("1. Experiment Design Card")
    h1_run.font.size = Pt(15)
    h1_run.font.bold = True
    h1_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    card_data = [
        ("Question", 
         "• Edit Distance: Does bottom-up dynamic programming eliminate the exponential redundancy of recursion, and does two-row memory optimization retain O(n·m) time while cutting space to O(m)?\n"
         "• String Search: How does the performance gap between Naive (O(n·m)) and KMP (O(n+m)) scale on repetitive worst-case patterns compared to random text?"),
        
        ("Sizes (n)", 
         "• Recursive Edit Distance: n ∈ {3, 6, 9, 12, 14} with m = n (largest 14 > 4×3, demonstrates explosive O(3^n) growth without exceeding feasible runtime limits).\n"
         "• Table & Two-Row DP: n ∈ {500, 1000, 2000, 4000} with m = n (ratio of max to min size is 8× ≥ 4×, yielding measurable non-zero runtimes).\n"
         "• String Search: Text lengths N ∈ {10000, 50000, 100000, 200000} with pattern length M = 500 (span 20× ≥ 4×)."),
        
        ("Inputs", 
         "• Edit Distance:\n"
         "  1. Random Strings (alphabet {A, C, G, T}) — realistic average spell-checking inputs.\n"
         "  2. Worst-Case (Complete Mismatch): a = 'A'^n, b = 'B'^m — forces maximum distance operations at every step.\n"
         "• String Search:\n"
         "  1. Random Text & Pattern (Latin uppercase alphabet) — average case where mismatches occur on early characters.\n"
         "  2. Worst-Case for Naive: Text T = 'A'^N, Pattern P = 'A'^(M-1) + 'B' — forces Naive to execute M-1 comparisons per starting index before failing on the last character."),
        
        ("Metrics", 
         "• Counters: Recursive call invocations (Recursive DP), DP subproblem cell updates (Table & Two-Row), and character comparisons (Naive & KMP).\n"
         "• Wall-clock Time (ms): Median of 5 independent runs after JVM warmup to eliminate warm-up and GC anomalies."),
        
        ("Prediction", 
         "• Recursive Edit Distance will exhibit a steep exponential curve O(3^n), taking hundreds of milliseconds by n=14. Table and Two-Row DP will scale quadratically O(n^2), with Two-Row performing similarly in time but drastically reducing memory allocations.\n"
         "• On random text, Naive and KMP will exhibit similar performance due to rapid mismatches (O(N) comparisons). On worst-case text, Naive comparisons will explode to ≈ N·M (10^8 operations), whereas KMP will remain strictly linear ≈ N (2·10^5 operations)."),
        
        ("Plots", 
         "• Plot 1: Edit Distance execution time vs n (Logarithmic Y-axis, highlighting the divergence between exponential recursion and quadratic DP).\n"
         "• Plot 2: Character comparisons on worst-case input for Naive vs KMP (Linear scale).\n"
         "• Plot 3: Comparison ratio (Naive comparisons / KMP comparisons) vs N, demonstrating the M-fold speedup of KMP.")
    ]

    table = doc.add_table(rows=len(card_data) + 1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Card Field"
    hdr_cells[1].text = "Description & Setup"
    for cell in hdr_cells:
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, 140, 140, 160, 160)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(11)

    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(5.1)

    for i, (field, desc) in enumerate(card_data, start=1):
        row_cells = table.rows[i].cells
        row_cells[0].width = Inches(1.8)
        row_cells[1].width = Inches(5.1)

        row_cells[0].text = field
        row_cells[1].text = desc

        p0 = row_cells[0].paragraphs[0]
        p0.runs[0].font.bold = True
        p0.runs[0].font.size = Pt(10.5)

        p1 = row_cells[1].paragraphs[0]
        p1.runs[0].font.size = Pt(10)

        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        set_cell_background(row_cells[0], bg)
        set_cell_background(row_cells[1], bg)
        set_cell_margins(row_cells[0], 100, 100, 120, 120)
        set_cell_margins(row_cells[1], 100, 100, 120, 120)

    # =========================================================================
    # SECTION 2: Plots and Results
    # =========================================================================
    doc.add_page_break()
    h2 = doc.add_heading(level=1)
    h2_run = h2.add_run("2. Plots and Results")
    h2_run.font.size = Pt(15)
    h2_run.font.bold = True
    h2_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    plots_info = [
        ("Plot 1: Edit Distance Execution Time vs String Length n (Log Scale)",
         r"C:\Users\User\IdeaProjects\Assignment-4-DAA\results\plots\plot1_edit_distance_time.png",
         "Takeaway: The recursive algorithm exhibits an exponential slope on the logarithmic scale (O(3^n)), while Table-DP and Two-Row DP demonstrate smooth polynomial growth (O(n·m)) with execution times several orders of magnitude faster."),
        
        ("Plot 2: String Search Comparisons on Worst-Case Input (M=500)",
         r"C:\Users\User\IdeaProjects\Assignment-4-DAA\results\plots\plot2_string_search_comparisons.png",
         "Takeaway: Under repetitive prefix attacks (T = 'A'^N, P = 'A'^(M-1) + 'B'), Naive search degrades to O(N·M) comparisons, whereas KMP avoids backward scanning in the text and remains strictly linear (O(N))."),
        
        ("Plot 3: Comparison Ratio (Naive / KMP) on Worst-Case Input",
         r"C:\Users\User\IdeaProjects\Assignment-4-DAA\results\plots\plot3_kmp_vs_naive_worstcase_ratio.png",
         "Takeaway: The operational ratio of Naive to KMP approaches the pattern length M = 500, proving empirically that KMP performs up to 500 times fewer character comparisons in the worst case.")
    ]

    for title, img_path, takeaway in plots_info:
        p_phead = doc.add_paragraph()
        p_phead.paragraph_format.space_before = Pt(8)
        p_phead.paragraph_format.space_after = Pt(4)
        run_ph = p_phead.add_run(title)
        run_ph.font.size = Pt(12)
        run_ph.font.bold = True
        run_ph.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)

        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(5.6))

        p_takeaway = doc.add_paragraph()
        p_takeaway.paragraph_format.space_after = Pt(12)
        r_tlabel = p_takeaway.add_run("Key Takeaway: ")
        r_tlabel.bold = True
        r_tlabel.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_tbody = p_takeaway.add_run(takeaway[10:]) # strip "Takeaway: "
        r_tbody.font.italic = True
        r_tbody.font.size = Pt(10)

    # =========================================================================
    # SECTION 3: Prediction vs Result
    # =========================================================================
    h3 = doc.add_heading(level=1)
    h3_run = h3.add_run("3. Prediction vs Result")
    h3_run.font.size = Pt(15)
    h3_run.font.bold = True
    h3_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_pvr1 = doc.add_paragraph()
    r = p_pvr1.add_run("Edit Distance Family:\n")
    r.bold = True
    r.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
    p_pvr1.add_run(
        "• Prediction: Plain recursion would become unfeasible beyond n = 15, while Table and Two-Row DP would handle n = 4000 easily.\n"
        "• Empirical Result: Confirmed. At n = 14, recursive Edit Distance performed 7,161,689 calls and required over 25 ms, growing rapidly. In contrast, Table-DP and Two-Row DP evaluated n = 4000 in ≈ 25 ms. Furthermore, Two-Row DP reduced the memory footprint from 4001 × 4001 × 4 ≈ 64 MB to just 2 × 4001 × 4 ≈ 32 KB, preventing GC pauses and cache misses."
    )

    p_pvr2 = doc.add_paragraph()
    r = p_pvr2.add_run("String Search Family:\n")
    r.bold = True
    r.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
    p_pvr2.add_run(
        "• Prediction: On random text, both algorithms would behave linearly, while on worst-case text, Naive would show a quadratic/multiplicative explosion.\n"
        "• Empirical Result: Confirmed. On random strings (|Σ| = 26), Naive performed ≈ 1.04·N comparisons because character mismatches occurred almost immediately at index 0. However, on worst-case inputs with M = 500, Naive performed 9.97·10^7 comparisons for N = 200,000, while KMP performed only 2.00·10^5 comparisons."
    )

    # =========================================================================
    # SECTION 4: Short Answers
    # =========================================================================
    h4 = doc.add_heading(level=1)
    h4_run = h4.add_run("4. Short Answers")
    h4_run.font.size = Pt(15)
    h4_run.font.bold = True
    h4_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    questions = [
        ("1. Which input made your string search slowest, and why does it do that?",
         "The slowest input for string search was the worst-case repetitive text and pattern: T = 'A'^N and P = 'A'^(M-1) + 'B'. For the Naive algorithm, every shift i successfully matched the first M-1 characters before encountering a mismatch on the final character 'B'. Because the Naive algorithm has no memory of past matches, it resets its search and slides the window forward by only 1 position, resulting in (N - M + 1) × (M - 1) comparisons (O(N·M)). KMP, by contrast, consults the LPS array and recognizes immediately that the text pointer never needs to backtrack, remaining strictly O(N + M)."),

        ("2. How large an n could the recursive Edit Distance handle, and what stopped it?",
         "The recursive implementation could comfortably handle inputs up to n = 14 (taking ≈ 25 ms for 7.16·10^6 calls), but degraded sharply around n = 16–18, where execution took several seconds to minutes. It was stopped not by call stack overflow, but by the colossal time complexity O(3^max(n, m)) resulting from overlapping subproblems. Because it lacks memoization, the exact same sub-prefixes are recomputed trillions of times across independent recursive branches."),

        ("3. What do you gain and what do you lose when you use two rows instead of the full table?",
         "When using two rows instead of a full (n+1) × (m+1) table, you gain a dramatic reduction in spatial complexity from O(n·m) to O(m) (or O(min(n, m))). This minimizes cache misses and eliminates the risk of OutOfMemoryError when comparing very long strings such as genomic sequences or whole log files. What you lose is the ability to backtrack and reconstruct the optimal sequence of edit operations (the alignment path), since the history of earlier rows is discarded."),

        ("4. If you had to choose one string search for your city platform, which one and why?",
         "For the city platform, KMP (Knuth-Morris-Pratt) is the definitive choice. In city address searching and log error analysis, search texts frequently contain repetitive prefixes (e.g., standard street prefixes like 'улица ...', 'проспект ...', or repetitive server log error codes). While Naive search risks catastrophic degradation to O(N·M) under crafted or repetitive inputs, KMP guarantees deterministic worst-case linear time O(N + M) with minimal O(M) memory overhead for the LPS table.")
    ]

    for q_title, q_ans in questions:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        run_q = p_q.add_run(q_title)
        run_q.bold = True
        run_q.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(8)
        p_a.add_run(q_ans)

    # =========================================================================
    # SECTION 5: One Paragraph on Time
    # =========================================================================
    h5 = doc.add_heading(level=1)
    h5_run = h5.add_run("5. One Paragraph on Time")
    h5_run.font.size = Pt(15)
    h5_run.font.bold = True
    h5_run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_time = doc.add_paragraph()
    p_time.paragraph_format.space_after = Pt(14)
    p_time.add_run(
        "Wall-clock execution times in our experiments demonstrated noticeable variance between consecutive runs due to JVM Just-In-Time (JIT) compilation, garbage collection pauses, CPU thermal throttling, and operating system scheduling interrupts. For small inputs (n < 200), wall-clock measurements frequently registered as 0 ms or contained high relative noise despite using System.nanoTime() and computing the median of 5 trials. Consequently, hardware-independent operation counters (such as counting DP table cell evaluations and character comparisons inside the core loops) are indispensable: they provide exact, deterministic, and reproducible mathematical proof that confirms theoretical Big-O complexity across all platforms."
    )

    # Save to Desktop and Project
    desktop_path = os.path.join(r"C:\Users\User\Desktop", "DAA_Assignment4_Report.docx")
    desktop_path2 = os.path.join(r"C:\Users\User\Desktop", "REPORT.docx")
    project_path = os.path.join(r"C:\Users\User\IdeaProjects\Assignment-4-DAA", "REPORT.docx")

    doc.save(desktop_path)
    doc.save(desktop_path2)
    doc.save(project_path)
    print(f"Successfully generated DOCX reports:")
    print(f" - {desktop_path}")
    print(f" - {desktop_path2}")
    print(f" - {project_path}")

if __name__ == "__main__":
    create_report()
