using DelimitedFiles # for writedlm

## REPLACE 
println(replace("GFG is a CS portal.", "CS" => "Computer Science"))


function trim_on_opening_tag(tag, text)
    found_range = findfirst(tag, text)
    if found_range == Nothing
        println("that is all folks for trim_on_opening_tag")
    else
        println("START: Found tag at location > ", found_range) # UnitRange{Int64}

        start = found_range[length(tag)]
        start = start + 1 # we want NEXT character 

        #ending = length(text) # last character
        ending = lastindex(text) # last character
        println( "start ", start, " ending ", ending)
        text = text[start:ending]
        #println( text[1:30])
        return text
    end
end 

function find_ending_tag(tag, text)
    found_range = findfirst(tag, text)
   
    println("END: Found tag at location > ", found_range) # UnitRange{Int64}

    ending = found_range[1] - 1 
    text = text[1:ending]
    println(text)
    return text
end 

data = [["index", "heading", "content"]]










## FILE LOCATION - fron the HOME of the project
blogger_xml_path = "./xml/data_blogger/personal.xml"
#blogger_xml_path = "./xml/data_blogger/tech.xml"


xml_file = open(blogger_xml_path, "r")
text = read(xml_file, String) # read entire file into a string 
close(xml_file)


post_title_tag_start = "<title type='text'>"
post_title_tag_end = "</title>"

counter = 0
while true
    text = trim_on_opening_tag(post_title_tag_start, text)
    post_heading = find_ending_tag(post_title_tag_end, text)
    counter += 1
    println(counter, " saving ", post_heading)
    new_data = [["$counter"; post_heading; "TBD"]] # inser an array as a row
    data = [data; new_data]
    writedlm("./xml/output.csv", data) # super ineficient until I fix the bug
end




println("entries_count ", entries_count)


