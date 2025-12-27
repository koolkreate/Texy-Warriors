# language_agent/__init__.py

"""
Language Agent Package

Core components for building agentic systems with reasoning capabilities.
"""

# Message classes
from .messages import BaseMessage, SystemMessage, ChatMessage

# Core agent
# Core agent
from .main_agent import LanguageAgent, GeminiAgent

# Reasoning chain components
# from .reasoning_chain import (
#     ReasoningChain, 
#     run_structured_reasoning_chain,
#     reason_and_return_output
# )

# Goal-oriented planner
from .goal_oriented_planner import GoalOrientedPlanner, PlanningStep

# Structured query components
from .structured_query import BaseStructuredModel, StructuredQueryEngine

__version__ = "0.7.0"
__author__ = "Kwame T"

__all__ = [
    # Message classes
    "BaseMessage",
    "SystemMessage", 
    "ChatMessage",
    
    # Core agent
    "LanguageAgent",
    "GeminiAgent",
    
    # # Reasoning chain
    # "ReasoningChain",
    # "run_structured_reasoning_chain",
    # "reason_and_return_output",
    
    # Lesson planner
    "GoalOrientedPlanner",
    "PlanningStep",
    
    # Structured query
    "BaseStructuredModel",
    "StructuredQueryEngine"
]