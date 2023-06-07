function estimate_pi(n)
    if n < 100
        println("The n should be at least 100 to get good approximation!")
    end 
    
    s = 1.0 #Float64 or BigFloat 
    # iterate from 1 to n
    for i in 1:n
        # if i is an odd number
        # flip sign
        # divide by 2i 
        s += (isodd(i) ? -1 : 1) / (2i + 1)
    end
    4s # return 4* the s
end
# estimate_pi(100_000_000_000) # takes forever
# 3.141592653598537