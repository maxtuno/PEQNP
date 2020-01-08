///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2018 Oscar Riveros. all rights reserved.        //
//                         oscar.riveros@peqnp.science                       //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <fstream>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <hess/hess.h>
#include <random>
#include <SDL2/SDL.h>

SDL_Event event;
SDL_Renderer *renderer;
SDL_Window *window;

void show(const I *seq, bool **map, const I len) {
    if (SDL_PollEvent(&event) && event.type == SDL_QUIT) {
        std::exit(EXIT_SUCCESS);
    }
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_RenderClear(renderer);
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    for (I i = 0; i < len; i++) {
        for (I j = 0; j < len; j++) {
            if (map[seq[i]][seq[j]]) {
                SDL_RenderDrawPoint(renderer, i, j);
            }
        }
    }
    SDL_RenderPresent(renderer);
}

int main(int argc, char *argv[]) {

    struct cpu box{};

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

    SDL_Init(SDL_INIT_VIDEO);
    SDL_CreateWindowAndRenderer(static_cast<int>(box.len), static_cast<int>(box.len), 0, &window, &renderer);
    SDL_SetWindowTitle(window, "www.peqnp.science : Hyper Exponential Space Sorting");

    std::vector<I> aux(box.len);
    std::iota(aux.begin(), aux.end(), 0);

    std::random_device device;
    std::default_random_engine engine(device());
    std::shuffle(aux.begin(), aux.end(), engine);

    box.seq = aux.data();

    box.log = [](struct cpu *box) {
        if (SDL_PollEvent(&event) && event.type == SDL_QUIT) {
            std::exit(EXIT_SUCCESS);
        }
        std::cout << box->glb << std::endl;
        show(box->seq, box->map, box->len);
    };

    hess(&box);

    if (box.glb == 0) {
        std::cout.precision(std::numeric_limits<I>::max_digits10 + 1);
        std::cout << "SATISFIABLE : " << data_file << std::endl;
        std::ofstream os(path_file);
        os << "NAME : Solution for \"" << data_file << "\"" << std::endl;
        os << "COMMENT : www.peqnp.science " << std::endl;
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

    // SDL_Delay(3000);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return EXIT_SUCCESS;
}
