module Container

using DataFrames
using OrderedCollections

struct Observable
    props::DataFrame
    data::DataFrame
    numkeys::Integer
    function Observable(
            name::String, shape::Tuple{Vararg{Integer}}, 
            keynames::Vector{String}=Vector{String}([]), 
            props::OrderedDict=OrderedDict()
        )
        props_dict = OrderedDict()
        props_dict["name"] = name
        props_dict["rank"] = length(shape)
        for (index,dim) in enumerate(shape)
            props_dict["dim" * string(index)] = dim
        end
        props = DataFrame(props_dict)
        #=
        if(props != None): 
            props_dict.update(props)
        # Metadata about the set of arrays
        self.props = pd.DataFrame([props_dict])

        columns = keynames + list(map(str,list(np.arange(1, np.prod(shape)+1))))
        #Data dataframe
        self.data = pd.DataFrame(columns = columns)
        #Aux variables
        self.shape = shape
        self.num_keys = len(keynames)
        =#
        new(props, DataFrame(), length(keynames))
    end
end

#=
function append(obs::Observable, array, keyvals; 
        check_duplicate::Bool=False, replace::Bool=False)
    #if(check_duplicate)
    #end
end

function to_parquet(obs::Observable)
    #TODO
end

function to_disk(obs::Observable; dirname::String)
    #TODO
end
=#

# module end
end
