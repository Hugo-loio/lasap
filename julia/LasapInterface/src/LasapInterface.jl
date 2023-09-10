module LasapInterface

using DataFrames, OrderedCollections, Parquet2

struct Observable
    props::DataFrame
    data::DataFrame
    numkeys::Integer
    function Observable(
            name::String, shape::Tuple{Vararg{Integer}}, 
            keynames::Vector{String}=Vector{String}([]), 
            extraprops::OrderedDict=OrderedDict()
        )
        props_dict = OrderedDict()
        props_dict["name"] = name
        props_dict["rank"] = length(shape)
        for (index,dim) in enumerate(shape)
            props_dict["dim" * string(index)] = dim
        end
        if(length(extraprops) != 0)
            merge!(props_dict, extraprops)
        end
        # Properties dataframe
        props = DataFrame(props_dict)

        columns = vcat(keynames, [string(x) for x in 1:prod(shape)])
        # Data dataframe
        data = DataFrame([Symbol(x) => Float64[] for x in columns])
        new(props, data, length(keynames))
    end
end

# Attention! Arrays in julia are collumn major but in python they are row major! You might need to reorder the dimensions before appending (which automatically flattens the array)
function append!(obs::Observable, array::Array, keyvals::Vector; 
        check_duplicate::Bool=false, replace::Bool=false)
    if(check_duplicate)
        #for (i,row) in enumerate(eachrow(obs.data))
        for row in eachrow(obs.data)
            if(all(Array(row[1:obs.numkeys]) .== keyvals))
                if(replace)
                    row[obs.numkeys+1:end] = vec(array)
                    return 1
                end
                return 2
            end
        end
    end
    push!(obs.data, vcat(keyvals, vec(array)))
    return 0
end

function data_dir()
    try 
        custompath = ENV["DAPP_DATA_DIR"]
        if(custompath[end] == "/")
            return custompath
        else
            return custompath * "/"
        end
    catch KeyError
        return pwd() * "/data/"
    end
end

function check_dir(dir::String)
    if(!isdir(dir))
        try
            mkdir(dir)
        catch IOError
            println(IOError)
        end
    end
end

function to_disk(obs::Observable, dirname::String)
    path = data_dir()
    check_dir(path)
    if(length(dirname) != 0)
        path = data_dir() * dirname
        check_dir(path)
    end
    name = obs.props[1,"name"]
    name_props = name * "_props.parquet"
    name_data = name * "_data.parquet"
    Parquet2.writefile(path * "/" * name_props, obs.props)
    Parquet2.writefile(path * "/" * name_data, obs.data)
end

# module end
end
