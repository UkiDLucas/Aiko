## Intel dos not work on MacBookPro even if I have UDH Graphics 630 card
# https://juliapackages.com/p/oneapi
Pkg.add("oneAPI") # works
using oneAPI.oneL0 # works




using oneAPI #ERROR: InitError: UndefVarError: libze_loader not defined
drv = first(drivers());
dev = first(devices(drv))