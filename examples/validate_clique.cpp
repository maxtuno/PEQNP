///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2018 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <map>
#include <fstream>
#include <iostream>
#include <map>

int main(int argc, char *argv[]) {

    std::string data_file(argv[1]);
    std::string clique_file(argv[2]);

    std::fstream graph(data_file);
    std::fstream clique(clique_file);

    char e;
    std::string dummy;
    int x{0}, y{0}, size{0}, l{0}, n{0};
    do {
        graph >> dummy;
    } while (dummy != "edge");
    graph >> size >> l;
    std::map<std::pair<int, int>, bool> map;
    for (int i = 0; i < l; i++) {
        graph >> e >> x >> y;
        map[std::make_pair(x, y)] = true;
        map[std::make_pair(y, x)] = true;
    }
    graph.close();

    clique >> n;
    auto seq = (int *) calloc(n, sizeof(int));
    for (int i = 0; i < n; i++) {
        clique >> x;
        seq[i] = x;
    }
    clique.close();

    std::map<int, int> degree;

    int loc = 0;
    for (int i = 0; i < n ; i++) {
        for (int j = 0; j < n; j++) {
            if (seq[i] != seq[j]) {
                if (!map[std::make_pair(seq[i], seq[j])]) {
                    std::cout << seq[i] << " " << seq[j] << std::endl;
                }
                loc += !map[std::make_pair(seq[i], seq[j])];
                degree[seq[i]]++;
                degree[seq[j]]++;
            }
        }
    }

    if (!loc) {
        std::cout << "SATISFIABLE : " << n << "-CLIQUE" << std::endl;
    } else {
        std::cout << "UNSATISFIABLE" << std::endl;
    }

    // int i = 0;
    // for (auto &kv : degree) {
    //     std::cout << i << ") " << kv.first << " : " << kv.second << std::endl;
    //     i++;
    // }

    return EXIT_SUCCESS;
}