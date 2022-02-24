def find_person(skill_name, min_skill_level, max_skill_level):
    for person in people:
        for skill in person["skills"]:
            if skill["skill_name"] == skill_name and int(skill["skill_level"]) >= min_skill_level and int(skill["skill_level"]) <= max_skill_level:
                return person
    return None


input = open("input.txt", "r")
lines = input.readlines()

people = []
projects = []

ptr = 1

while ptr < len(lines):
    obj = lines[ptr].strip().split(" ")

    if len(obj) == 2:
        person_skills_list = []
        person_name, person_skill_count = obj

        person_skill_counter = int(person_skill_count)

        while person_skill_counter > 0:
            ptr += 1
            skill_name, skill_level = lines[ptr].strip().split(" ")

            person_skills_list.append({
                "skill_name": skill_name,
                "skill_level": skill_level
            })

            person_skill_counter -= 1

        people.append({
            "name": person_name,
            "skills": person_skills_list
        })
    else:
        project_skill_requirements = []
        project_name, days_to_complete, score, deadline, role_requirements_count = obj

        role_requirements_counter = int(role_requirements_count)

        while role_requirements_counter > 0:
            ptr += 1
            skill_name, skill_level = lines[ptr].strip().split(" ")

            project_skill_requirements.append({
                "skill_name": skill_name,
                "skill_level": skill_level
            })

            role_requirements_counter -= 1

        projects.append({
            "name": project_name,
            "days_to_complete": int(days_to_complete),
            "score": int(score),
            "deadline": int(deadline),
            "role_requirements": project_skill_requirements
        })

    ptr += 1

projects.sort(key=lambda x: x["deadline"])

for project in projects:
    qualified_people = []
    role_requirement_count = len(project["role_requirements"])

    for role in project["role_requirements"]:
        # try to fill with people who are between skill level - 1 and skill level + 1
        # if not found fill with people between skill level - 1 and skill level + 101
        qualified_person = find_person(role["skill_name"], int(
            role["skill_level"]) - 1, int(role["skill_level"]) + 1)

        if qualified_person is None:
            qualified_person = find_person(
                role["skill_name"], int(role["skill_level"]) - 1, 101)

        if qualified_person is not None:
            qualified_people.append(qualified_person)

        if len(qualified_people) == role_requirement_count:
            print(project["name"])
            print(qualified_people)