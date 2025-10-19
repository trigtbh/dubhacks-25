"""
Vectorization and Clustering Service

This module provides core functionality for user vectorization and clustering
based on user attributes and interests.
"""

from typing import List, Dict, Any, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


class UserVectorizationService:
    """Service for vectorizing and clustering users based on their attributes"""

    def __init__(self, max_features: int = 100):
        """Initialize the vectorization service

        Args:
            max_features: Maximum number of features for TF-IDF vectorization
        """
        self.max_features = max_features
        self.vectorizer = None

    def create_user_text_representation(self, user) -> str:
        """
        Convert user attributes into a text representation for vectorization.
        This helps in creating meaningful embeddings.

        Args:
            user: User object with attributes

        Returns:
            Text representation of user attributes
        """
        parts = []

        # Add specialty with high weight (split by comma if multiple)
        if user.specialty:
            specialties = [s.strip() for s in user.specialty.split(',') if s.strip()]
            parts.extend(specialties * 3)  # Repeat specialties for higher weight

        # Add interests with high weight (split by comma)
        if user.interests:
            interests = [i.strip() for i in user.interests.split(',') if i.strip()]
            parts.extend(interests * 3)  # Repeat interests for higher weight

        # Add field with medium weight (split by comma if multiple)
        if user.field:
            fields = [f.strip() for f in user.field.split(',') if f.strip()]
            parts.extend(fields * 2)  # Repeat fields for medium weight

        # Add vibe
        if user.vibe:
            parts.extend([user.vibe] * 2)  # Repeat vibe for medium weight

        # Add comfort preferences
        if user.comfort:
            parts.extend([user.comfort] * 2)  # Repeat comfort for higher weight

        # Add previous missions (already a list)
        if user.previous_missions:
            parts.extend(user.previous_missions)

        # Add current mission
        if user.current_mission:
            parts.append(user.current_mission)

        # Add name
        if user.name:
            parts.append(user.name)

        return " ".join(parts) if parts else "no attributes"

    def vectorize_users(self, users: List[Any]) -> tuple:
        """
        Convert user attributes into vector representations using TF-IDF vectorization.

        Args:
            users: List of user objects with attributes

        Returns:
            Tuple of (vectors_array, vectorizer)
        """
        # Create text representations for each user
        user_texts = [self.create_user_text_representation(user) for user in users]

        # Vectorize using TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            lowercase=True,
            stop_words='english'
        )
        vectors = self.vectorizer.fit_transform(user_texts).toarray()

        return vectors, self.vectorizer

    def cluster_users(self, users: List[Any], vectors: np.ndarray, num_clusters: int) -> Dict[int, List[int]]:
        """
        Cluster users based on their vector representations using K-Means.

        Args:
            users: List of user objects
            vectors: Vector representations of users
            num_clusters: Number of clusters to create

        Returns:
            Dictionary mapping cluster_id to list of user indices
        """
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(vectors)

        # Group users by cluster
        clusters_dict = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters_dict:
                clusters_dict[label] = []
            clusters_dict[label].append(idx)

        return clusters_dict

    def calculate_cluster_similarity(self, cluster_vectors: np.ndarray) -> float:
        """
        Calculate average pairwise similarity within a cluster.

        Args:
            cluster_vectors: Vectors for users in the cluster

        Returns:
            Average similarity score within the cluster
        """
        if len(cluster_vectors) <= 1:
            return 1.0

        similarities = cosine_similarity(cluster_vectors)
        # Get upper triangle values (pairwise similarities)
        upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]
        return float(np.mean(upper_triangle)) if len(upper_triangle) > 0 else 0.0

    def find_common_interests(self, users_in_cluster: List[Any]) -> List[str]:
        """
        Find interests common to all users in a cluster.

        Args:
            users_in_cluster: List of user objects in the cluster

        Returns:
            List of interests common to all users
        """
        if not users_in_cluster:
            return []

        all_interests_sets = []
        for user in users_in_cluster:
            user_interests = set(i.strip() for i in user.interests.split(',') if i.strip()) if user.interests else set()
            all_interests_sets.append(user_interests)

        if not all_interests_sets:
            return []

        # Find interests common to all users in cluster
        common = all_interests_sets[0]
        for interests_set in all_interests_sets[1:]:
            common = common.intersection(interests_set)

        return list(common)

    def calculate_user_similarity(self, user1: Any, user2: Any) -> float:
        """
        Calculate similarity between two users based on their attributes.

        Args:
            user1: First user object
            user2: Second user object

        Returns:
            Similarity score between 0 and 1
        """
        if user1.uuid == user2.uuid:
            return 1.0

        similarity_scores = []

        # Interests similarity
        if user1.interests and user2.interests:
            interests1 = set(i.strip() for i in user1.interests.split(',') if i.strip())
            interests2 = set(i.strip() for i in user2.interests.split(',') if i.strip())
            intersection = len(interests1.intersection(interests2))
            union = len(interests1.union(interests2))
            if union > 0:
                similarity_scores.append(intersection / union)  # Jaccard similarity

        # Specialties similarity
        if user1.specialty and user2.specialty:
            specialties1 = set(s.strip() for s in user1.specialty.split(',') if s.strip())
            specialties2 = set(s.strip() for s in user2.specialty.split(',') if s.strip())
            intersection = len(specialties1.intersection(specialties2))
            union = len(specialties1.union(specialties2))
            if union > 0:
                similarity_scores.append(intersection / union)

        # Field similarity
        if user1.field and user2.field:
            fields1 = set(f.strip() for f in user1.field.split(',') if f.strip())
            fields2 = set(f.strip() for f in user2.field.split(',') if f.strip())
            intersection = len(fields1.intersection(fields2))
            union = len(fields1.union(fields2))
            if union > 0:
                similarity_scores.append(intersection / union)

        if similarity_scores:
            return np.mean(similarity_scores)
        return 0.0

    def extract_common_interests(self, user1: Any, user2: Any) -> List[str]:
        """
        Extract common interests between two users.

        Args:
            user1: First user object
            user2: Second user object

        Returns:
            List of common interests
        """
        interests1 = set(i.strip() for i in user1.interests.split(',') if i.strip()) if user1.interests else set()
        interests2 = set(i.strip() for i in user2.interests.split(',') if i.strip()) if user2.interests else set()
        return list(interests1.intersection(interests2))