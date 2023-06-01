using DelimitedFiles

function tokenize_subwords(original_text::String, tokens::Dict{String, Integer})
    text_by_spaces = split(original_text)
    println("text_by_spaces : \n", text_by_spaces)
    
    # Create a copy of text to prevent original text modification
     

    
    # Iterate over terms
    for element in tokens
        root = element[1]
        for word in text_by_spaces # TODO parallelize

            # If the term exists in the text
            println("- check if the root '", root,"' exists in word '", word, "' ")
            while occursin(root, word)
                println("- the root '", root,"' exists in word '", word, "' ")

                # Get the start and end indices of the term in the text
                range = findfirst(root, word)
                println("findfirst ", range, typeof(range) );
                
                println("- processing root '", root,"' in in word '", word, "' ") 
                println("-- ", range, " found '", word[range], "' " )
                return
                
                # Add new token to dictionnary, 
                # increment "," +1

                # If the term is not at the start of the text
                if start_ind > 1
                    # Get the token before the term
                    pre_token = strip(text_by_spaces[1:start_ind-1])
                    if pre_token != ""
                        push!(tokens, pre_token)
                    end
                end
                
                # Add the term to the tokens
                push!(tokens, term)
                
                # Remove the part of the text up to and including the term
                original_text = text_by_spaces[end_ind+1:end]
            end
        end
    end

    # Add any remaining tokens from the text
    remaining_tokens = split(text_by_spaces)
    append!(tokens, remaining_tokens)

    return tokens
end





