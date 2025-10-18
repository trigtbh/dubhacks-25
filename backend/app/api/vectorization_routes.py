from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import numpy as np
from datetime import datetime
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(prefix="/api/v1/users", tags=["User Vectorization & Clustering"])

# ============================================================================
# Pydantic Models
# ============================================================================

class UserAttributes(BaseModel):
    """User attributes that will be converted to vectors"""
    user_id: str
    skills: List[str] = Field(..., description="List of user skills")
    interests: List[str] = Field(..., description="List of user interests")
    hobbies: List[str] = Field(default_factory=list, description="List of user hobbies")
    vibe: str = Field(default="", description="User vibe or personality type")
    comfort: List[str] = Field(default_factory=list, description="Comfort level and preferences")
    availability: str = Field(default="", description="User availability (e.g., weekdays, weekends, flexible)")

class UserAttributesRequest(BaseModel):
    """Request to vectorize user attributes"""
    users: List[UserAttributes] = Field(..., description="List of users with their attributes")

class VectorizedUser(BaseModel):
    """Response containing vectorized user data"""
    user_id: str
    vector: List[float]
    attributes: UserAttributes
    vector_dimension: int

class VectorizeResponse(BaseModel):
    """Response for vectorization endpoint"""
    vectorized_users: List[VectorizedUser]
    vector_dimension: int
    timestamp: str

class ClusterRequest(BaseModel):
    """Request to cluster users based on their attributes"""
    users: List[UserAttributes] = Field(..., description="List of users to cluster")
    num_clusters: int = Field(default=3, description="Number of clusters")
    min_interest_overlap: float = Field(default=0.0, description="Minimum similarity threshold (0-1)")

class UserCluster(BaseModel):
    """A cluster containing users"""
    cluster_id: int
    user_ids: List[str]
    size: int
    common_interests: List[str] = Field(default_factory=list, description="Interests shared by users in this cluster")
    similarity_score: float = Field(default=0.0, description="Average similarity within cluster")

class ClusterResponse(BaseModel):
    """Response for clustering endpoint"""
    clusters: List[UserCluster]
    num_clusters: int
    total_users: int
    clustering_method: str
    timestamp: str

class SimilarUsersRequest(BaseModel):
    """Request to find similar users"""
    user: UserAttributes = Field(..., description="Reference user")
    all_users: List[UserAttributes] = Field(..., description="Pool of users to compare against")
    top_k: int = Field(default=5, description="Number of most similar users to return")

class SimilarUser(BaseModel):
    """Similar user with similarity score"""
    user_id: str
    similarity_score: float
    shared_interests: List[str]

class SimilarUsersResponse(BaseModel):
    """Response for finding similar users"""
    reference_user_id: str
    similar_users: List[SimilarUser]
    timestamp: str

# ============================================================================
# Helper Functions
# ============================================================================

def _create_user_text_representation(user: UserAttributes) -> str:
    """
    Convert user attributes into a text representation for vectorization.
    This helps in creating meaningful embeddings.
    """
    parts = []
    
    # Add skills with high weight
    if user.skills:
        parts.extend(user.skills * 3)  # Repeat skills for higher weight
    
    # Add interests with high weight
    if user.interests:
        parts.extend(user.interests * 3)  # Repeat interests for higher weight
    
    # Add hobbies with medium weight
    if user.hobbies:
        parts.extend(user.hobbies * 2)  # Repeat hobbies for higher weight
    
    # Add vibe
    if user.vibe:
        parts.extend([user.vibe] * 2)  # Repeat vibe for medium weight
    
    # Add comfort preferences
    if user.comfort:
        parts.extend(user.comfort * 2)  # Repeat comfort for higher weight
    
    # Add availability
    if user.availability:
        parts.append(user.availability)
    
    return " ".join(parts) if parts else "no attributes"

def _extract_common_interests(user1: UserAttributes, user2: UserAttributes) -> List[str]:
    """Extract common interests between two users"""
    interests1 = set(user1.interests) if user1.interests else set()
    interests2 = set(user2.interests) if user2.interests else set()
    return list(interests1.intersection(interests2))

def _calculate_user_similarity(user1: UserAttributes, user2: UserAttributes) -> float:
    """Calculate similarity between two users based on their attributes"""
    if user1.user_id == user2.user_id:
        return 1.0
    
    similarity_scores = []
    
    # Interests similarity
    if user1.interests and user2.interests:
        interests1 = set(user1.interests)
        interests2 = set(user2.interests)
        intersection = len(interests1.intersection(interests2))
        union = len(interests1.union(interests2))
        if union > 0:
            similarity_scores.append(intersection / union)  # Jaccard similarity
    
    # Skills similarity
    if user1.skills and user2.skills:
        skills1 = set(user1.skills)
        skills2 = set(user2.skills)
        intersection = len(skills1.intersection(skills2))
        union = len(skills1.union(skills2))
        if union > 0:
            similarity_scores.append(intersection / union)
    
    if similarity_scores:
        return np.mean(similarity_scores)
    return 0.0

# ============================================================================
# Endpoints
# ============================================================================

