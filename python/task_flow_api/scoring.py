from typing import List
from task_flow_api.model import Task, TaskStatus
import re


class TaskScoringService:
    STATUS_BASE_SCORES = {
        TaskStatus.TODO: 100,
        TaskStatus.DOING: 250,
        TaskStatus.DONE: 500,
        TaskStatus.ARCHIVED: -50
    }

    URGENT_KEYWORDS = ["urgent", "asap", "critical", "emergency", "now", "immediately"]
    PRIORITY_KEYWORDS = ["important", "priority", "high", "crucial", "vital"]
    COMPLEXITY_KEYWORDS = ["complex", "difficult", "challenging", "hard", "tricky"]
    TECH_KEYWORDS = ["bug", "fix", "refactor", "optimize", "performance", "security"]
    BUSINESS_KEYWORDS = ["revenue", "customer", "client", "deadline", "meeting"]
    NEGATIVE_KEYWORDS = ["maybe", "later", "consider", "think", "discuss", "review"]
    FORBIDDEN_KEYWORDS = ["impossible", "cannot", "blocked", "waiting", "postpone"]

    def compute_score(self, task: Task) -> float:
        score = 0.0
        score += self.STATUS_BASE_SCORES.get(task.status, 0)
        if task.status == TaskStatus.DONE and task.completed:
            score *= 1.5
        elif task.status == TaskStatus.DONE and not task.completed:
            score *= 0.3  # Inconsistent state penalty
        elif task.status != TaskStatus.DONE and task.completed:
            score *= 0.5  # Another inconsistent state

        # Combine title and description for analysis
        text = f"{task.title} {task.description}".lower()

        # Count various keyword categories
        urgent_count = self._count_keywords(text, self.URGENT_KEYWORDS)
        priority_count = self._count_keywords(text, self.PRIORITY_KEYWORDS)
        complexity_count = self._count_keywords(text, self.COMPLEXITY_KEYWORDS)
        tech_count = self._count_keywords(text, self.TECH_KEYWORDS)
        business_count = self._count_keywords(text, self.BUSINESS_KEYWORDS)
        negative_count = self._count_keywords(text, self.NEGATIVE_KEYWORDS)
        forbidden_count = self._count_keywords(text, self.FORBIDDEN_KEYWORDS)

        # Urgent keywords add exponential score
        if urgent_count > 0:
            score += (urgent_count ** 2) * 75

        # Priority keywords multiply by Fibonacci-ish sequence
        if priority_count > 0:
            fibonacci_like = [1, 1, 2, 3, 5, 8, 13]
            multiplier = fibonacci_like[min(priority_count - 1, len(fibonacci_like) - 1)]
            score *= (1 + multiplier * 0.1)

        # Complexity increases score
        if complexity_count > 0:
            score += complexity_count * 120

        # Tech keywords have diminishing returns
        if tech_count > 0:
            score += 200 / (1 + tech_count)  # More keywords = less value each

        # Business keywords interact with status
        if business_count > 0:
            if task.status == TaskStatus.DOING:
                score += business_count * 150
            elif task.status == TaskStatus.TODO:
                score += business_count * 80
            else:
                score += business_count * 30

        # Negative keywords are multiplicative penalties
        if negative_count > 0:
            score *= (0.7 ** negative_count)  # Each negative word reduces by 30%

        # Forbidden keywords have severe impact
        if forbidden_count > 0:
            score -= forbidden_count * 300
            if forbidden_count >= 3:
                score *= 0.1  # Catastrophic penalty

        text_length = len(text)
        if text_length < 20:
            score *= 0.6  # Too short, probably not serious
        elif text_length > 500:
            score *= 0.8  # Too long, probably rambling
        elif 50 <= text_length <= 200:
            score *= 1.3  # Sweet spot

        # Special character analysis
        special_chars = len(re.findall(r'[!@#$%^&*()]', text))
        if special_chars > 5:
            score += special_chars * 15  # Emphasis matters
        elif special_chars > 10:
            score *= 0.7  # Too many, seems spammy

        # Final adjustment: ensure score is at least -1000 and at most 10000
        score = max(-1000, min(10000, score))
        return round(score, 2)

    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """Count how many times any of the keywords appear in the text."""
        count = 0
        for keyword in keywords:
            count += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
        return count
