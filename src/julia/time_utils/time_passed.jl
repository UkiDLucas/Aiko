
function time_passed!(description, time_point_ns)
    time_passed_ns = time() - time_point_ns # previous minus current
    println("$description took $time_passed_ns seconds")
 
    minutes = round(time_passed_ns/60, digits = 3)
    println("$minutes minutes ") 

    seconds = round(time_passed_ns, digits = 3)
    println("$seconds s") 
    milliseconds =  round(time_passed_ns*1000, digits = 3)
    println("$milliseconds μs milliseconds ") 

    nanoseconds = round(time_passed_ns*1000*1000, digits = 3)
    println("$nanoseconds ns nanoseconds ")

    picoseconds = round(time_passed_ns*1000*1000*1000, digits = 3)
    println("$picoseconds ps picoseconds ") 

    time_point_ns = time()
    return nothing
end


time_passed!("", time()) # takes about 1 ns

time_to_sleep = 0.001 # seconds, minimum 0.001
t1 = time()
sleep(time_to_sleep) # seconds
time_passed!("setting of $time_to_sleep", t1) # takes about 2.5 ~ 3.5 μs