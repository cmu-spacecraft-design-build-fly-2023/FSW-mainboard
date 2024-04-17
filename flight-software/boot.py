import storage

print("Boot")
storage.remount("sd/", readonly=False)