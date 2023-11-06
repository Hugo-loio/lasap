push!(LOAD_PATH, "./../julia/LasapInterface/src/")

import LasapInterface as li

run(`lasap_merge_daemon test 1`, wait=false)

println("Daemon lauched")
sleep(10)
