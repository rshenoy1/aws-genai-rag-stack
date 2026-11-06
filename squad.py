
import time

def tool_web_search(query):
    print(f"   [TOOL RUNNING] Scraping live data for: \"{query}\"...")
    time.sleep(0.3)
    return "CURRENT FACT: Widget prices spiked by 15% due to a raw copper shortage."

def tool_secure_calculator(formula):
    print(f"   [TOOL RUNNING] Executing sandboxed formula math: {formula}...")
    time.sleep(0.3)
    if "100" in formula and "1.15" in formula:
        return "115.00"
    return "0.00"

def worker_researcher(task_payload):
    print("\n -> [AGENT ACTIVATED] Researcher Agent initialized.")
    fact_result = tool_web_search(task_payload)
    return fact_result

def worker_analyst(task_payload):
    print("\n -> [AGENT ACTIVATED] Analyst Agent initialized.")
    math_result = tool_secure_calculator(task_payload)
    return f"ANALYTICS REPORT: Projected single unit manufacturing cost totals ${math_result} USD."

def worker_writer(research_context, analysis_context):
    print("\n -> [AGENT ACTIVATED] Writer Agent initialized.")
    print("    [WRITER RUNNING] Composing executive compliance brief...")
    time.sleep(0.4)
    brief = f"""
    === EXECUTIVE COMPLIANCE REPORT ===
    {research_context}
    {analysis_context}
    STATUS: Approved. Sourcing alternatives recommended to mitigate cost baseline adjustments.
    ==================================
    """
    return brief

def run_squad_manager(user_macro_objective):
    print(f"\n[SQUAD MANAGER] New Objective Received: \"{user_macro_objective}\"")
    print("[SQUAD MANAGER] Planning task delegation roadmap...")
    time.sleep(0.5)
    
    research_data = worker_researcher("Latest standard industry copper manufacturing prices")
    print(f" <- [AGENT RETURN] Researcher data: \"{research_data}\"")
    
    analysis_data = worker_analyst("Compute base price 100 * 1.15 overhead")
    print(f" <- [AGENT RETURN] Analyst data: \"{analysis_data}\"")
    
    final_output = worker_writer(research_data, analysis_data)
    
    print("\n[SUCCESS] Squad Execution Completed successfully!")
    print(final_output)

if __name__ == "__main__":
    run_squad_manager("Research copper price spikes, compute a 15% overhead increase on a $100 base, and draft a brief.")

