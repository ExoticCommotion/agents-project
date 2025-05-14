# AI Project Manager (AIPM)

The AI Project Manager (AIPM) is a system of specialized agents designed to orchestrate and manage complex projects. It breaks down high-level goals into structured plans, creates and prioritizes tasks, coordinates execution, analyzes results, and synthesizes feedback for continuous improvement.

## Agent Roles

### 1. Planner Agent

The Planner Agent takes high-level goals and creates structured plans with clear steps, complexity estimates, and time estimates.

```python
from backend.app.agents.planner import PlannerAgent
from backend.app.core.data_models import HighLevelGoal

planner = PlannerAgent()
goal = HighLevelGoal(id="goal-1", title="Build Feature X", description="...")
plan = planner.create_plan(goal)
```

### 2. Task Definer Agent

The Task Definer Agent breaks down structured plans into epics and well-defined tasks (tickets) that can be executed by Devin.

```python
from backend.app.agents.task_definer import TaskDefinerAgent

task_definer = TaskDefinerAgent()
epics = task_definer.create_epics(plan)
tickets = []
for epic in epics:
    tickets.extend(task_definer.create_tickets(epic))
```

### 3. Prioritizer Agent

The Prioritizer Agent takes a list of tasks and prioritizes them based on dependencies, complexity, and importance.

```python
from backend.app.agents.prioritizer import PrioritizerAgent

prioritizer = PrioritizerAgent()
prioritized_tickets = prioritizer.prioritize_tickets(tickets)
```

### 4. Execution Coordinator Agent

The Execution Coordinator Agent manages the execution of tasks by Devin, tracking progress and collecting results.

```python
from backend.app.agents.execution_coordinator import ExecutionCoordinatorAgent

execution_coordinator = ExecutionCoordinatorAgent()
result = execution_coordinator.execute_ticket(ticket)
```

### 5. Feedback Analyzer Agent

The Feedback Analyzer Agent analyzes execution results and generates structured analysis reports with insights and improvement suggestions.

```python
from backend.app.agents.feedback_analyzer import FeedbackAnalyzerAgent

feedback_analyzer = FeedbackAnalyzerAgent()
report = feedback_analyzer.analyze_result(result)
```

### 6. Feedback Synthesizer Agent

The Feedback Synthesizer Agent synthesizes feedback from multiple sources into learning proposals for future improvement.

```python
from backend.app.agents.feedback_synthesizer import FeedbackSynthesizerAgent

feedback_synthesizer = FeedbackSynthesizerAgent()
proposal = feedback_synthesizer.synthesize_feedback(reports, feedback)
```

## Tools

### Devin Session Manager

The Devin Session Manager interacts with the Devin API to create and manage Devin sessions for executing tasks.

```python
from backend.app.tools.devin_session_manager import DevinSessionManager

session_manager = DevinSessionManager()
session_id = session_manager.create_session(ticket)
result = session_manager.get_session_result(session_id)
```

## Pipeline Orchestration

The Project Orchestrator coordinates the flow of data between the different agents in the AI Project Manager system, managing the end-to-end process from high-level goal to learning proposals.

```python
from backend.app.core.orchestration.project_orchestrator import ProjectOrchestrator
from backend.app.core.data_models import HighLevelGoal, InitiativeGoal

orchestrator = ProjectOrchestrator()

# Process a high-level goal
goal = HighLevelGoal(id="goal-1", title="Build Feature X", description="...")
learning_proposal = orchestrator.run_placeholder_pipeline(goal)

# Process an initiative goal
initiative = InitiativeGoal(id="initiative-1", title="Initiative Y", description="...")
tickets = orchestrator.process_initiative(initiative)
```

## Data Models

The AI Project Manager uses a set of data models to represent the different entities in the system:

- `HighLevelGoal`: Represents a high-level goal or objective for a project
- `InitiativeGoal`: Represents a high-level initiative goal for a project
- `StructuredPlan`: Represents a structured plan created by the Planner Agent
- `DecompositionPlan`: Represents a decomposition plan created from a high-level initiative goal
- `WorkPackage`: Represents a work package created as part of a decomposition plan
- `Epic`: Represents an epic or major feature set within a project plan
- `DevinTicket`: Represents a task ticket for Devin to execute
- `ExecutionResult`: Represents the result of a task execution by Devin
- `StructuredAnalysisReport`: Represents an analysis report of execution results
- `ActionDecision`: Represents a decision on what action to take next
- `FeedbackContent`: Represents feedback content for learning and improvement
- `LearningProposal`: Represents a proposal for learning and improvement

## Future Enhancements

- Integration with external project management tools
- Advanced prioritization algorithms
- Real-time progress tracking and reporting
- Machine learning-based feedback analysis
- Automated learning proposal implementation
