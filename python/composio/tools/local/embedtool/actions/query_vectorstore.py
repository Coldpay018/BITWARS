from pathlib import Path

from pydantic import BaseModel, Field

from composio.tools.local.base import Action


class QueryImageVectorStoreInputSchema(BaseModel):
    search_query: str = Field(..., description="Search query to retrieve the image")
    indexed_directory: str = Field(
        ...,
        description="Directory path that was indexed for image search",
    )
    max_results: int = Field(..., description="Maximum number of results to return")


class QueryImageVectorStoreOutputSchema(BaseModel):
    result: str = Field(..., description="Status of the image retrieval")
    image_paths: list[str] = Field(..., description="List of retrieved image file paths")


class QueryImageVectorStore(Action):
    """
    Query Vector Store for images
    """

    _display_name = "Query Image Vector Store"
    _request_schema = QueryImageVectorStoreInputSchema
    _response_schema = QueryImageVectorStoreOutputSchema
    _tags = ["query_image_embeddings"]
    _tool_name = "embedtool"

    def execute(
        self,
        request_data: QueryImageVectorStoreInputSchema,
        authorisation_data: dict = {},
    ) -> QueryImageVectorStoreOutputSchema:
        import chromadb
        from chromadb.utils import embedding_functions

        image_collection_name = Path(request_data.indexed_directory).name + "_images"
        index_storage_path = Path.home() / ".composio" / "image_index_storage"
        chroma_client = chromadb.PersistentClient(path=str(index_storage_path))
        chroma_collection = chroma_client.get_collection(image_collection_name)

        text_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="distiluse-base-multilingual-cased-v2")
        query_embeddings = text_embedding_function([request_data.search_query])

        search_results = chroma_collection.query(
            query_texts=request_data.search_query,
            n_results=request_data.max_results,
        )
        if search_results is None:
            return QueryImageVectorStoreOutputSchema(result="No images found", image_paths=[])

        retrieved_image_paths = [result["file_path"] for result in search_results["metadatas"][0]]

        return QueryImageVectorStoreOutputSchema(result="Images successfully retrieved", image_paths=retrieved_image_paths)
<<<<<<< HEAD
=======

>>>>>>> 290719188e128b7c686b0c042afc13318fe1022c
