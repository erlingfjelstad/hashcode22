from tqdm import tqdm

input = open("input.txt", "r")
lines = input.readlines()

people = []
projects = []

people_count, project_count = lines[0].strip().split(" ")

ptr = 1
sub_ptr = 0
counter = 0

while ptr < len(lines):
    obj = lines[ptr].strip().split(" ")

    if len(obj) == 2:
        person_skills_list = []
        person_name, person_skill_count = obj

        person_skill_counter = int(person_skill_count)

        while person_skill_counter > 0:
            person_skills = {}
            ptr += 1

            skill_name, skill_level = lines[ptr].strip().split(" ")
            person_skills["skill_name"] = skill_name
            person_skills["skill_level"] = skill_level

            person_skills_list.append(person_skills)
            person_skill_counter -= 1

        person = {
            "name": person_name,
            "skills": person_skills_list,
            "free": True,
            "next_availability": 0
        }
        people.append(person)
    else:
        project_skill_requirements = []

        project_name, days_to_complete, score, deadline, role_requirements_count = obj

        role_requirements_counter = int(role_requirements_count)

        while role_requirements_counter > 0:
            role_requirements = {}
            ptr += 1

            skill_name, skill_level = lines[ptr].strip().split(" ")
            role_requirements["skill_name"] = skill_name
            role_requirements["skill_level"] = skill_level

            project_skill_requirements.append(role_requirements)
            role_requirements_counter -= 1

        project = {
            "name": project_name,
            "days_to_complete": int(days_to_complete),
            "score": int(score),
            "deadline": int(deadline),
            "role_requirements": project_skill_requirements
        }
        projects.append(project)

    ptr += 1

projects.sort(key = lambda i: i['deadline'])

skills = {}
persons = {}
for person in people:
  for skill in person["skills"]:
    if skill["skill_name"] not in skills:
      skills[skill["skill_name"]] = []
    skills[skill["skill_name"]].append({ "name": person["name"], "skill_level": skill["skill_level"]})
  persons[person["name"]] = person


skillsForDb = []
for k, v in skills.items():
  skillsForDb.append({
    "name": k,
    "persons": v
  })


def lazyLoadPerson(name):
  return persons[name]


def setPersonFree(name):
  person = lazyLoadPerson(name)
  person["free"] = True


def takePerson(name, daysToComplete):
  person = lazyLoadPerson(name)
  person["free"] = True
  person["next_availability"] = daysToComplete


def isPersonFree(name, actualWorkingDay):
  person = lazyLoadPerson(name)
  return person["next_availability"] < actualWorkingDay or actualWorkingDay == 0

resultStr = ""
nAssignedProjects = 0

actualWorkingDay = 0
matchesFound = False
maxMatchedTime = 0

while True:
  for project in projects:
    daysToComplete = int(project["days_to_complete"])
    assignedPersons = []
    for role in project["role_requirements"]:
      requiredRoleLevel = int(role["skill_level"])
      # get person that has a skill with the closest skill level
      dmin = 99
      personName = None
      for person in skills[role["skill_name"]]:
        if not isPersonFree(person["name"], actualWorkingDay) or person["name"] in assignedPersons: continue
        personSkillLevel = int(person["skill_level"])
        if personSkillLevel >= requiredRoleLevel and personSkillLevel - requiredRoleLevel < dmin:
          if personName is None:
            dmin = personSkillLevel
            personName = person["name"]
          else:
            dmin = personSkillLevel
            personName = person["name"]
      if personName is not None:
        assignedPersons.append(personName)
        takePerson(personName, daysToComplete)
    if len(assignedPersons) == len(project["role_requirements"]):
      matchesFound = True
      resultStr += project["name"] + "\n"
      nAssignedProjects += 1
      maxMatchedTime = max(int(project["deadline"]), maxMatchedTime + actualWorkingDay)
      actualWorkingDay += int(project["deadline"])
      for person in assignedPersons:
        resultStr += person + " "
      resultStr += "\n"
    else:
      for p in assignedPersons:
        setPersonFree(p)
  print(actualWorkingDay, maxMatchedTime)
  if not matchesFound:
    if actualWorkingDay >= maxMatchedTime:
      break
  else:
    matchesFound = False


print(str(nAssignedProjects) + "\n" + resultStr)

# try to first find a person that has skill level exactly the same as the project requires
# if that person has the exact skills, he will get a rank up in his ability
#