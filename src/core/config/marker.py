from marker.config.parser import ConfigParser

from .env import env

default_config = {
    "output_format": "markdown",
    "use_llm": False,
    "max_concurrency": 10,
    "timeout": 180,
    "max_retries": 5,
    "retry_wait_time": 10,
    "gemini_model_name": "gemini-2.0-flash",
    "gemini_api_key": env.gemini_api_key,
    "extract_images": True,
    # "pdftext_workers":7,
    # "TableProcessor_pdftext_workers": 7,
    # "DocumentProvider_pdftext_workers": 7,
    # "PdfProvider_pdftext_workers": 7,
    # "EpubProvider_pdftext_workers": 7,
    # "PowerPointProvider_pdftext_workers": 7,
    # "SpreadSheetProvider_pdftext_workers": 7,
}


def create_marker_config_parser(config: dict) -> ConfigParser:
    merged_config = default_config.copy()
    merged_config.update(config)
    config_parser = ConfigParser(merged_config)
    return config_parser


# TODO: The docs on the github repo metions about --workers, but I don't see it in the cli_options.txt
# https://github.com/datalab-to/marker?tab=readme-ov-file#convert-multiple-files
# RE: so that is wrong, and one should use --pdftext_workers

# Convert multiple files
# marker /path/to/input/folder
# marker supports all the same options from marker_single above.
# --workers is the number of conversion workers to run simultaneously.
# This is automatically set by default, but you can increase it to increase throughput, at the cost of more CPU/GPU usage. Marker will use 5GB of VRAM per worker at the peak, and 3.5GB average.
# Convert multiple files on multiple GPUs
# NUM_DEVICES=4 NUM_WORKERS=15 marker_chunk_convert ../pdf_in ../md_out
# NUM_DEVICES is the number of GPUs to use. Should be 2 or greater.
# NUM_WORKERS is the number of parallel processes to run on each GPU.


# TODO: Additional configs, that seem useful (all listed in cli_options.txt)
# enable_table_ocr
# max_concurrency INTEGER
#   --use_llm                       Whether to use LLMs to improve accuracy.
#                                   Default is False
#   --table_merge_prompt TEXT
#   --pdftext_workers

#   --timeout INTEGER               The timeout to use for the service. Default
#                                   is 30. (Applies to: AzureOpenAIService,
#                                   ClaudeService, GoogleGeminiService,
#                                   OllamaService, OpenAIService,
#                                   GoogleVertexService)
#   --max_retries INTEGER           The maximum number of retries to use for the
#                                   service. Default is 2. (Applies to:
#                                   AzureOpenAIService, ClaudeService,
#                                   GoogleGeminiService, OllamaService,
#                                   OpenAIService, GoogleVertexService)
#   --retry_wait_time INTEGER       The wait time between retries. Default is 3.
#                                   (Applies to: AzureOpenAIService,
#                                   ClaudeService, GoogleGeminiService,
#                                   OllamaService, OpenAIService,
#                                   GoogleVertexService)
#   --azure_endpoint TEXT           The Azure OpenAI endpoint URL. No trailing
#                                   slash. Default is None. (Applies to:
#                                   AzureOpenAIService)
#   --azure_api_key TEXT            The API key to use for the Azure OpenAI
#                                   service. Default is None. (Applies to:
#                                   AzureOpenAIService)
#   --azure_api_version TEXT        The Azure OpenAI API version to use. Default
#                                   is None. (Applies to: AzureOpenAIService)
#   --deployment_name TEXT          The deployment name for the Azure OpenAI
#                                   model. Default is None. (Applies to:
#                                   AzureOpenAIService)
#   --claude_model_name TEXT        The name of the Google model to use for the
#                                   service. Default is
#                                   claude-3-7-sonnet-20250219. (Applies to:
#                                   ClaudeService)
#   --claude_api_key TEXT           The Claude API key to use for the service.
#                                   Default is None. (Applies to: ClaudeService)
#   --max_claude_tokens INTEGER     The maximum number of tokens to use for a
#                                   single Claude request. Default is 8192.
#                                   (Applies to: ClaudeService)
#   --gemini_model_name TEXT        The name of the Google model to use for the
#                                   service. Default is gemini-2.0-flash.
#                                   (Applies to: GoogleGeminiService,
#                                   GoogleVertexService)
#   --gemini_api_key TEXT           The Google API key to use for the service.
#                                   Default is None. (Applies to:
#                                   GoogleGeminiService)
#   --ollama_base_url TEXT          The base url to use for ollama.  No trailing
#                                   slash. Default is http://localhost:11434.
#                                   (Applies to: OllamaService)
#   --ollama_model TEXT             The model name to use for ollama. Default is
#                                   llama3.2-vision. (Applies to: OllamaService)
#   --openai_base_url TEXT          The base url to use for OpenAI-like models.
#                                   No trailing slash. Default is
#                                   https://api.openai.com/v1. (Applies to:
#                                   OpenAIService)
#   --openai_model TEXT             The model name to use for OpenAI-like model.
#                                   Default is gpt-4o-mini. (Applies to:
#                                   OpenAIService)
#   --openai_api_key TEXT           The API key to use for the OpenAI-like
#                                   service. Default is None. (Applies to:
#                                   OpenAIService)
#   --openai_image_format TEXT      The image format to use for the OpenAI-like
#                                   service. Use 'png' for better compatability
#                                   Default is webp. (Applies to: OpenAIService)
#   --vertex_project_id TEXT        Google Cloud Project ID for Vertex AI.
#                                   Default is None. (Applies to:
#                                   GoogleVertexService)
#   --vertex_location TEXT          Google Cloud Location for Vertex AI. Default
#                                   is us-central1. (Applies to:
#                                   GoogleVertexService)
#   --vertex_dedicated              Whether to use a dedicated Vertex AI
#                                   instance. Default is False. (Applies to:
#                                   GoogleVertexService)
