## executing Julia in CPU multiple cores
## you need to decide how many cores you want to allocate, see code below
## you can allocate per physical cores (6), not hyper-threads (12)
## you performance might be limited by amount of memory and access to it from the multiple cores
## your performance might be throttled by the CPU temperature


## Uncomment this for the first time run in your system
# using Pkg
# Pkg.add("BenchmarkTools") #for @btime to time our function execution
using BenchmarkTools # @btime

## In your terminal (e.g.: .zproperties)
# export JULIA_NUM_THREADS=6
# MacBook Pro (16-inch, 2019) 6 cores available to Julia out of 12 hyper-threads
# Win 10 Anaconda Prompt: 1
Threads.nthreads() 


function simple_add_vectors!(x, y, counter) 
    counter = counter + 1
    # result = x .+ y # 62 μs https://docs.julialang.org/en/v1/manual/unicode-input/ mu
    result = x + y # 62 μs https://docs.julialang.org/en/v1/manual/unicode-input/ mu
    # println("executing simple_add_vectors() $counter $result[1]")
    return nothing
end

## Set the size of arrays
## eg. 10^20 causes out of memory on 16GB MacBook Pro
## 3.8s 7.45 GiB for creation 10^9 1,000,000,000-element Vector{Float64}
## 478 ns for 10^3 exectution on 6 cores, no printing 

println("creating vectors with random numbers")
a = rand(Float64, 10^3)
b = rand(Float64, 10^3)
exec_counter = 0
@btime simple_add_vectors!(a, b, exec_counter)



size = 2^20             # 2^20 = 1,073,741,824
println("processing x")
@btime x = fill(1.0, size)     # 1048576-element Array{Float64,1}
println("processing y")
@btime y = fill(2, size)       # 1048576-element Array{Int64,1}:
println("processing dot multiplication")
@btime out = y .* x # add each element of x to each element of y
using Test
@test all(y .== 3.0)


## DEFINE FUNCTION to test TIMING
function dot_add!(x,y)
    y .*= x 
    return nothing
end 

fill!(y, 2) # clean the values
@btime dot_add!(x,y)
# 1.779 ms on MacBook Pro (16-inch, 2019) for 2^20 = 1,048,576 elements
# 28.652 s on MacBook Pro (16-inch, 2019) for 2^30 = 1,073,741,824 elements
@test all(y .== 3.0)

## CUDA SEQUENTIAL ADD

function sequential_add!(y, x)
    for i in eachindex(y, x)
        @inbounds y[i] += x[i]
    end
    return nothing
end

fill!(y, 2)
sequential_add!(y, x)
@test all(y .== 3.0f0)



## CUDA PARALLEL ADD

function parallel_add!(y, x)
    Threads.@threads for i in eachindex(y, x)
        @inbounds y[i] += x[i]
    end
    return nothing
end

fill!(y, 2)
parallel_add!(y, x)
@test all(y .== 3.0f0)



@btime sequential_add!($y, $x)
# 1.477 ms (0 allocations: 0 bytes) -- Predator Helios 300 Win 10
# 1.853 ms (0 allocations: 0 bytes) -- MacBook Pro


using oneAPI
a = oneArray(rand(2,2)) #ERROR: UndefVarError: libze_loader not defined
a .+ 1

