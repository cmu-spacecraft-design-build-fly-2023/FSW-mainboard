# Core modules containing the framework of the flight software

from .state_manager import StateManager
from .template_task import TemplateTask

# expose the Singleton state manager
state_manager = StateManager()
