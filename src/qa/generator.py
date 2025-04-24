from random import choice, sample, random
import networkx as nx
from typing import Dict, Any, List, Tuple, Optional
from collections.abc import Set
from typeguard import typechecked
from .question import QuestionTemplate, GraphPathStep
from .answer import Fact, QA

@typechecked
class QAGenerator:
	_node_label_to_id_cache = {}

	def find_node_id_by_label(self, graph: nx.Graph, label: str) -> Optional[str]:
		"""Finds the first node ID matching a given label."""
		if label in self._node_label_to_id_cache:
			return self._node_label_to_id_cache[label]

		for node_id, data in graph.nodes(data=True):
			if data.get("label") == label:
				self._node_label_to_id_cache[label] = node_id # Cache the result
				return node_id
		return None

	def get_random_node(self, graph: nx.Graph, node_type: str) -> Optional[str]:
		"""Selects a random node ID of a specific type from the graph."""
		nodes_of_type = [
			node_id for node_id, data in graph.nodes(data=True)
			if data.get("type") == node_type and data.get("label")  # Ensure it has a label
		]
		if not nodes_of_type:
			return None
		return sample(nodes_of_type, 1)[0]

	def traverse_graph_path(
		self,
		graph: nx.Graph,
		start_nodes: Dict[str, Dict[str, Any]],
		template_info: QuestionTemplate
	) -> Tuple[bool, Dict[str, Dict[str, Any]], List[Fact]]: # Return List[Fact] now
		"""
		Traverses the graph based on a declarative path definition using GraphPathStep objects.

		Args:
			graph: The NetworkX graph.
			start_nodes: A dictionary of starting nodes with their IDs and labels.
			template_info: The QuestionTemplate object containing the path definition.

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

		for step in template_info.path:
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

		if template_info.answer_variable not in captured_nodes:
			return False, captured_nodes, traversal_facts

		return True, captured_nodes, traversal_facts

	def generate_distractor_facts(
		self,
		graph: nx.Graph,
		correct_facts: List[Fact],
		num_distractors: int = 2
	) -> List[Fact]:
		"""
		Generates distractor facts related to entities in the correct facts.

		Args:
			graph: The NetworkX graph.
			correct_facts: A list of Fact objects representing the relevant context.
			num_distractors: The desired number of distractor facts.

		Returns:
			A list of Fact objects representing distractor facts.
		"""
		if not correct_facts or num_distractors <= 0:
			return []

		# 1. Identify entities and create a set of correct fact tuples for quick lookup
		entities_of_interest: Set[str] = set()
		correct_fact_tuples: Set[Tuple[str, str, str]] = set()
		for fact in correct_facts:
			entities_of_interest.add(fact.subject)
			entities_of_interest.add(fact.object)
			correct_fact_tuples.add(fact.to_tuple())

		# 2. Find candidate distractor facts connected to these entities
		candidate_distractors: List[Fact] = []
		processed_entities: Set[str] = set() # Avoid processing the same entity multiple times

		# Clear cache for node lookup before starting generation batch
		self._node_label_to_id_cache.clear()

		for entity_label in entities_of_interest:
			if entity_label in processed_entities:
				continue

			entity_id = self.find_node_id_by_label(graph, entity_label)
			if entity_id is None or not graph.has_node(entity_id):
				continue # Entity label not found in graph

			processed_entities.add(entity_label)

			# Find all neighbors and generate potential facts
			for neighbor_id in graph.neighbors(entity_id):
				if not graph.has_node(neighbor_id): continue # Should not happen

				neighbor_label = graph.nodes[neighbor_id].get("label")
				edge_data = graph.get_edge_data(entity_id, neighbor_id, default={})
				edge_type = edge_data.get("type")

				if neighbor_label and edge_type:
					# Create fact: <entity> <edge_type> <neighbor>
					potential_fact = Fact(subject=entity_label, predicate=edge_type, object=neighbor_label)
					# Add if it's not one of the correct facts
					if potential_fact.to_tuple() not in correct_fact_tuples:
						candidate_distractors.append(potential_fact)

					# Consider adding the inverse fact if your graph represents bidirectional info implicitly
					# Example: If edge is 'located_in', maybe add '<neighbor> <contains> <entity>'
					# This depends heavily on your schema and needs careful definition.
					# For now, we only add the direct fact found.

		# 3. Select distractors randomly
		if not candidate_distractors:
			return []

		num_to_sample = min(num_distractors, len(candidate_distractors))
		selected_distractors = sample(candidate_distractors, num_to_sample)

		return selected_distractors

	def generate_questions(
		self,
		graph: nx.Graph,
		templates: List[QuestionTemplate],
		num_questions: int = 50,
		add_distractors: int = 0
	) -> List[QA]:
		"""
		Generates questions based on generalized QuestionTemplate objects, optionally adding distractor facts.

		Args:
			graph: The populated NetworkX graph.
			templates: A list of QuestionTemplate objects.
			num_questions: The desired number of questions to generate.
			add_distractors: The number of distractor facts to add to each generated QA pair.

		Returns:
			A list of QA objects.
		"""
		if not graph or graph.number_of_nodes() == 0:
			print("Graph is empty. Cannot generate questions.")
			return []

		generated_data: List[QA] = []
		attempts = 0
		max_attempts = num_questions * 25

		# Clear node lookup cache at the start of generation
		self._node_label_to_id_cache.clear()

		while len(generated_data) < num_questions and attempts < max_attempts:
			attempts += 1
			template_info: QuestionTemplate = choice(templates)

			start_nodes = {}
			format_dict = {}
			for req_key, req_details in template_info.requirements.items():
				node_id = self.get_random_node(graph, req_details["type"])
				if node_id is None:
					raise ValueError(f"No nodes of type {req_details['type']} not found in graph.")

				node_label = graph.nodes[node_id].get("label")
				if not node_label:
					raise ValueError(f"Node {node_id} does not have a label.")

				start_nodes[req_key] = {"id": node_id, "label": node_label, "type": req_details["type"]}
				format_dict[f"{req_key}_label"] = node_label

			question = template_info.template.format(**format_dict)

			success, captured_nodes, context_facts = self.traverse_graph_path(
				graph, start_nodes, template_info
			)
			if not success:
				continue

			distractor_facts: List[Fact] = []

			answer_node_data = captured_nodes[template_info.answer_variable]
			answer_label = answer_node_data.get("label")
			if not answer_label:
				raise ValueError("Answer node missing label.")
			answer = template_info.answer_pattern.format(target_label=answer_label)

			# Generate distractor facts if requested
			if add_distractors > 0 and context_facts:
				distractor_facts = self.generate_distractor_facts(graph, context_facts, add_distractors)

			if context_facts: # Ensure context was generated
				generated_data.append(QA(
					question=question,
					answer=answer,
					context_facts=sorted(context_facts + distractor_facts, key=lambda x: random())
				))

		# Clear cache after generation batch
		self._node_label_to_id_cache.clear()

		print(f"Generated {len(generated_data)} questions after {attempts} attempts.")
		return generated_data