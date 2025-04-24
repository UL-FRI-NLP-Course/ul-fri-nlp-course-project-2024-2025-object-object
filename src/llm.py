import string
import re
from typeguard import typechecked
import torch
from transformers import pipeline

@typechecked
class LLMManager:
	"""
	Manages interactions with a Hugging Face language model,
	maintains conversation history, and provides evaluation capabilities.
	"""
	def __init__(self, model_id: str = "cjvt/GaMS-1B-Chat"):
		"""
		Initializes the LLMManager.

		Args:
			model_id (str): The Hugging Face model ID to load.
		"""
		self.model_id = model_id
		self.__history = [] # Stores conversation history [{role: 'user', content: '...'}, {role: 'assistant', content: '...'}]
		self.llm_pipeline = None
		self._load_model()

	def _load_model(self):
		"""Loads the tokenizer and model pipeline."""
		if torch.backends.mps.is_available():
			device = torch.device("mps")
		elif torch.cuda.is_available():
			device = torch.device("cuda")
		else:
			device = torch.device("cpu")

		# For chat models, using the pipeline is often easier as it handles formatting.
		# Trust remote code if necessary for this specific model architecture
		self.llm_pipeline = pipeline(
			"text-generation",
			model=self.model_id,
			torch_dtype=torch.bfloat16 if device.type != 'mps' else torch.float16, # bfloat16 often faster, but check compatibility. float16 for MPS.
			device=device, # Explicitly set device
		)

	def ask(self, prompt: str) -> str:
		"""
		Sends a prompt to the LLM and gets a response.

		Args:
			prompt (str): The user's input prompt.

		Returns:
			str: The LLM's generated response, or an error message.
		"""

		current_interaction = [{"role": "user", "content": prompt}]
		messages = self.__history + current_interaction

		response = self.llm_pipeline(messages, max_new_tokens=500)
		generated_text = response[0]['generated_text']
		assistant_response = generated_text[-1]['content']

		self.__history.append({"role": "user", "content": prompt})
		self.__history.append({"role": "assistant", "content": assistant_response})

		return assistant_response

	@property
	def history(self) -> list:
		"""Returns the current conversation history."""
		return self.__history.copy() # Return a copy to prevent external modification

	def clear_history(self):
		"""Clears the conversation history."""
		self.__history = []

if __name__ == "__main__":
	llm = LLMManager(model_id="cjvt/GaMS-1B-Chat")

	# First interaction
	prompt1 = "Kdo je France Prešeren?"
	print(f"User: {prompt1}")
	response1 = llm.ask(prompt1)
	print(f"LLM: {response1}")

	# Second interaction (model remembers the context via history)
	prompt2 = "Kje je bil rojen?"
	print(f"User: {prompt2}")
	response2 = llm.ask(prompt2)
	print(f"LLM: {response2}")