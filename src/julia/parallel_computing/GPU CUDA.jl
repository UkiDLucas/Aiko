
Pkg.add("CUDA") # works
# CUDA will ERROR on MacBook Pro with (non ENVIDIA card)
Pkg.test("CUDA") # ERROR: Package CUDA errored during testing
