cmake_minimum_required(VERSION 2.4)
project(CaDiCaL)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

include_directories(. ../../sat)

set(CMAKE_CXX_FLAGS "-std=c++11 -Os -D NDEBUG")

add_library(CaDiCaL SHARED
        peqnp_sat.cpp
        analyze.cpp
        arena.cpp
        arena.hpp
        assume.cpp
        averages.cpp
        backtrack.cpp
        backward.cpp
        bins.cpp
        block.cpp
        cadical.cpp
        cadical.hpp
        ccadical.cpp
        checker.cpp
        clause.cpp
        clause.hpp
        collect.cpp
        compact.cpp
        condition.cpp
        config.cpp
        contract.hpp
        cover.cpp
        cover.hpp
        decide.cpp
        decompose.cpp
        deduplicate.cpp
        elim.cpp
        ema.cpp
        extend.cpp
        external.cpp
        external.hpp
        file.cpp
        flags.cpp
        format.cpp
        gates.cpp
        instantiate.cpp
        internal.cpp
        internal.hpp        
        limit.cpp
        logging.cpp
        lucky.cpp
        message.cpp
        minimize.cpp
        occs.cpp
        options.cpp
        parse.cpp
        phases.cpp
        probe.cpp
        profile.cpp
        proof.cpp
        propagate.cpp
        queue.cpp
        random.cpp
        reduce.cpp
        rephase.cpp
        report.cpp
        resources.cpp
        restart.cpp
        restore.cpp
        score.cpp
        signal.cpp
        solution.cpp
        solver.cpp
        stats.cpp
        subsume.cpp
        terminal.cpp
        ternary.cpp
        tracer.cpp
        transred.cpp
        util.cpp
        var.cpp
        version.cpp
        vivify.cpp
        walk.cpp
        watch.cpp
        )