@router.post("/vectorize", response_model=VectorizeResponse)
async def vectorize_users(request: UserAttributesRequest):
    """
    Convert user attributes into vector representations using TF-IDF vectorization.
    
    This endpoint takes a list of users with their attributes (interests, skills, bio, preferences)
    and converts them into numerical vectors that can be used for clustering and similarity analysis.
    
    Args:
        request: UserAttributesRequest containing list of users
        
    Returns:
        VectorizeResponse with vectorized users and vector dimensions
    """
    try:
        if not request.users or len(request.users) == 0:
            raise HTTPException(status_code=400, detail="At least one user is required")
        
        # Create text representations for each user
        user_texts = [_create_user_text_representation(user) for user in request.users]
        
        # Vectorize using TF-IDF
        vectorizer = TfidfVectorizer(max_features=100, lowercase=True, stop_words='english')
        vectors = vectorizer.fit_transform(user_texts).toarray()
        
        # Create response with vectorized users
        vectorized_users = []
        for i, user in enumerate(request.users):
            vector_list = vectors[i].tolist()
            vectorized_users.append(VectorizedUser(
                user_id=user.user_id,
                vector=vector_list,
                attributes=user,
                vector_dimension=len(vector_list)
            ))
        
        return VectorizeResponse(
            vectorized_users=vectorized_users,
            vector_dimension=vectors.shape[1],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vectorization failed: {str(e)}")


@router.post("/cluster", response_model=ClusterResponse)
async def cluster_users(request: ClusterRequest):
    """
    Cluster users based on their interests and attributes using K-Means clustering.
    
    This endpoint groups users with similar interests together. It uses the user attributes
    to create vectors and then applies K-Means clustering to find groups of similar users.
    
    Args:
        request: ClusterRequest containing users and clustering parameters
        
    Returns:
        ClusterResponse with cluster assignments and statistics
    """
    try:
        if not request.users or len(request.users) == 0:
            raise HTTPException(status_code=400, detail="At least one user is required")
        
        if request.num_clusters < 1:
            raise HTTPException(status_code=400, detail="num_clusters must be at least 1")
        
        if request.num_clusters > len(request.users):
            raise HTTPException(
                status_code=400, 
                detail=f"num_clusters ({request.num_clusters}) cannot exceed number of users ({len(request.users)})"
            )
        
        # Create text representations and vectorize
        user_texts = [_create_user_text_representation(user) for user in request.users]
        vectorizer = TfidfVectorizer(max_features=100, lowercase=True, stop_words='english')
        vectors = vectorizer.fit_transform(user_texts).toarray()
        
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=request.num_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(vectors)
        
        # Group users by cluster
        clusters_dict = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters_dict:
                clusters_dict[label] = []
            clusters_dict[label].append(idx)
        
        # Calculate cluster statistics and create response
        user_clusters = []
        for cluster_id, user_indices in clusters_dict.items():
            cluster_user_ids = [request.users[i].user_id for i in user_indices]
            
            # Get cluster vectors
            cluster_vectors = vectors[user_indices]
            
            # Calculate average pairwise similarity within cluster
            if len(user_indices) > 1:
                similarities = cosine_similarity(cluster_vectors)
                # Get upper triangle values (pairwise similarities)
                upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]
                avg_similarity = float(np.mean(upper_triangle)) if len(upper_triangle) > 0 else 0.0
            else:
                avg_similarity = 1.0
            
            # Find common interests
            common_interests = []
            if len(user_indices) > 0:
                all_interests = [request.users[i].interests for i in user_indices]
                if all_interests:
                    # Find interests common to all users in cluster
                    common = set(all_interests[0]) if all_interests[0] else set()
                    for interests in all_interests[1:]:
                        common = common.intersection(set(interests) if interests else set())
                    common_interests = list(common)
            
            user_clusters.append(UserCluster(
                cluster_id=int(cluster_id),
                user_ids=cluster_user_ids,
                size=len(cluster_user_ids),
                common_interests=common_interests,
                similarity_score=avg_similarity
            ))
        
        return ClusterResponse(
            clusters=user_clusters,
            num_clusters=request.num_clusters,
            total_users=len(request.users),
            clustering_method="K-Means with TF-IDF vectorization",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clustering failed: {str(e)}")


@router.post("/find-similar", response_model=SimilarUsersResponse)
async def find_similar_users(request: SimilarUsersRequest):
    """
    Find users with similar interests to a reference user.
    
    This endpoint compares a reference user against a pool of users and returns
    the top K most similar users based on their attributes.
    
    Args:
        request: SimilarUsersRequest containing reference user and user pool
        
    Returns:
        SimilarUsersResponse with ranked similar users
    """
    try:
        if not request.all_users or len(request.all_users) == 0:
            raise HTTPException(status_code=400, detail="At least one user to compare against is required")
        
        if request.top_k < 1:
            raise HTTPException(status_code=400, detail="top_k must be at least 1")
        
        # Calculate similarity with all users
        similarities = []
        for other_user in request.all_users:
            if other_user.user_id == request.user.user_id:
                continue  # Skip the reference user itself
            
            similarity_score = _calculate_user_similarity(request.user, other_user)
            shared_interests = _extract_common_interests(request.user, other_user)
            
            similarities.append(SimilarUser(
                user_id=other_user.user_id,
                similarity_score=similarity_score,
                shared_interests=shared_interests
            ))
        
        # Sort by similarity score and get top K
        similarities.sort(key=lambda x: x.similarity_score, reverse=True)
        top_similar = similarities[:request.top_k]
        
        return SimilarUsersResponse(
            reference_user_id=request.user.user_id,
            similar_users=top_similar,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search failed: {str(e)}")


@router.get("/vectorize/status")
async def vectorization_status():
    """Get status of vectorization service"""
    return {
        "service": "User Vectorization & Clustering",
        "status": "operational",
        "capabilities": [
            "User attribute vectorization using TF-IDF",
            "K-Means clustering for user groups",
            "Similarity-based user matching",
            "Interest-based recommendations"
        ],
        "timestamp": datetime.now().isoformat()
    }
