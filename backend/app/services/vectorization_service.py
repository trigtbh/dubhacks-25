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

        # Specialty and fields (skill-like)
        if getattr(user, 'specialty', None):
            specialty_items = [s.strip() for s in user.specialty.split(',') if s.strip()]
            parts.extend(specialty_items * 3)

        if getattr(user, 'fields', None):
            fields_items = [s.strip() for s in user.fields.split(',') if s.strip()]
            parts.extend(fields_items * 2)

        # Interests and hobbies combined
        if getattr(user, 'interests_and_hobbies', None):
            interests_items = [i.strip() for i in user.interests_and_hobbies.split(',') if i.strip()]
            parts.extend(interests_items * 3)

        # Vibe
        if getattr(user, 'vibe', None):
            parts.extend([user.vibe] * 2)

        # Comfort preferences
        if getattr(user, 'comfort', None):
            comfort_items = [c.strip() for c in user.comfort.split(',') if c.strip()]
            parts.extend(comfort_items * 2)

        # Name and handle as context
        if getattr(user, 'name', None):
            parts.append(user.name)
        if getattr(user, 'handle', None):
            parts.append(user.handle)

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
            user_interests = set(i.strip() for i in (getattr(user, 'interests_and_hobbies', '') or '').split(',') if i.strip())
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

        # Interests/hobbies similarity
        interests1 = set(i.strip() for i in (getattr(user1, 'interests_and_hobbies', '') or '').split(',') if i.strip())
        interests2 = set(i.strip() for i in (getattr(user2, 'interests_and_hobbies', '') or '').split(',') if i.strip())
        if interests1 and interests2:
            intersection = len(interests1.intersection(interests2))
            union = len(interests1.union(interests2))
            if union > 0:
                similarity_scores.append(intersection / union)

        # Specialty/fields similarity
        specs1 = set(s.strip() for s in (getattr(user1, 'specialty', '') or '').split(',') if s.strip())
        specs1.update(s.strip() for s in (getattr(user1, 'fields', '') or '').split(',') if s.strip())
        specs2 = set(s.strip() for s in (getattr(user2, 'specialty', '') or '').split(',') if s.strip())
        specs2.update(s.strip() for s in (getattr(user2, 'fields', '') or '').split(',') if s.strip())
        if specs1 and specs2:
            intersection = len(specs1.intersection(specs2))
            union = len(specs1.union(specs2))
            if union > 0:
                similarity_scores.append(intersection / union)

        # Comfort similarity
        if getattr(user1, 'comfort', None) and getattr(user2, 'comfort', None):
            comforts1 = set(c.strip() for c in user1.comfort.split(',') if c.strip())
            comforts2 = set(c.strip() for c in user2.comfort.split(',') if c.strip())
            intersection = len(comforts1.intersection(comforts2))
            union = len(comforts1.union(comforts2))
            if union > 0:
                similarity_scores.append(intersection / union)

        if similarity_scores:
            return float(np.mean(similarity_scores))
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
        interests1 = set(i.strip() for i in (getattr(user1, 'interests_and_hobbies', '') or '').split(',') if i.strip())
        interests2 = set(i.strip() for i in (getattr(user2, 'interests_and_hobbies', '') or '').split(',') if i.strip())
        return list(interests1.intersection(interests2))