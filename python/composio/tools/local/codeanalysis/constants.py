import os
from pathlib import Path



# TMP_FOLDER_FOR_PYTHON = "./tmp"
TMP_FOLDER_FOR_PYTHON = os.path.join(Path.home(), ".composio/tmp")
DIR_FOR_FQDN_CACHE = os.path.join(TMP_FOLDER_FOR_PYTHON, "FQDN_CACHE")
DIR_FOR_TOOL_INFO_CACHE = os.path.join(TMP_FOLDER_FOR_PYTHON, "TOOL_INFO_CACHE")
DEEPLAKE_FOLDER = os.path.join(TMP_FOLDER_FOR_PYTHON, "deeplake")
TREE_SITTER_CACHE = os.path.join(TMP_FOLDER_FOR_PYTHON, "tree_sitter_cache")
EMBEDDER = "sentence-transformers/all-mpnet-base-v2"
