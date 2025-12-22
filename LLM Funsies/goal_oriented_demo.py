# goal_oriented_demo.py

import os
import json
from language_agent import LanguageAgent, GoalOrientedPlanner


def load_api_key():
    """Load API key from venv/api_key.txt"""
    #C:\Users\katwu\agent_learning\.venv
    api_key_path = os.path.join(".venv", "api_key.txt")
    try:
        with open(api_key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"API key file not found at {api_key_path}")


def main():
    # Load API key
    try:
        api_key = load_api_key()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    # Initialize agent
    agent = LanguageAgent(
        api_key=api_key,
        default_model="qwen-3-235b-a22b-instruct-2507"
    )
    
    # Define goal and system prompt
    goal = "Develop a comprehensive cybersecurity awareness program for our organization"
    
    system_prompt = (
        "Persona to adopt: You are a cybersecurity expert and training specialist\n"
        "Role as a goal breaker: Break down complex cybersecurity initiatives into actionable steps\n"
        "Context: Our organization needs to improve employee awareness of cybersecurity risks\n"
        "Task: Create a structured program that educates employees and reduces security incidents"
    )
    
    # Create planner
    print("Creating Goal-Oriented Planner...")
    planner = GoalOrientedPlanner(goal, system_prompt, agent)
    
    # Generate initial plan
    try:
        initial_steps = planner.generate_initial_plan()
        print(f"\nInitial plan generated with {len(initial_steps)} steps")
        
        # Display plan summary
        plan_summary = planner.get_plan_summary()
        print("\nPLAN SUMMARY:")
        print("=" * 50)
        for step in plan_summary["steps"]:
            status = "REFINED" if step["is_refined"] else "ORIGINAL"
            print(f"Step {step['step_number']} [{status}]:")
            print(f"  Context: {step['context'][:80]}...")
            print(f"  Task: {step['task'][:80]}...")
            print()
        
        # Validate and refine steps
        refined_steps = planner.validate_and_refine_steps()
        
        # Display refined plan
        refined_summary = planner.get_plan_summary()
        print("\nREFINED PLAN SUMMARY:")
        print("=" * 50)
        print(f"Total steps: {refined_summary['total_steps']}")
        print(f"Refined steps: {refined_summary['refined_steps']}")
        
        # Execute plan
        print("\nExecuting plan...")
        execution_results = planner.execute_plan()
        
        # Save results
        with open("goal_oriented_execution_results.json", "w") as f:
            json.dump(execution_results, f, indent=2, ensure_ascii=False)
        
        print("\nExecution complete. Results saved to 'goal_oriented_execution_results.json'")
        
        # Display final outcome
        if execution_results["final_outcome"]:
            print("\nACTIONABLE FINAL OUTPUT:")
            print("=" * 50)
            print(execution_results["final_outcome"])
        
    except Exception as e:
        print(f"Error during planning/execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()