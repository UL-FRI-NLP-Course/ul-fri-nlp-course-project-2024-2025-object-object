from typing import List, Dict, Tuple, NamedTuple, Optional

class Fact(NamedTuple):
	"""Represents a single Subject-Predicate-Object fact derived from the graph."""
	subject: str
	predicate: str
	object: str

	def __str__(self):
		"""Simple string representation for printing."""
		return f"<{self.subject}> <{self.predicate}> <{self.object}>."

	def to_tuple(self) -> Tuple[str, str, str]:
		"""Convert Fact to a simple tuple for set operations."""
		return (self.subject, self.predicate, self.object)

class QA:
	"""Represents a generated Question, Answer, and supporting Context Facts."""
	def __init__(self, question: str, answer: str, context_facts: List[Fact]):
		self.question = question
		self.answer = answer
		self.context_facts = context_facts # List of Fact objects

	def __repr__(self):
		return f"QA(question='{self.question}', answer='{self.answer}', num_facts={len(self.context_facts)})"

	def to_dict(self) -> Dict[str, str]:
		"""Convert QA to a dictionary representation."""
		return {
			"question": self.question,
			"answer": self.answer,
			"context_facts": [str(fact) for fact in self.context_facts]
		}

	def get_context_string(self, separator: str = " ") -> str:
		"""Helper to get context facts as a single string."""
		return separator.join(map(str, self.context_facts))