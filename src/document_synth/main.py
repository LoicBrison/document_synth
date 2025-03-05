#!/usr/bin/env python
import sys, os
import warnings

from datetime import datetime

from document_synth.crew import DocumentSynth

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Exécute le CrewAI pour traiter les documents.
    """

    INPUT_DIR = "data/"
    OUTPUT_DIR = "output/"
    folders = [
        "Analyse et statistiques",
        "Données et stockage",
        "Expérimentation et mise en pratique",
        "LLM RAG Fiabilité et évaluation",
        "LLM RAG Infrastructure et mise en place",
        "Optimisation gestion et veille",
        "Sentence Transformers - Utilisation et Optimisation"
    ]

    for folder in folders:
        os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

    inputs = {
        'base_path': INPUT_DIR,
        'output_path': OUTPUT_DIR,
    }
    DocumentSynth().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
