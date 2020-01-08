///////////////////////////////////////////////////////////////////////////////
//        copyright (b) 2012-2019 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>
#include <random>

namespace peqnp {
    int n{0}, m{0}, h(0), w(0);
    std::vector<std::vector<int>> formula;

    int oracle(const std::vector<bool> &subset) {
        int satisfied = 0;
        for (const auto &clause : formula) {
            for (int i{1}; i < clause.size(); i++) {
                if (((clause[i] > 0) && subset[std::abs(clause[i]) - 1]) || ((clause[i] < 0) && !subset[std::abs(clause[i]) - 1])) {
                    satisfied += clause.front();
                    break;
                }
            }
        }
        return w - satisfied;
    }

    bool hess(std::vector<bool> &subset, std::vector<bool> &optimal, const int &k) {
        auto cursor{w};
        std::vector<int> ids;
        std::random_device device;
        std::default_random_engine engine(device());
        for (int o{0}; o < w; o++) {
            std::shuffle(subset.begin(), subset.end(), engine);
            auto global{oracle(subset)};
            for (int i = 0; i < std::pow(n, k); i++) {
                ids.clear();
                auto ii = i;
                do {
                    ids.emplace_back(ii % subset.size());
                    ii /= subset.size();
                } while (ii);
                oo:
                std::for_each(ids.begin(), ids.end(), [&](auto &j) {
                    subset[j] = !subset[j];
                });
                auto local = oracle(subset);
                if (local < global) {
                    global = local;
                    if (global < cursor) {
                        cursor = global;
                        optimal.assign(subset.begin(), subset.end());
                        std::cout << "o " << global << " | " << w - global << std::endl;
                        if (global == 0) {
                            return true;
                        }
                    }
                    goto oo;
                } else if (local > global) {
                    goto oo;
                }
            }
        }
        return false;
    } // namespace peqnp

    void max_sat(const std::string &file_name, const int &k) {
        auto load = [&](const std::string &file_name) {
            auto ifstream = std::ifstream(file_name);
            std::string line, buffer;
            while (getline(ifstream, line)) {
                std::stringstream ss(line);
                std::vector<int> clause;
                while (ss.good()) {
                    ss >> buffer;
                    if (buffer == "c") {
                        break;
                    }
                    if (buffer == "wcnf") {
                        ss >> n;
                        ss >> m;
                        ss >> h;
                        break;
                    }
                    if (buffer == "cnf") {
                        ss >> n;
                        ss >> m;
                        break;
                    }
                    if (buffer != "0" && buffer != "p" && buffer != "cnf" && buffer != "wcnf" && buffer != "%") {
                        clause.emplace_back(std::atoi(buffer.c_str()));
                    }
                }
                if (!clause.empty()) {
                    w += clause.front();
                    formula.emplace_back(clause);
                }
            }
        };

        load(file_name);

        std::vector<bool> subset, complement, optimal;

        subset.resize(n);
        optimal.resize(n);
        peqnp::hess(subset, optimal, k);

        std::cout << "c HESS is polynomial-time incomplete? algorithm for Max2SAT." << std::endl;
        std::cout << "s UNKNOWN\nv ";

        for (int i{0}; i < n; i++) {
            if (optimal[i]) {
                std::cout << (i + 1) << " ";
            } else {
                std::cout << "-" << (i + 1) << " ";
            }
        }
        std::cout << "0" << std::endl;
    }
} // namespace peqnp

int main(int, char *argv[]) {

    std::cout << "c ///////////////////////////////////////////////////////////////////////////////" << std::endl;
    std::cout << "c //        copyright (c) 2012-2019 Oscar Riveros. all rights reserved.        //" << std::endl;
    std::cout << "c //                        oscar.riveros@peqnp.science                        //" << std::endl;
    std::cout << "c //                                                                           //" << std::endl;
    std::cout << "c //   without any restriction, Oscar Riveros reserved rights, patents and     //" << std::endl;
    std::cout << "c //  commercialization of this knowledge or derived directly from this work.  //" << std::endl;
    std::cout << "c ///////////////////////////////////////////////////////////////////////////////" << std::endl;

    peqnp::max_sat(argv[1], std::atoi(argv[2]));

    return EXIT_SUCCESS;
}