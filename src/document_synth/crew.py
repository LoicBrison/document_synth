import os
from document_synth.tools.custom_file_reader import *
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    BraveSearchTool,
	DirectoryReadTool,
    FileReadTool
)


docs_tool = DirectoryReadTool(directory='E:/Documents/TEDIES/travaux 2024/document_synth/src/document_synth/data')
file_tool = CustomFileReader()
web_rag_tool = BraveSearchTool()


@CrewBase
class DocumentSynth():
	"""Automatisation de la synthèse et génération de documents"""
	
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def explorateur_documents(self) -> Agent:
		return Agent(
            config=self.agents_config['explorateur_documents'],
            verbose=True,
			tools=[docs_tool,file_tool]
        )

	@agent
	def synthetiseur(self) -> Agent:
		return Agent(
			config=self.agents_config['synthetiseur'],
			verbose=True,
			tools=[docs_tool,file_tool]
		)

	@agent
	def generateur_contenu(self) -> Agent:
		return Agent(
			config=self.agents_config['generateur_contenu'],
			verbose=True,
			tools=[docs_tool,file_tool]
		)

	@agent
	def verificateur(self) -> Agent:
		return Agent(
			config=self.agents_config['verificateur'],
			verbose=True,
			tools=[docs_tool,file_tool]
		)

	@task
	def classification_documents(self) -> Task:
		return Task(
			config=self.tasks_config['classification_documents'],
		)

	@task
	def synthese_documents(self) -> Task:
		return Task(
			config=self.tasks_config['synthese_documents'],
		)

	@task
	def generation_contenu(self) -> Task:
		return Task(
			config=self.tasks_config['generation_contenu'],
		)

	@task
	def verification_contenu(self) -> Task:
		"""Tâche de vérification et sauvegarde des documents générés"""

		def save_output(output_dir, filename, content, category):
			"""Enregistre le fichier dans la bonne catégorie"""
			filepath = os.path.join(output_dir, category, f"{filename}.md")
			with open(filepath, "w", encoding="utf-8") as file:
				file.write(content)
			print(f"✅ Fichier enregistré : {filepath}")

		def process_verification(inputs):
			"""Vérifie le contenu et l'enregistre dans le bon dossier"""
			category = inputs.get("category", "Autres")
			filename = inputs.get("filename", "document")
			content = inputs.get("content", "")
			output_dir = 'E:/Documents/TEDIES/travaux 2024/document_synth/output'

			# Vérification du texte (on peut rajouter d'autres filtres ici)
			content = content.replace("erreur", "correction")  # Exemple simple de correction

			save_output(output_dir, filename, content, category)

		return Task(
			config=self.tasks_config['verification_contenu'],
			# action=process_verification
			output_file="report.md"
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)