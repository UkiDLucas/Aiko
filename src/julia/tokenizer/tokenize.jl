# most simplistic tokenizer using white space
# "AI," is a word here!
function tokenize(text)
    return split(text) 
end

sentence = "I love natural language processing with AI, but would like to see subwords."
tokens = tokenize(sentence)
println(tokens)


using Test

@testset "Tokenizer Tests" begin
    @test tokenize("I love AI.") == ["I", "love", "AI."]
end