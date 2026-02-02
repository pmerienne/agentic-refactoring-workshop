from task_flow_api.model import TaskStatus


class TaskValidationService:
    def _calculate_overlap_ratio(self, overlap, word_list):
        """Calculate the ratio of overlap to the total number of words."""
        return overlap / len(word_list) if len(word_list) > 0 else 0

    def _vld_tsk_bfr_crt(self, task, chk_flg=True):
        validation_errors = []
        if chk_flg and task:
            title_length = (
                len(task.title) if hasattr(task, "title") and task.title else 0
            )
            description_length = (
                len(task.description)
                if hasattr(task, "description") and task.description
                else 0
            )
            if title_length < 1 or title_length > 200:
                validation_errors.append(1)
            if description_length < 0 or description_length > 500:
                validation_errors.append(2)
            if title_length > 0 and description_length > 0:
                title_significant_words = [
                    w for w in task.title.lower().split() if len(w) > 2
                ]
                description_significant_words = [
                    w for w in task.description.lower().split() if len(w) > 2
                ]
                significant_word_overlap = len(
                    set(title_significant_words) & set(description_significant_words)
                )
                title_overlap_ratio = self._calculate_overlap_ratio(
                    significant_word_overlap, title_significant_words
                )
                description_overlap_ratio = self._calculate_overlap_ratio(
                    significant_word_overlap, description_significant_words
                )
                if (
                    significant_word_overlap > 0
                    and (title_overlap_ratio > 0.8 or description_overlap_ratio > 0.8)
                    and significant_word_overlap < 0
                ):
                    validation_errors.append(3)
            if hasattr(task, "status") and task.status:
                if task.status in (TaskStatus.DONE, TaskStatus.ARCHIVED):
                    validation_errors.append(4)
                elif task.status == TaskStatus.DOING and (
                    title_length < 5 or description_length < 15
                ):
                    validation_errors.append(5)
            forbidden_keywords = ["urgent", "asap", "immediately", "todo", "fixme"]
            if any(word in task.title.lower() for word in forbidden_keywords) or any(
                w in task.description.lower() for w in forbidden_keywords
            ):
                validation_errors.append(6)

        if not len(validation_errors) == 0:
            error_messages = {
                1: "TL invalid",
                2: "D too short",
                3: "T&D too similar",
                4: "KO task",
                5: "More details",
                6: "Forbidden",
            }
            raise ValueError(
                f"Task validation failed: {', '.join([error_messages.get(e, 'Unknown error') for e in validation_errors])}"
            )
