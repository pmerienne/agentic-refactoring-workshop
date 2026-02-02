import pytest
from task_flow_api.model import Task, TaskStatus
from task_flow_api.scoring import TaskScoringService


class TestTaskScoringServiceNormalStatuses:
    """Tests pour capturer le comportement actuel de TaskScoringService avec les statuts normaux."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_status_todo_base_score(self):
        """Test avec TaskStatus.TODO - score base attendu: 100"""
        task = Task(
            id=1,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = 100.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_status_doing_base_score(self):
        """Test avec TaskStatus.DOING - score base attendu: 250"""
        task = Task(
            id=2,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.DOING,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base DOING (250)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = 250.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_status_done_with_completed_true(self):
        """Test avec TaskStatus.DONE et completed=True - score base 500 * 1.5 = 750"""
        task = Task(
            id=3,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.DONE,
            completed=True,
        )
        score = self.service.compute_score(task)
        # Score base DONE (500) * 1.5 (completed)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = 750.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_status_archived_base_score(self):
        """Test avec TaskStatus.ARCHIVED - score base attendu: -50"""
        task = Task(
            id=4,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.ARCHIVED,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base ARCHIVED (-50)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = -50.0
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceConsistentStates:
    """Tests pour capturer le comportement actuel avec les états cohérents."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_done_status_with_completed_true_bonus_multiplier(self):
        """Test avec status=DONE et completed=True: bonus multiplicateur 1.5x"""
        task = Task(
            id=5,
            title="Completed work",
            description="This is a simple description",
            status=TaskStatus.DONE,
            completed=True,
        )
        score = self.service.compute_score(task)
        # Score base DONE (500) * 1.5 (état cohérent: done + completed)
        # Text: "Completed work This is a simple description" = 44 chars
        # (entre 20 et 50, pas de multiplicateur de longueur)
        expected = 750.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_text_length_sweet_spot_bonus_multiplier(self):
        """Test avec texte de longueur sweet spot (50-200 caractères): bonus 1.3x"""
        # Créer un texte de 100 caractères exactement (dans le sweet spot)
        description = "This is a perfectly sized description to be in the sweet spot range for task scoring."
        task = Task(
            id=6,
            title="Task",
            description=description,
            status=TaskStatus.TODO,
            completed=False,
        )
        # Vérifier que le texte combiné est bien dans le sweet spot
        text = f"{task.title} {task.description}"
        assert (
            50 <= len(text) <= 200
        ), f"Text length {len(text)} not in sweet spot range"

        score = self.service.compute_score(task)
        # Score base TODO (100) * 1.3 (sweet spot 50-200 chars)
        # Text: "Task This is a perfectly sized description..." = 95 chars
        expected = 130.0
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceInconsistentStates:
    """Tests pour capturer le comportement actuel avec les incohérences de statut."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_status_done_but_completed_false_penalty(self):
        """Test avec status=DONE mais completed=False: pénalité 0.3x"""
        task = Task(
            id=100,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.DONE,
            completed=False,  # Incohérence: status DONE mais pas completed
        )
        score = self.service.compute_score(task)
        # Score base DONE (500) * 0.3 (pénalité incohérence)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = 150.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_status_not_done_but_completed_true_penalty(self):
        """Test avec status!=DONE mais completed=True: pénalité 0.5x"""
        task = Task(
            id=101,
            title="Simple task",
            description="A basic description",
            status=TaskStatus.TODO,  # Incohérence: status TODO mais completed=True
            completed=True,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100) * 0.5 (pénalité incohérence)
        # Text: "Simple task A basic description" = 33 chars (entre 20 et 50, aucun multiplicateur)
        expected = 50.0
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceExtremTextLength:
    """Tests pour capturer le comportement actuel avec des longueurs de texte extrêmes."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_very_short_text_penalty(self):
        """Test avec texte très court (< 20 caractères): pénalité 0.6x"""
        # Créer une tâche avec un texte de moins de 20 caractères
        # Utiliser des mots neutres sans mots-clés pour isoler l'effet de la longueur
        task = Task(
            id=200,
            title="Go",  # 2 chars
            description="Shop",  # 4 chars
            status=TaskStatus.TODO,
            completed=False,
        )
        # Vérifier que le texte combiné est bien < 20 caractères
        text = f"{task.title} {task.description}"
        assert len(text) < 20, f"Text length {len(text)} should be < 20"

        score = self.service.compute_score(task)
        # Score base TODO (100) * 0.6 (pénalité texte trop court)
        # Text: "Go Shop" = 7 chars (< 20)
        # Aucun mot-clé détecté
        expected = 60.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_very_long_text_penalty(self):
        """Test avec texte très long (> 500 caractères): pénalité 0.8x"""
        # Créer une tâche avec un texte de plus de 500 caractères
        # Utiliser des mots neutres pour isoler l'effet de la longueur
        long_description = (
            "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
            "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam quis "
            "nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore "
            "eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident sunt "
            "in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis "
            "unde omnis iste natus error sit voluptatem accusantium doloremque laudantium "
            "totam rem aperiam eaque ipsa quae ab illo inventore veritatis et quasi architecto."
        )
        task = Task(
            id=201,
            title="Lorem ipsum dolor sit amet",
            description=long_description,
            status=TaskStatus.TODO,
            completed=False,
        )
        # Vérifier que le texte combiné est bien > 500 caractères
        text = f"{task.title} {task.description}"
        assert len(text) > 500, f"Text length {len(text)} should be > 500"

        score = self.service.compute_score(task)
        # Score base TODO (100) * 0.8 (pénalité texte trop long)
        # Text length > 500 chars
        # Aucun mot-clé détecté
        expected = 80.0
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceUrgentKeywords:
    """Tests pour capturer le comportement actuel avec les mots-clés URGENT (comportement exponentiel)."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_one_urgent_keyword_adds_75_points(self):
        """Test avec 1 mot-clé urgent: score += 1² * 75 = 75"""
        task = Task(
            id=100,
            title="This is urgent",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 1 mot-clé urgent: +75 (1² * 75)
        # Text: "This is urgent A simple description" = 36 chars (entre 20 et 50, aucun multiplicateur)
        expected = 100.0 + 75.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_two_urgent_keywords_adds_300_points(self):
        """Test avec 2 mots-clés urgent: score += 2² * 75 = 300"""
        task = Task(
            id=101,
            title="This is urgent and critical",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 2 mots-clés urgent: +300 (2² * 75)
        # Text: "This is urgent and critical A simple description" = 49 chars (entre 20 et 50, aucun multiplicateur)
        expected = 100.0 + 300.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_three_urgent_keywords_exponential_behavior(self):
        """Test avec 3 mots-clés urgent: score += 3² * 75 = 675 - comportement exponentiel"""
        task = Task(
            id=102,
            title="This is urgent, critical and asap",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 3 mots-clés urgent: +675 (3² * 75)
        # Text: "This is urgent, critical and asap A simple description" = 56 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # (100 + 675) * 1.3
        expected = (100.0 + 675.0) * 1.3
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServicePriorityKeywords:
    """Tests pour capturer le comportement actuel avec les mots-clés PRIORITY (comportement Fibonacci)."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_one_priority_keyword_multiplier_1_1(self):
        """Test avec 1 mot-clé priority: fibonacci_like[0] = 1 → score *= 1.1"""
        task = Task(
            id=200,
            title="This is important",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 1 mot-clé priority: multiplier = fibonacci_like[0] = 1
        # score *= (1 + 1 * 0.1) = score *= 1.1
        # Text: "This is important A simple description" = 39 chars (entre 20 et 50, aucun multiplicateur)
        # 100 * 1.1 = 110.0
        expected = 110.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_three_priority_keywords_multiplier_1_2(self):
        """Test avec 3 mots-clés priority: fibonacci_like[2] = 2 → score *= 1.2"""
        task = Task(
            id=201,
            title="This is important, priority and high",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 3 mots-clés priority: multiplier = fibonacci_like[2] = 2
        # score *= (1 + 2 * 0.1) = score *= 1.2
        # Text: "This is important, priority and high A simple description" = 59 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # 100 * 1.2 * 1.3 = 156.0
        expected = 156.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_seven_or_more_priority_keywords_multiplier_2_3(self):
        """Test avec 7+ mots-clés priority: fibonacci_like[6] = 13 → score *= 2.3 - limite de l'array"""
        task = Task(
            id=202,
            title="This is important, priority, high, crucial, vital, important, priority",
            description="High priority task",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 7+ mots-clés priority: multiplier = fibonacci_like[6] = 13 (limite max de l'array)
        # score *= (1 + 13 * 0.1) = score *= 2.3
        # Text: "This is important, priority, high, crucial, vital, important, priority High priority task" = 90 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # 100 * 2.3 * 1.3 = 299.0
        expected = 299.0
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceComplexityKeywords:
    """Tests pour capturer le comportement actuel avec les mots-clés COMPLEXITY (comportement linéaire)."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_one_complexity_keyword_adds_120_points(self):
        """Test avec 1 mot-clé complexity: score += 1 * 120 = 120"""
        task = Task(
            id=300,
            title="This is complex",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 1 mot-clé complexity: +120 (1 * 120)
        # Text: "This is complex A simple description" = 37 chars (entre 20 et 50, aucun multiplicateur)
        expected = 100.0 + 120.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_three_complexity_keywords_adds_360_points(self):
        """Test avec 3 mots-clés complexity: score += 3 * 120 = 360"""
        task = Task(
            id=301,
            title="This is complex, difficult and challenging",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 3 mots-clés complexity: +360 (3 * 120)
        # Text: "This is complex, difficult and challenging A simple description" = 64 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # (100 + 360) * 1.3 = 598.0
        expected = (100.0 + 360.0) * 1.3
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceTechKeywords:
    """Tests pour capturer le comportement actuel avec les mots-clés TECH (rendements décroissants)."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_one_tech_keyword_diminishing_returns(self):
        """Test avec 1 mot-clé tech: score += 200 / (1 + 1) = 100"""
        task = Task(
            id=400,
            title="Need to fix a problem",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 1 mot-clé tech (fix): +100 (200 / (1 + 1))
        # Text: "Need to fix a problem A simple description" = 43 chars (entre 20 et 50, aucun multiplicateur)
        expected = 100.0 + 100.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_two_tech_keywords_diminishing_returns(self):
        """Test avec 2 mots-clés tech: score += 200 / (1 + 2) = 66.67"""
        task = Task(
            id=401,
            title="Need to fix and refactor code",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 2 mots-clés tech (fix, refactor): +66.67 (200 / (1 + 2))
        # Text: "Need to fix and refactor code A simple description" = 51 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # (100 + 66.67) * 1.3 = 216.67
        expected = 216.67
        assert score == expected, f"Expected {expected}, got {score}"

    def test_five_tech_keywords_diminishing_returns(self):
        """Test avec 5 mots-clés tech: score += 200 / (1 + 5) = 33.33 - diminishing returns"""
        task = Task(
            id=402,
            title="Need to fix bug, refactor to optimize performance",
            description="A simple description",
            status=TaskStatus.TODO,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base TODO (100)
        # 5 mots-clés tech (fix, bug, refactor, optimize, performance): +33.33 (200 / (1 + 5))
        # Text: "Need to fix bug, refactor to optimize performance A simple description" = 72 chars (dans le sweet spot 50-200, multiplicateur 1.3)
        # (100 + 33.33) * 1.3 = 173.33
        expected = 173.33
        assert score == expected, f"Expected {expected}, got {score}"


class TestTaskScoringServiceBusinessKeywords:
    """Tests pour capturer le comportement actuel de TaskScoringService concernant les mots-clés BUSINESS (interaction avec statut)."""

    def setup_method(self):
        self.service = TaskScoringService()

    def test_one_business_keyword_status_doing(self):
        """Test avec 1 mot-clé business et status=DOING: score += 1 * 150"""
        task = Task(
            id=500,
            title="Prepare customer presentation",
            description="A simple description",
            status=TaskStatus.DOING,
            completed=False,
        )
        score = self.service.compute_score(task)
        # Score base DOING (250)
        # 1 mot-clé business (customer) avec status DOING: +150 (1 * 150)
        # Text: "Prepare customer presentation A simple description" = 50 chars (exactement dans le sweet spot 50-200, multiplicateur 1.3)
        # (250 + 150) * 1.3 = 520.0
        expected = 520.0
        assert score == expected, f"Expected {expected}, got {score}"

    def test_one_business_keyword_status_done(self):
        """Test avec 1 mot-clé business et status=DONE: score += 1 * 30"""
        task = Task(
            id=502,
            title="Finalize revenue report",
            description="A simple description",
            status=TaskStatus.DONE,
            completed=True,
        )
        score = self.service.compute_score(task)
        # Score base DONE (500) * 1.5 (done + completed = état cohérent) = 750
        # 1 mot-clé business (revenue) avec status DONE: +30 (1 * 30)
        # Text: "Finalize revenue report A simple description" = 44 chars (entre 20 et 50, pas de multiplicateur)
        # 750 + 30 = 780.0
        expected = 780.0
        assert score == expected, f"Expected {expected}, got {score}"
