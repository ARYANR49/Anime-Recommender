import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_root)


from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY,MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

# class AnimeRecommendationPipeline:
#     def __init__(self,persist_dir="FAISS_index"):
#         try:
#             logger.info("Intializing Recommdation Pipeline")

#             # vector_builder = VectorStoreBuilder(csv_path="" , persist_dir=persist_dir)

#             vs = VectorStoreBuilder(csv_path="",persist_dir=persist_dir)
#             # if vs.csv_path:
#             #  vs.build_and_save_vectorstore()
            
#             retriever = vs.load_vector_store().as_retriever()

#             # retriever = vector_builder.load_vector_store().as_retriever()

#             self.recommender = AnimeRecommender(retriever,GROQ_API_KEY,MODEL_NAME)

#             logger.info("Pipleine intialized sucesfully...")

#         except Exception as e:
#             logger.error(f"Failed to intialize pipeline {str(e)}")
#             raise CustomException("Error during pipeline intialization" , e)
        
#     def recommend(self,query:str) -> str:
#         try:
#             logger.info(f"Recived a query {query}")

#             recommendation = self.recommender.get_recommendation(query)

#             logger.info("Recommendation generated sucesfulyy...")
#             return recommendation
#         except Exception as e:
#             logger.error(f"Failed to get recommendation {str(e)}")
#             raise CustomException("Error during getting recommendation" , e)
        


        
class AnimeRecommendationPipeline:
    def __init__(self, persist_dir=os.path.abspath("FAISS_index")):
        try:
            logger.info("Initializing Recommendation Pipeline")

            csv_path = "data/anime_updated.csv"
            vs = VectorStoreBuilder(csv_path=csv_path, persist_dir=persist_dir)

            faiss_index_file = os.path.join(persist_dir, "index.faiss")
            if not os.path.exists(faiss_index_file):
                logger.info("FAISS index not found. Building vector store...")
                vs.build_and_save_vectorstore()
            else:
                logger.info("FAISS index found. Skipping build.")

            retriever = vs.load_vector_store().as_retriever()

            self.recommender = AnimeRecommender(retriever, GROQ_API_KEY, MODEL_NAME)
            logger.info("Pipeline initialized successfully...")

        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise CustomException("Error during pipeline initialization", e)

    def recommend(self, query: str) -> str:
        try:
            logger.info(f"Received a query: {query}")
            recommendation = self.recommender.get_recommendation(query)
            logger.info("Recommendation generated successfully.")
            return recommendation
        except Exception as e:
            logger.error(f"Failed to get recommendation: {str(e)}")
            raise CustomException("Error during getting recommendation", e)
