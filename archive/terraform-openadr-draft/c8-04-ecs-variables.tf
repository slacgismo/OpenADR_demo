# ECS  Variables
## VEN variables

# define if this ven to use mock battery api

variable "agent_definition_list_file" {
  description = "agent_definition_list_file"
  default = "./templates/ecs/task_definitions/agent-definition-list.json" # DEV or PROD
}
