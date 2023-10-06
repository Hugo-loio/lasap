module LasapInterface

using DataFrames, OrderedCollections, Parquet2

export Observable, append!, todisk

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
        custompath = ENV["LASAP_DATA_DIR"]
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

function todisk(obs::Observable, dirname::String;
        name::String="", verbose::Bool=false, tarname::String="")
    path = data_dir()
    check_dir(path)
    path = data_dir() * dirname
    check_dir(path)
    if(length(name) == 0)
        name = obs.props[1,"name"]
    end
    name_props = name * "_props.parquet"
    name_data = name * "_data.parquet"
    path_props = path * "/" * name_props
    path_data = path * "/" * name_data
    Parquet2.writefile(path_props, obs.props)
    Parquet2.writefile(path_data, obs.data)

    if(verbose)
        println("Outputed data files to: " * path * "/" * name)
    end

    if(length(tarname) > 0)
        tarpath = path * "/" * tarname * ".tar"
        # Bundle files in tar with tarname, and remove the separate files
        readchomp(`tar -rf $tarpath -C $path $name_props $name_data`)
        rm(path_props)
        rm(path_data)
    end
end

end
