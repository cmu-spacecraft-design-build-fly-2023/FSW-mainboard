# Onboard Data Handling (OBDH) Task

from tasks.template_task import DebugTask

from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH


class Task(DebugTask):

    name = "OBDH"
    ID = 0x02

    # Class variables
    SD_scanned = False
    SD_stored_volume = 0

    async def main_task(self):

        if SM.current_state == "STARTUP":
            DH.delete_all_files()
            if self.SD_scanned == False:
                DH.scan_SD_card()
                self.SD_scanned = True
            # TODO Temporarily start global state switch here
            SM.switch_to("NOMINAL")
        elif SM.current_state == "NOMINAL":
            # DH.clean_up()
            self.SD_stored_volume = DH.compute_total_size_files()
            # print(DH.data_process_registry['imu'].request_TM_path())

        print(f"[{self.ID}][{self.name}] OBDH running.")
        print(
            f"[{self.ID}][{self.name}] Stored files are taking {self.SD_stored_volume} bytes."
        )
