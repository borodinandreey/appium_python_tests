import allure


class ResponseHelper:

    @staticmethod
    @allure.step("Получение Team ID")
    def get_team_id(responses, index=0):
        for response in responses:
            data_items = response.get("data")
            if 0 <= index < len(data_items):
                item = data_items[index]
                if item.get("type") == "team":
                    return item.get("id")
        return None

    @staticmethod
    def get_job_titles(responses, type_key="player_position", relationship_key="players"):

        if isinstance(responses, dict):
            responses = [responses]

        result = []

        for response in responses:
            data_items = response.get("data")

            for item in data_items:
                if item.get("type") == type_key:
                    attributes = item.get("attributes")
                    relationships = item.get("relationships")
                    relationship_block = relationships.get(relationship_key)
                    relationship_data = relationship_block.get("data")

                    if len(relationship_data) > 1:
                        title_plural = attributes.get("job_title_plural")
                        result.append(title_plural)
                    elif len(relationship_data) == 1:
                        title_single = attributes.get("job_title")
                        result.append(title_single)

        return result