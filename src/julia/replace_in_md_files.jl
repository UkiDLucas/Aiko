# using Pkg; Pkg.add("Glob") # RUN ONE TIME
using Glob

function replace_in_md_files(directory_path::String, replace_func::Function)

    println(directory_path)
    
    # Get all the .md files in the given directory
    md_files = glob("*.md", directory_path)
    println(md_files)
    
    # Iterate through each file
    for file in md_files
        println(file)
        # Open the file for reading
        file_content = open(f -> read(f, String), file)
        
        # Replace timestamps
        modified_content = replace_func(file_content)
        
        # Open the file for writing and save the modified content
        open(file, "w") do f
            write(f, modified_content)
        end
    end
end