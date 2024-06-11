# Core modules containing the framework of the flight software

from .template_task import TemplateTask
from .state_manager import StateManager

# expose the Singleton state manager
state_manager = StateManager()