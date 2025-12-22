# language_agent/goal_oriented_planner.py

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from .language_agent import LanguageAgent

#Ibr this is prolly not as neccesary, leaving it here in case we may want it tho xx

@dataclass
class PlanningStep:
    """Represents a single planning step with context and task."""
    step_number: int
    context: str
    task: str
    is_refined: bool = False
    refinement_reason: Optional[str] = None


class GoalOrientedPlanner:
    """
    Decomposes high-level goals into structured sub-goals with validation and refinement.
    """
    
    def __init__(self, goal: str, system_prompt: str, agent: LanguageAgent):
        self.goal = goal
        self.system_prompt = system_prompt
        self.agent = agent
        self.planning_steps: List[PlanningStep] = []
        self.refinement_count = 0
        self.max_refinements = 3
        
    def generate_initial_plan(self) -> List[PlanningStep]:
        """
        Generate initial plan by decomposing the goal into sub-goals.
        
        Returns:
            List[PlanningStep]: Initial planning steps
        """
        print(f"Generating initial plan for goal: {self.goal}")
        
        # Create planning prompt
        planning_prompt = (
            f"Create a structured study plan to achieve this learning goal:\n"
            f"GOAL: {self.goal}\n\n"
            f"Requirements:\n"
            f"1. Break the goal into sequential study modules or sessions\n"
            f"2. Each step must have a clear CONTEXT (Learning Objective) and TASK (Study Activity)\n"
            f"3. CONTEXT: What concept or topic is being covered\n"
            f"4. TASK: Specific study action (e.g., 'Read chapter X', 'Solve practice problems', 'Review lecture notes')\n"
            f"5. Start with foundational concepts and build up to complex ones\n"
            f"6. Include review or self-assessment steps\n\n"
            f"Format each step as:\n"
            f"STEP X:\n"
            f"CONTEXT: [Learning Objective/Topic]\n"
            f"TASK: [Specific Study Activity]"
        )
        
        # Get conversation context
        conversation = [{"role": "system", "content": self.system_prompt}]
        
        # Prepare payload
        payload = {
            "model": self.agent.current_model,
            "messages": conversation + [{"role": "user", "content": planning_prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        # Generate plan
        plan_response = self._send_request(payload)
        
        if not plan_response:
            raise Exception("Failed to generate initial plan")
        
        # Parse steps
        steps = self._parse_planning_response(plan_response)
        self.planning_steps = steps
        
        print(f"Generated {len(steps)} initial planning steps")
        return steps
    
    def validate_and_refine_steps(self) -> List[PlanningStep]:
        """
        Validate each step and refine poor/unhelpful ones.
        
        Returns:
            List[PlanningStep]: Validated and refined planning steps
        """
        print("Validating and refining planning steps...")
        
        refined_steps = []
        
        for i, step in enumerate(self.planning_steps):
            print(f"Validating step {step.step_number}...")
            
            # Check if step needs refinement
            needs_refinement, reason = self._evaluate_step_quality(step)
            
            if needs_refinement and self.refinement_count < self.max_refinements:
                print(f"Refining step {step.step_number}: {reason}")
                refined_step = self._refine_step(step, reason)
                refined_step.is_refined = True
                refined_step.refinement_reason = reason
                refined_steps.append(refined_step)
                self.refinement_count += 1
            else:
                refined_steps.append(step)
        
        self.planning_steps = refined_steps
        print(f"Validation complete. {self.refinement_count} steps refined.")
        return refined_steps
    
    def execute_plan(self) -> Dict:
        """
        Execute the validated plan using ReasoningChain.
        
        Returns:
            Dict: Execution results including all steps and outputs
        """
        print("Executing validated plan...")
        
        # Import ReasoningChain locally to avoid circular imports
        from .reasoning_chain import ReasoningChain, run_structured_reasoning_chain, reason_and_return_output
        
        results = {
            "goal": self.goal,
            "steps_executed": [],
            "final_outcome": None
        }
        
        # Create reasoning chain for execution
        chain = ReasoningChain()
        chain.add_system_prompt(self.system_prompt)
        
        # Execute each step
        for i, step in enumerate(self.planning_steps):
            print(f"\nExecuting step {step.step_number}/{len(self.planning_steps)}")
            
            # Create step prompt combining context and task
            step_prompt = f"CONTEXT: {step.context}\n\nTASK: {step.task}"
            
            # Add to chain
            chain.add_user_query(step_prompt)
            
            # Execute step (using existing reasoning function)
            run_structured_reasoning_chain(chain, self.agent)
            
            # Store step result
            step_result = {
                "step_number": step.step_number,
                "context": step.context,
                "task": step.task,
                "is_refined": step.is_refined,
                "refinement_reason": step.refinement_reason,
                "reasoning_steps": chain.get_structured_steps()[-3:] if chain.get_structured_steps() else []  # Last 3 steps
            }
            results["steps_executed"].append(step_result)
        
        # Generate task-focused final output
        final_prompt = (
            f"Based on the completed study steps, provide a comprehensive Study Guide for the user.\n"
            f"Original goal: {self.goal}\n\n"
            f"Your response should be:\n"
            f"1. A structured summary of key concepts covered\n"
            f"2. A recommended schedule or order of review\n"
            f"3. Specific resources or topics to focus on for exams\n"
            f"4. A set of practice questions or self-check points derived from the steps\n"
            f"5. Encouraging next steps for mastery\n\n"
            f"Format this as a clear, readable Study Guide."
        )
        chain.add_user_query(final_prompt)
        
        final_output = reason_and_return_output(chain, self.agent)
        results["final_outcome"] = final_output
        
        return results
    
    def _parse_planning_response(self, response: str) -> List[PlanningStep]:
        """Parse LLM response into PlanningStep objects."""
        steps = []
        
        # Split by STEP markers
        step_blocks = re.split(r'STEP\s+\d+[:.]', response, flags=re.IGNORECASE)
        step_blocks = [block.strip() for block in step_blocks if block.strip()]
        
        for i, block in enumerate(step_blocks):
            # Extract context and task
            context_match = re.search(r'CONTEXT[:\s]+(.*?)(?:\nTASK:|\Z)', block, re.DOTALL | re.IGNORECASE)
            task_match = re.search(r'TASK[:\s]+(.*?)(?:\n|\Z)', block, re.DOTALL | re.IGNORECASE)
            
            context = context_match.group(1).strip() if context_match else f"Working on step {i+1} of goal: {self.goal}"
            task = task_match.group(1).strip() if task_match else block.strip()
            
            step = PlanningStep(
                step_number=i + 1,
                context=context,
                task=task
            )
            steps.append(step)
        
        return steps
    
    def _evaluate_step_quality(self, step: PlanningStep) -> Tuple[bool, str]:
        """
        Evaluate if a step needs refinement.
        
        Returns:
            Tuple[bool, str]: (needs_refinement, reason)
        """
        issues = []
        
        # Check for clarity
        if len(step.task) < 10:
            issues.append("Task description is too brief")
        
        if "tbd" in step.task.lower() or "to be determined" in step.task.lower():
            issues.append("Task contains undefined elements")
        
        # Check for actionability - focused on educational activities
        if not any(action_word in step.task.lower() for action_word in 
                  ["read", "analyze", "practice", "solve", "review", "evaluate", "study", "memorize", "summarize", "quiz", "watch", "learn"]):
            issues.append("Task lacks clear educational action (e.g., read, practice, review)")
        
        # Check context relevance
        if len(step.context) < 5:
            issues.append("Context is insufficient")
        
        if issues:
            return True, "; ".join(issues)
        
        return False, ""
    
    def _refine_step(self, step: PlanningStep, reason: str) -> PlanningStep:
        """
        Refine a poor quality step.
        
        Args:
            step: The step to refine
            reason: Why refinement is needed
            
        Returns:
            PlanningStep: Refined step
        """
        print(f"Refining step {step.step_number} due to: {reason}")
        
        refinement_prompt = (
            f"Improve this planning step:\n\n"
            f"ORIGINAL STEP {step.step_number}:\n"
            f"CONTEXT: {step.context}\n"
            f"TASK: {step.task}\n\n"
            f"ISSUES IDENTIFIED: {reason}\n\n"
            f"Please provide an improved version with:\n"
            f"1. Clear, detailed context\n"
            f"2. Specific, actionable task\n"
            f"3. Direct contribution to the goal\n\n"
            f"Format as:\n"
            f"CONTEXT: [improved context]\n"
            f"TASK: [improved task]"
        )
        
        conversation = [{"role": "system", "content": self.system_prompt}]
        payload = {
            "model": self.agent.current_model,
            "messages": conversation + [{"role": "user", "content": refinement_prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        refinement_response = self._send_request(payload)
        
        if refinement_response:
            # Parse refined step
            context_match = re.search(r'CONTEXT[:\s]+(.*?)(?:\nTASK:|\Z)', refinement_response, re.DOTALL | re.IGNORECASE)
            task_match = re.search(r'TASK[:\s]+(.*?)(?:\n|\Z)', refinement_response, re.DOTALL | re.IGNORECASE)
            
            refined_context = context_match.group(1).strip() if context_match else step.context
            refined_task = task_match.group(1).strip() if task_match else step.task
            
            return PlanningStep(
                step_number=step.step_number,
                context=refined_context,
                task=refined_task
            )
        
        # If refinement fails, return original
        return step
    
    def _send_request(self, payload: dict) -> Optional[str]:
        """Send request to LLM agent."""
        url = f"{self.agent.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.agent.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            import requests
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def get_plan_summary(self) -> Dict:
        """Get summary of the current plan."""
        return {
            "goal": self.goal,
            "total_steps": len(self.planning_steps),
            "refined_steps": len([s for s in self.planning_steps if s.is_refined]),
            "steps": [
                {
                    "step_number": step.step_number,
                    "context": step.context,
                    "task": step.task,
                    "is_refined": step.is_refined
                }
                for step in self.planning_steps
            ]
        }