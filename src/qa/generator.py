from random import choice, sample
import networkx as nx
from typing import Dict, Any, List, Tuple, Optional
from typeguard import typechecked
from .question import QuestionTemplate, GraphPathStep
from .answer import Fact, QA

@typechecked
class QAGenerator:
	def get_random_node(graph: nx.Graph, node_type: str) -> Optional[str]:
		"""Selects a random node ID of a specific type from the graph."""
		nodes_of_type = [
			node_id for node_id, data in graph.nodes(data=True)
			if data.get("type") == node_type and data.get("label")  # Ensure it has a label
		]
		if not nodes_of_type:
			return None
		return sample(nodes_of_type, 1)[0]

	def traverse_graph_path(
		graph: nx.Graph,
		start_nodes: Dict[str, Dict[str, Any]],
		path_definition: List[GraphPathStep]
	) -> Tuple[bool, Dict[str, Dict[str, Any]], List[Fact]]: # Return List[Fact] now
		"""
		Traverses the graph based on a declarative path definition using GraphPathStep objects.

		Returns:
			A tuple containing:
			- success (bool): Whether the full path was successfully traversed.
			- captured_nodes (dict): All nodes captured during traversal (including start nodes).
			- traversal_facts (list): List of Fact objects representing successful steps.
		"""
		captured_nodes = start_nodes.copy()
		traversal_facts: List[Fact] = [] # Store Fact objects
		if not start_nodes:
			return False, captured_nodes, traversal_facts
		current_step_source_variable = list(start_nodes.keys())[0] # Assume single start node for now

		for step in path_definition:
			source_var = step.source_variable if step.source_variable else current_step_source_variable

			if source_var not in captured_nodes:
				return False, captured_nodes, traversal_facts

			current_node_id = captured_nodes[source_var]["id"]
			current_node_label = captured_nodes[source_var]["label"]

			possible_next_nodes = []
			for neighbor_id in graph.neighbors(current_node_id):
				edge_data = graph.get_edge_data(current_node_id, neighbor_id, default={})
				node_data = graph.nodes[neighbor_id]
				if (edge_data.get("type") == step.edge_type and
					node_data.get("type") == step.target_node_type and
					node_data.get("label")):
					possible_next_nodes.append(neighbor_id)

			if len(possible_next_nodes) == 1:
				next_node_id = possible_next_nodes[0]
				next_node_data = graph.nodes[next_node_id]
				next_node_label = next_node_data.get("label")

				captured_nodes[step.capture_as] = {
					"id": next_node_id,
					"label": next_node_label,
					"type": step.target_node_type
				}
				# Store step data as a Fact object
				traversal_facts.append(Fact(
					subject=current_node_label,
					predicate=step.edge_type,
					object=next_node_label
				))
				current_step_source_variable = step.capture_as
			else:
				return False, captured_nodes, traversal_facts

		return True, captured_nodes, traversal_facts


	def generate_questions(graph: nx.Graph, templates: List[QuestionTemplate], num_questions: int = 50) -> List[QA]:
		"""
		Generates questions based on generalized QuestionTemplate objects.

		Args:
			graph: The populated NetworkX graph.
			templates: A list of QuestionTemplate objects.
			num_questions: The desired number of questions to generate.

		Returns:
			A list of QA objects.
		"""
		if not graph or graph.number_of_nodes() == 0:
			print("Graph is empty. Cannot generate questions.")
			return []

		generated_data: List[QA] = []
		attempts = 0
		max_attempts = num_questions * 20 # Increase attempts slightly more

		while len(generated_data) < num_questions and attempts < max_attempts:
			attempts += 1
			template_info: QuestionTemplate = choice(templates)

			if not template_info.path or not template_info.answer_variable or not template_info.answer_pattern:
				continue

			start_nodes = {}
			possible = True
			format_dict = {}
			for req_key, req_details in template_info.requirements.items():
				node_id = QAGenerator.get_random_node(graph, req_details["type"])
				if node_id is None: possible = False; break
				node_label = graph.nodes[node_id].get("label")
				if not node_label: possible = False; break
				start_nodes[req_key] = {"id": node_id, "label": node_label, "type": req_details["type"]}
				format_dict[f"{req_key}_label"] = node_label

			if not possible: continue

			try:
				question = template_info.template.format(**format_dict)
			except KeyError: continue

			success, captured_nodes, traversal_facts = QAGenerator.traverse_graph_path(
				graph, start_nodes, template_info.path
			)

			answer = "N/A"
			context_facts: List[Fact] = []

			if success and template_info.answer_variable in captured_nodes:
				try:
					answer_node_data = captured_nodes[template_info.answer_variable]
					answer_label = answer_node_data.get("label")
					if not answer_label: raise ValueError("Answer node missing label.")
					answer = template_info.answer_pattern.format(target_label=answer_label)
					context_facts = traversal_facts # Use the facts returned by traversal

				except Exception:
					answer = "Napaka pri formatiranju odgovora."
			else:
				answer = "Podatek ni na voljo ali pot ni veljavna."

			valid_answer_states = ["N/A", "Podatek ni na voljo ali pot ni veljavna.", "Napaka pri formatiranju odgovora."]
			if answer not in valid_answer_states and context_facts: # Ensure context was generated
				generated_data.append(QA(
					question=question,
					answer=answer,
					context_facts=context_facts # Store the list of Fact objects
				))
			# Optional: Log skips...

		print(f"Generated {len(generated_data)} questions after {attempts} attempts.")
		return generated_data