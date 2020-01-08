#include <iostream>
#include <vector>
#include <fstream>
#include <numeric>
#include <cmath>
#include <algorithm>

struct cell {
    int id;
    int dem;
    double x, y;
};

int cap;

struct cell depot;
std::vector<std::vector<struct cell>> clusters;

void inv(int i, int j, std::vector<struct cell> &cells) {
    while (i < j) {
        std::swap(cells[i], cells[j]);
        i++;
        j--;
    }
}

double delta(std::vector<struct cell> &cells) {
    auto loc = 0.0;
    for (auto k = 0; k < cells.size(); k++) {
        loc += std::sqrt(std::pow(cells[k].x - cells[(k + 1) % cells.size()].x, 2) + std::pow(cells[k].y - cells[(k + 1) % cells.size()].y, 2));
    }
    return loc;
}

double h_algorithm(std::vector<struct cell> &cells) {
    cells.emplace_back(depot);
    auto top = delta(cells);
    for (auto k{0}; k < cells.size(); k++) {
        auto glb = std::numeric_limits<double>::max();
        o:
        for (auto i{0}; i < cells.size() - 1; i++) {
            for (auto j{i + 1}; j < cells.size(); j++) {
                oo:
                inv(i, j, cells);
                auto loc = delta(cells);
                if (loc < glb) {
                    glb = loc;
                    if (glb < top) {
                        top = glb;
                        goto o;
                    }
                } else if (loc > glb) {
                    goto oo;
                }
            }
        }
    }
    return top;
}

double oracle(std::vector<struct cell> &cells, cell &depot) {
    auto lod = 0;
    auto loc = 0.0;
    clusters.clear();
    std::vector<struct cell> cluster;
    for (auto k{0}; k < cells.size(); k++) {
        lod += cells[k].dem;
        cluster.emplace_back(cells[k]);
        if (lod > cap) {
            lod = cells[k].dem;
            cluster.pop_back();
            loc += h_algorithm(cluster);
            clusters.emplace_back(cluster);
            cluster.clear();
            cluster.emplace_back(cells[k]);
        }
    }
    if (!cluster.empty()) {
        loc += h_algorithm(cluster);
        clusters.emplace_back(cluster);
    }
    return loc;
}

double hess(std::vector<struct cell> &cells) {
    std::cout.precision(std::numeric_limits<double>::max_digits10 + 1);
    depot = cells.front();
    cells.erase(cells.begin());
    auto top = oracle(cells, depot);
    for (auto k{0}; k < cells.size(); k++) {
        auto glb = std::numeric_limits<double>::max();
        o:
        for (auto i{0}; i < cells.size() - 1; i++) {
            for (auto j{i + 1}; j < cells.size(); j++) {
                oo:
                inv(i, j, cells);
                auto loc = oracle(cells, depot);
                if (loc < glb) {
                    glb = loc;
                    if (glb < top) {
                        top = glb;
                        std::cout << top << std::endl;
                        goto o;
                    }
                } else if (loc > glb) {
                    goto oo;
                }
            }
        }
    }
    cells.emplace_back(depot);
    std::rotate(cells.rbegin(), cells.rbegin() + 1, cells.rend());
    return top;
}

int main(int, char *argv[]) {

    int n;
    std::vector<cell> cells;
    std::ifstream cells_file(argv[1]);
    cells_file >> n >> cap;
    for (int i{0}; i < n; i++) {
        struct cell cell;
        cells_file >> cell.id;
        cells_file >> cell.x >> cell.y;
        cells.emplace_back(cell);
    }
    for (int i{0}; i < n; i++) {
        cells_file >> cells[i].id;
        cells_file >> cells[i].dem;
    }
    cells_file.close();

    auto glb = std::numeric_limits<double>::max();
    for (;;) {
        auto loc = hess(cells);

        std::ofstream data_file("data.py");
        data_file << "data = [";
        for (auto &cluster : clusters) {
            data_file << "[";
            for (auto &node : cluster) {
                data_file << "(" << node.id << ", " << node.x << ", " << node.y << ", " << node.dem << "), ";
            }
            data_file << "], ";
        }
        data_file << "]" << std::endl;
        data_file.close();
        if (loc < glb) {
            glb = loc;
            std::cout << "=>" << glb << std::endl;
        }
    }

    return EXIT_SUCCESS;
}