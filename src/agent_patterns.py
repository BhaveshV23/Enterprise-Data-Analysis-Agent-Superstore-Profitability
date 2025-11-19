import json
import time
import re
from google.genai.types import Tool, FunctionDeclaration, Schema
from google.genai.errors import APIError

# NOTE: This file depends on the functions defined in src/tools.py (data_summary, automated_eda, check_for_outliers)

# --- Tool Dispatcher (Cell 12 Logic) ---

def call_tool(name: str, df, **kwargs):
    """
    Executes the appropriate local Python function based on the tool name requested 
    by the Gemini model. Requires the DataFrame (df) to be passed explicitly.
    """
    # Import local tool functions (assuming they are available in the running environment)
    from tools import data_summary, automated_eda, check_for_outliers 

    # --- 1. Data Summary Tool ---
    if name == "data_summary":
        print(f"-> Executing tool: {name}()")
        return data_summary(df)

    # --- 2. Automated EDA Tool ---
    elif name == "automated_eda":
        print(f"-> Executing tool: {name}()")
        return automated_eda(df)

    # --- 3. Outlier Check Tool ---
    elif name == "check_for_outliers":
        if 'column_name' not in kwargs:
            return {"error": "Tool 'check_for_outliers' requires the 'column_name' parameter."}
            
        column_name = kwargs['column_name']
        print(f"-> Executing tool: {name}(column_name='{column_name}')")
        return check_for_outliers(df, column_name)
    
    # --- Fallback ---
    else:
        print(f"ERROR: Unknown tool requested by the model: {name}")
        return {"error": f"Unknown tool: {name}"}


# --- Official Function Calling Agent (Cell 13 Logic) ---

def enterprise_agent(user_query: str, df, client, model_name, tools_list, system_instruction):
    """
    Manages the multi-turn conversation necessary for Function Calling (Official SDK Method).
    """
    conversation_history = [
        {"role": "user", "parts": [{"text": user_query}]}
    ]

    max_turns = 5
    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1}: Calling Gemini (Official FC) ---")
        
        try:
            GENERATION_CONFIG = {
                "system_instruction": system_instruction, 
                "tools": tools_list                            
            }
            
            response = client.models.generate_content(
                model=model_name,
                contents=conversation_history,
                config=GENERATION_CONFIG 
            )
        except Exception as e:
            return f"API ERROR during turn {turn + 1}: {e}"

        if response.function_calls:
            print("Model requested a Tool Call.")
            
            tool_call = response.function_calls[0]
            tool_name = tool_call.name
            tool_args = dict(tool_call.args)

            try:
                # Use the local dispatcher, passing the DataFrame
                tool_output_data = call_tool(tool_name, df, **tool_args)
                tool_output_content = str(tool_output_data)
                
                print(f"Tool execution successful. Result size: {len(tool_output_content)} bytes.")

                conversation_history.append({"role": "model", "parts": [{"functionCall": tool_call}]})
                conversation_history.append({"role": "tool", "parts": [{"functionResponse": {"name": tool_name, "response": tool_output_data}}]})
                
                continue
                
            except Exception as e:
                print(f"Error executing Python tool '{tool_name}': {e}")
                conversation_history.append({"role": "model", "parts": [{"functionCall": tool_call}]})
                conversation_history.append({"role": "tool", "parts": [{"functionResponse": {"name": tool_name, "response": {"error": f"Internal tool execution error: {e}"}}}]})
                continue 

        elif response.text:
            return response.text
        
        else:
            return "Agent failed to generate a response or requested a tool not handled."

    return "Agent exceeded maximum conversation turns without providing a final answer."


# --- Two-Step Agent (Cell 15 Logic) ---

def ask_model_for_action(user_query, client, model_name):
    """Asks the model to decide deterministically: call a tool or respond directly."""
    
    # We include ALL defined tools in the prompt for the model to choose from
    tool_list = "`data_summary`, `automated_eda`, `check_for_outliers(column_name:str)`"
    
    prompt = (
    "You are an assistant that can call local python tools. "
    f"The ONLY valid tool names are: {tool_list}. " 
    "When appropriate, respond ONLY with exactly `TOOL:<tool_name>` (e.g. TOOL:automated_eda, or TOOL:check_for_outliers(column_name='profit')) to request a local tool, "
    "or respond with `RESPONSE:<your answer>` when you can answer directly. "
    "Do NOT include anything else. Now decide for this user query:\n\n"
    f"User query: {user_query}\n"
    )
    resp = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return resp.text.strip()


def enterprise_agent_new(user_query, df, client, model_name):
    """Executes the two-step agent pattern (Decision -> Execution -> Response)."""
    
    print("\n--- Step 1: Model Decision (Tool or Response) ---")
    decision = ask_model_for_action(user_query, client, model_name)
    print(f"Model Decision: {decision}")
    
    if decision.startswith("TOOL:"):
        tool_call_string = decision.split("TOOL:")[1].strip()
        
        # 1. Run the python tool locally
        tool_output = call_tool_two_step(tool_call_string, df)
        
        # 2. Convert tool output to a safe string
        tool_output_str = str(tool_output)[:20000] 

        # 3. Now ask the model to produce a final answer using the tool output
        print("\n--- Step 2: Model Interpretation ---")
        followup_prompt = (
            "The requested tool has been executed and produced the following output:\n\n"
            f"TOOL: {tool_call_string}\n\nOUTPUT:\n{tool_output_str}\n\n"
            "Using the original user query and the tool output above, "
            "produce a helpful, concise summary and any actionable insights. "
            "Be explicit about the charts produced (if any) and mention their filenames so they can be viewed."
            f"\n\nOriginal user query: {user_query}\n"
        )

        final = client.models.generate_content(
            model=model_name,
            contents=followup_prompt
        )
        return final.text

    elif decision.startswith("RESPONSE:"):
        return decision.split("RESPONSE:",1)[1].strip()
    else:
        # Fallback if the model didn't follow the strict format
        print("\n--- Step 2: Model Fallback (Failed to follow format) ---")
        fallback = client.models.generate_content(
            model=model_name,
            contents=f"User: {user_query}\nThe agent decision was irregular ('{decision}'). Please answer the user query directly and professionally."
        )
        return fallback.text

def call_tool_two_step(name_and_args: str, df):
    """
    Executes the appropriate local Python function for the Two-Step Agent by parsing the tool string.
    """
    match_params = re.search(r'\((.*?)\)', name_and_args)
    tool_name = name_and_args.split('(')[0].strip()
    
    kwargs = {}
    if match_params:
        args_str = match_params.group(1).replace("'", "").replace('"', '').strip()
        if '=' in args_str:
             key, value = args_str.split('=', 1)
             kwargs[key.strip()] = value.strip()
             
    return call_tool(tool_name, df, **kwargs)
