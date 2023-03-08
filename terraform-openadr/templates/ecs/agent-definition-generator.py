import json
from typing import List, Dict, Any
CONTAINER_DEFINITION_TEMPLATE = ({
    "name": "vtn",
    "image": "${app_image_vtn}",
    "essential": True,
    "memoryReservation": 256,
    "runtimePlatform": {
        "operatingSystemFamily": "LINUX",
        "cpuArchitecture": "ARM64"
    },
    "entryPoint": ["sh", "-c"],
    "command": ["python vtn.py"],

})


def export_to_json_tpl(data, filename):
    """
    Export data to json file
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def generate_vtn_container_definitions_from_template(vtn_template: dict, vtn: dict) -> dict:
    """
    Generate container definition for VEN
    params: vtn_template: dict
    params: ven: dict
    """
    vtn_id = vtn['vtn_id']
    vtn_template['name'] = "vtn-" + vtn_id
    vtn_template['image'] = vtn['app_image_vtn']
    vtn_template['environment'] = [{"name": key.upper(), "value": value}
                                   for key, value in vtn.items() if key != 'app_image_vtn']

    vtn_template['portMappings'] = [
        {
            "containerPort": 8080,
            "hostPort": 8080
        }
    ]
    vtn_template['mountPoints'] = [
        {
            "readOnly": False,
            "containerPath": f"/vol/{vtn_id}",
            "sourceVolume": "agent-volume"
        }
    ]
    vtn_template['healthCheck'] = {
        "retries": 3,
        "command": [
            "CMD-SHELL",
            "curl -f http://127.0.0.1:8080/health || exit 1"
        ],
        "timeout": 5,
        "interval": 30
    }

    vtn_template['logConfiguration'] = {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "${log_group_name}",
            "awslogs-region": "${log_group_region}",
            "awslogs-stream-prefix": f"{vtn_id}"
        }
    }
    return vtn_template


def generate_ven_container_definitions_from_template(ven_template: dict, ven: dict) -> dict:
    """
    Generate container definition for VEN
    params: ven_template: dict
    params: ven: dict
    """
    ven_id = ven['ven_id']
    ven_template['name'] = "ven-" + ven_id
    ven_template['image'] = ven['app_image_ven']
    ven_template['command'] = ["python ven.py"]
    ven_template['environment'] = [{"name": key.upper(), "value": value}
                                   for key, value in ven.items() if key != 'app_image_ven']

    ven_template['mountPoints'] = [
        {
            "readOnly": False,
            "containerPath": f"/vol/{ven_id}",
            "sourceVolume": "agent-volume"
        }
    ]
    ven_template['logConfiguration'] = {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "${log_group_name}",
            "awslogs-region": "${log_group_region}",
            "awslogs-stream-prefix": f"{ven_id}"
        }
    }
    return ven_template


if __name__ == "__main__":
    with open('input-agents-list.json', 'r') as json_file:
        # Load the contents of the file into a dictionary
        data = json.load(json_file)

    agents = data['agents']
    agent_definition = []
    agent_definition_list = []
    for agent in agents:

        agent_id = agent['agent_id']
        vtn = agent['vtn']
        vens = agent['vens']
        # append vtn to definition_template's environment
        vtn_template = CONTAINER_DEFINITION_TEMPLATE.copy()
        vtn_definitaion = generate_vtn_container_definitions_from_template(
            vtn_template, vtn)
        agent_definition.append(vtn_definitaion)

        for ven in vens:
            # create ven template
            ven_template = CONTAINER_DEFINITION_TEMPLATE.copy()
            ven_difinition = generate_ven_container_definitions_from_template(
                ven_template=ven_template, ven=ven)

            agent_definition.append(ven_difinition)
        definition_file_name = f'./task_definitions/container-definition-{agent_id}.json.tpl'
        agent_definition_list.append({
            "agent_id": agent_id,
            "definition_file_name": definition_file_name
        })

        # export each agent definition to a json file
        export_to_json_tpl(
            agent_definition, definition_file_name)

    # export agent_definition_list to a json file
    list_file_name = "./task_definitions/agent-definition-list.json"
    export_to_json_tpl(
        agent_definition_list, list_file_name)
