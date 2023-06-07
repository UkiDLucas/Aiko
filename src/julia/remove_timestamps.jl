using Pkg
# Pkg.add("Dates") # RUN ONCE
using Dates

function remove_timestamps(text::String)::String

    # Remove potential double line breaks
    text = replace(text, "\n\n" => "\n")
    
    #pattern = r"\d+:\d+\.\d+\s-->\s\d+:\d+\.\d+\s"
    #text = replace(text, pattern => "")
    
    # Timestamp pattern
    # 00:02.800 --> 00:05.320
    # 35:39.440 --> 35:42.760
    pattern = r"\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\s"
    # Replace all instances of the pattern with an empty string
    text = replace(text, pattern => "")

    # 1:02:20.500 --> 1:02:23.700
    pattern = r"\d{1}:\d{2}:\d{2}\.\d{3} --> \d{1}:\d{2}:\d{2}\.\d{3}\s"
    # Replace all instances of the pattern with an empty string
    text = replace(text, pattern => "")
    

    # Remove double spacing
    text = replace(text, "  " => " ")

    text = replace(text, "\n" => "XXXX")

    pattern = r"\.XXXX"
    text = replace(text, pattern => ".\n")
    
    pattern = r"XXXX"
    text = replace(text, pattern => " ")

    
    # Remove double spacing
    text = replace(text, "  " => " ")

    return text
end