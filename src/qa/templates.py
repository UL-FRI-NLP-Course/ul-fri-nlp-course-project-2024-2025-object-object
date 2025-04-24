from qa.question import QuestionTemplate, GraphPathStep

TEMPLATES = [
	# --- Simple Fact Retrieval (1-Hop) ---
	QuestionTemplate(
		template="V kateri statistični regiji se nahaja občina {občina_label}?",
		requirements={"občina": {"type": "občina"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="regija", source_variable="občina", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Koliko prebivalcev ima občina {občina_label}?",
		requirements={"občina": {"type": "občina"}},
		path=[
			GraphPathStep(edge_type="ima_populacijo", target_node_type="populacija", source_variable="občina", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšna je površina občine {občina_label}?",
		requirements={"občina": {"type": "občina"}},
		path=[
			GraphPathStep(edge_type="ima_površino", target_node_type="površina", source_variable="občina", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label} km²"
	),
	QuestionTemplate(
		template="V kateri občini leži vrh {vrh_label}?",
		requirements={"vrh": {"type": "vrh"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="vrh", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšno nadmorsko višino dosega {vrh_label}?",
		requirements={"vrh": {"type": "vrh"}},
		path=[
			GraphPathStep(edge_type="ima_višino", target_node_type="višina", source_variable="vrh", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label} m"
	),
	QuestionTemplate(
		template="V kateri občini stoji grad {grad_label}?",
		requirements={"grad": {"type": "grad"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="grad", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Pod kateri status kulturne dediščine spada grad {grad_label}?",
		requirements={"grad": {"type": "grad"}},
		path=[
			GraphPathStep(edge_type="pripada_dediščini", target_node_type="dediščina", source_variable="grad", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	# --- Multi-Hop Retrieval (2+ Hops) ---
	QuestionTemplate(
		template="Kakšna je populacija občine, v kateri leži vrh {vrh_label}?",
		requirements={"vrh": {"type": "vrh"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="vrh", capture_as="mun"),
			GraphPathStep(edge_type="ima_populacijo", target_node_type="populacija", source_variable="mun", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="Kakšna je površina občine, kjer stoji grad {grad_label}?",
		requirements={"grad": {"type": "grad"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="grad", capture_as="mun"),
			GraphPathStep(edge_type="ima_površino", target_node_type="površina", source_variable="mun", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label} km²"
	),
	QuestionTemplate(
		template="V kateri statistični regiji leži vrh {vrh_label}?",
		requirements={"vrh": {"type": "vrh"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="vrh", capture_as="mun"),
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="regija", source_variable="mun", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	),
	QuestionTemplate(
		template="V kateri statistični regiji stoji grad {grad_label}?",
		requirements={"grad": {"type": "grad"}},
		path=[
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="občina", source_variable="grad", capture_as="mun"),
			GraphPathStep(edge_type="se_nahaja_v", target_node_type="regija", source_variable="mun", capture_as="odgovor")
		],
		answer_variable="odgovor",
		answer_pattern="{target_label}"
	)
]