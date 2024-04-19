from hal.drivers.burnwire import BurnWires
from hal.argus_v1 import ArgusV1Components

duty_cycle_pct      = 50
frequency           = 1000

# Create a burn wires object
burn_wires = BurnWires(
    enable_pin=ArgusV1Components.BURN_WIRE_ENABLE,
    burn_xp=ArgusV1Components.BURN_WIRE_XP,
    burn_xm=ArgusV1Components.BURN_WIRES_XM,
    burn_yp=ArgusV1Components.BURN_WIRES_YP,
    burn_ym=ArgusV1Components.BURN_WIRES_YM,
)

# Set the frequency
burn_wires.frequency = frequency

# Set the duty cycle
burn_wires.duty_cycle = 50

# Set the duration
burn_wires.duration_s = 1

# Enable the burn wires
burn_wires.enable()
burn_wires.burn_xp()
burn_wires.burn_xm()
burn_wires.burn_yp()
burn_wires.burn_ym()
burn_wires.disable()
