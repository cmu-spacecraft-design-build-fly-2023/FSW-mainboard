# Onboard Data Handling (OBDH) Task

from apps.data_handler import DataHandler as DH
from state_manager import state_manager as SM
from tasks.template_task import DebugTask


class Task(DebugTask):

    name = "OBDH"
    ID = 0x02

    # Class variables
    SD_cleaned = False  # TODO DEBUG
    SD_scanned = False
    SD_stored_volume = 0

    async def main_task(self):

        if SM.current_state == "STARTUP":
            if self.SD_cleaned == False:
                DH.delete_all_files()
                self.SD_cleaned = True
            if self.SD_scanned == False:
                DH.scan_SD_card()
                self.SD_scanned = True

            # TODO Temporarily start global state switch here
            # TODO should have a verification checklist in monitor and switch from there
            SM.switch_to("NOMINAL")
        elif SM.current_state == "NOMINAL":
            self.SD_stored_volume = DH.compute_total_size_files()

        print(
            f"[{self.ID}][{self.name}] Stored files: {self.SD_stored_volume} bytes."
        )
