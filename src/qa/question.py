from typing import List, Dict, NamedTuple, Optional

class GraphPathStep(NamedTuple):
	"""Represents a single step in a graph traversal path."""
	edge_type: str
	target_node_type: str
	capture_as: str
	source_variable: Optional[str] = None # If None, uses the previously captured node

class QuestionTemplate:
	"""Represents a template for generating a question, answer, and context."""
	def __init__(
		self,
		template: str,
		requirements: Dict[str, Dict[str, str]],
		path: List[GraphPathStep],
		answer_variable: str,
		answer_pattern: str
	):
		if not path or not answer_variable or not answer_pattern:
			raise ValueError("Path, answer_variable, and answer_pattern must be provided.")

		self.template = template
		self.requirements = requirements # e.g., {"municipality": {"type": "municipality"}}
		self.path = path # List of GraphPathStep objects
		self.answer_variable = answer_variable # Key in captured_nodes holding the answer
		self.answer_pattern = answer_pattern # Format string for the answer

	def __repr__(self):
		return f"QuestionTemplate(template='{self.template[:30]}...', requirements={self.requirements}, path_steps={len(self.path)})"
