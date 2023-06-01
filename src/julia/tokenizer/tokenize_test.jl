 
include("tokenize_subwords.jl")



# token, number of occurences
tokens = Dict{String, Integer}("." => 0, "," => 0, "reg" => 0, "anti" => 0, "agri" => 0)
println(tokens)


text = "Farming is an agricultural business, it does not use antigovermantal regulations."
tokens = tokenize_subwords(text, tokens)
println(tokens)


using Test

@testset "Tokenizer Tests" begin
    @test tokenize_subwords(text, tokens) == [
        "Farming", "is", "an", "agricultural", "business", "," , 
        "it", "does", "not", "use", "antigravity",  "regulations", "."]
end