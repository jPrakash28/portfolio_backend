import json
import os


def display_current_info():
    """Display current Joshua info from the JSON file"""
    if not os.path.exists('joshua_info.json'):
        print("No joshua_info.json file found.")
        return None

    with open('joshua_info.json', 'r') as file:
        data = json.load(file)

    print("\n=== Current Joshua Info ===")
    print(f"Name: {data['professional']['name']}")
    print(f"Email: {data['professional']['email']}")
    print(f"Projects: {len(data['professional']['projects'])}")
    print(f"Skills: {len(data['professional']['skills']['languages'])} languages")
    print(f"Fun Facts: {len(data['personal']['fun_facts'])}")

    return data


def add_project():
    """Add a new project to Joshua's info"""
    data = display_current_info()
    if not data:
        return

    print("\n=== Add New Project ===")
    project = {
        "name": input("Project Name: "),
        "status": input("Status (completed/in-progress): "),
        "description": input("Description: "),
        "technologies": input("Technologies (comma-separated): ").split(','),
        "github": input("GitHub URL (optional): ")
    }

    data['professional']['projects'].append(project)

    with open('joshua_info.json', 'w') as file:
        json.dump(data, file, indent=2)

    print("Project added successfully!")


def add_fun_fact():
    """Add a new fun fact"""
    data = display_current_info()
    if not data:
        return

    print("\n=== Add New Fun Fact ===")
    fun_fact = input("Enter new fun fact: ")

    data['personal']['fun_facts'].append(fun_fact)

    with open('joshua_info.json', 'w') as file:
        json.dump(data, file, indent=2)

    print("Fun fact added successfully!")


def update_skills():
    """Update skills"""
    data = display_current_info()
    if not data:
        return

    print("\n=== Update Skills ===")
    skill_type = input("Skill type (languages/tools/technologies/soft_skills): ")

    if skill_type in data['professional']['skills']:
        new_skill = input(f"Enter new {skill_type} (comma-separated): ")
        new_skills = [s.strip() for s in new_skill.split(',')]
        data['professional']['skills'][skill_type].extend(new_skills)

        with open('joshua_info.json', 'w') as file:
            json.dump(data, file, indent=2)

        print(f"{skill_type} updated successfully!")
    else:
        print(f"Invalid skill type: {skill_type}")


def main():
    while True:
        print("\n=== Joshua Info Manager ===")
        print("1. Display current info")
        print("2. Add a project")
        print("3. Add a fun fact")
        print("4. Update skills")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            display_current_info()
        elif choice == '2':
            add_project()
        elif choice == '3':
            add_fun_fact()
        elif choice == '4':
            update_skills()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()