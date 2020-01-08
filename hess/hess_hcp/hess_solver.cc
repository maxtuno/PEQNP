///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //
//                         oscar.riveros@peqnp.science                       //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <fstream>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <hess/hess_solver.h>

int main(int argc, char *argv[]) {

    struct box box{};

    std::string data_file(argv[1]);
    std::string path_file(data_file);
    path_file.erase(std::find(path_file.begin(), path_file.end(), '.'), path_file.end());
    path_file += ".path";

    std::fstream graph(data_file);
    std::string buffer;
    I x{0}, y{0};
    while (graph >> buffer) {
        if (buffer == "DIMENSION") {
            graph >> buffer;
            if (buffer == ":") {
                graph >> box.len;
                box.seq = (I *) calloc(box.len, sizeof(I));
                box.map = (bool **) calloc(box.len, sizeof(bool *));
                for (I i = 0; i < box.len; i++) {
                    box.map[i] = (bool *) calloc(box.len, sizeof(bool));
                    box.seq[i] = i;
                }
            }
        }
        if (buffer == "EDGE_DATA_SECTION") {
            break;
        }
    }
    while (graph.good()) {
        graph >> buffer;
        if (buffer == "-1" || buffer == "EOF") {
            break;
        }
        x = static_cast<I>(std::atoll(buffer.c_str()) - 1);
        graph >> buffer;
        y = static_cast<I>(std::atoll(buffer.c_str()) - 1);
        box.map[x][y] = true;
        box.map[y][x] = true;
    }
    graph.close();

    box.glb = box.len;

    box.log = [](struct box *box) {
         std::cout << box->glb << std::endl;
    };

    hess(&box);

    if (box.sat) {
        std::cout.precision(std::numeric_limits<I>::max_digits10 + 1);
        std::cout << "SATISFIABLE : " << data_file << std::endl;
        std::ofstream os(path_file);
        os << "NAME : Solution for \"" << data_file << "\"" << std::endl;
        os << "COMMENT : Solved with HESS oscar.riveros@peqnp.science" <<  std::endl;
        os << "TYPE : PATH" << std::endl;
        os << "DIMENSION : " << box.len << std::endl;
        os << "TOUR_SECTION" << std::endl;
        std::size_t k{0};
        for (std::size_t i{0}; i < box.len; i++) {
            os << box.seq[i] + 1 << (++k < box.len ? "\n" : "");
        }
        os << std::endl;
        os << "-1" << std::endl;
        os << "EOF" << std::endl;
    } else {
        std::cout << "UNSATISFIABLE : " << data_file << std::endl;
    }

    return EXIT_SUCCESS;
}
