from qa.question import QuestionTemplate, GraphPathStep

TEMPLATES = [
	# --- Simple Fact Retrieval (1-Hop) ---
	QuestionTemplate(
		template="V kateri statistični regiji se nahaja občina {municipality_label}?",
		requirements={"municipality": {"type": "municipality"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="region", source_variable="municipality", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Koliko prebivalcev ima občina {municipality_label}?",
		requirements={"municipality": {"type": "municipality"}},
		path=[
			GraphPathStep(edge_type="has_population", target_node_type="population", source_variable="municipality", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšna je površina občine {municipality_label}?",
		requirements={"municipality": {"type": "municipality"}},
		path=[
			GraphPathStep(edge_type="has_area", target_node_type="area", source_variable="municipality", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label} km²"
	),
	QuestionTemplate(
		template="V kateri občini leži vrh {peak_label}?",
		requirements={"peak": {"type": "mountain_peak"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="peak", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšno nadmorsko višino dosega {peak_label}?",
		requirements={"peak": {"type": "mountain_peak"}},
		path=[
			GraphPathStep(edge_type="has_elevation", target_node_type="elevation", source_variable="peak", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label} m"
	),
	QuestionTemplate(
		template="V kateri občini stoji grad {castle_label}?",
		requirements={"castle": {"type": "castle"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="castle", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Pod kateri status kulturne dediščine spada grad {castle_label}?",
		requirements={"castle": {"type": "castle"}},
		path=[
			GraphPathStep(edge_type="belongs_to_heritage", target_node_type="heritage", source_variable="castle", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	# --- Multi-Hop Retrieval (2+ Hops) ---
	QuestionTemplate(
		template="Kakšna je populacija občine, v kateri leži vrh {peak_label}?",
		requirements={"peak": {"type": "mountain_peak"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="peak", capture_as="mun"),
			GraphPathStep(edge_type="has_population", target_node_type="population", source_variable="mun", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšna je površina občine, kjer stoji grad {castle_label}?",
		requirements={"castle": {"type": "castle"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="castle", capture_as="mun"),
			GraphPathStep(edge_type="has_area", target_node_type="area", source_variable="mun", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label} km²"
	),
	QuestionTemplate(
		template="V kateri statistični regiji leži vrh {peak_label}?",
		requirements={"peak": {"type": "mountain_peak"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="peak", capture_as="mun"),
			GraphPathStep(edge_type="located_in", target_node_type="region", source_variable="mun", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="V kateri statistični regiji stoji grad {castle_label}?",
		requirements={"castle": {"type": "castle"}},
		path=[
			GraphPathStep(edge_type="located_in", target_node_type="municipality", source_variable="castle", capture_as="mun"),
			GraphPathStep(edge_type="located_in", target_node_type="region", source_variable="mun", capture_as="answer")
		],
		answer_variable="answer",
		answer_pattern="{target_label}"
	)
]