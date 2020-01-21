///////////////////////////////////////////////////////////////////////////////
//        copyright (c) 2012-2018 Oscar Riveros. alst rights reserved.        //
//                           oscar.riveros@peqnp.com                         //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#include <fstream>
#include <iostream>

#include <boost/multiprecision/cpp_int.hpp>

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

namespace mps = boost::multiprecision;

typedef mps::cpp_int U;
typedef unsigned I;

U g;
U c;

struct tape {
    U *ram;
    I idx;
    const I len;
};

inline void write(struct tape *tape, U o) {
    tape->ram[tape->idx] = o;
    tape->idx++;
}

inline U read(struct tape *tape) {
    tape->idx--;
    return tape->ram[tape->idx];
}

inline U *list_3sort(U *lst, const I &len) {
    U aux = 0;
    I i = 0, j = 1;
    for (i = j - 1; i < j; i++) {
        for (j = i + 1; j < len - i - 1; j++) {
            aux = lst[j];
            if (lst[i] > aux) {
                lst[j] = lst[i];
                lst[i] = aux;
            }
            aux = lst[len - 1 - j];
            if (lst[len - 1 - i] < aux) {
                lst[len - 1 - j] = lst[len - 1 - i];
                lst[len - 1 - i] = aux;
            }
        }
    }

    aux = lst[len / 2];
    if (aux < lst[len / 2 - 1]) {
        lst[len / 2] = lst[len / 2 - 1];
        lst[len / 2 - 1] = aux;
    }

    return lst;
}

inline bool in(struct tape *tape, I o) {
    for (I idx = 0; idx < tape->idx; idx++) {
        if (tape->ram[idx] == o) {
            return true;
        }
    }
    return false;
}

inline void print(struct tape *uu, struct tape *vv) {
    std::cout << "\nprint(sum([";
    for (I idx = 0; idx < uu->len; idx++) {
        if (uu->ram[idx] != 0) {
            if (in(vv, idx)) {
                std::cout << uu->ram[idx] << ", ";
            }
        }
    }
    std::cout << "]))" << std::endl;
    std::cout << "\nprint(sum([";
    for (I idx = 0; idx < uu->len; idx++) {
        if (uu->ram[idx] != 0) {
            if (!in(vv, idx)) {
                std::cout << uu->ram[idx] << ", ";
            }
        }
    }
    std::cout << "]))\n" << std::endl;
}

inline U state(const U &s, const U &r, const U &p, const U &q) {
    U l = MIN((s < q ? q - s : s - q), (r < p ? p - r : r - p));
    if (l < g) {
        g = l;
        std::cout << "# " << c << " => " << g << std::endl;
    }
    return l;
}

void deidos(struct tape uu, U u, struct tape *vv, U s, U r, const U p, const U q) {
    c++;
    U l = state(s, r, p, q);
    if (!l) {
        print(&uu, vv);
        g = q + p;
    } else {
        while (u >= l) {
            U o = read(&uu);
            u -= o;
            s += o;
            r -= o;
            if (s <= p && r >= 0) {
                write(vv, uu.idx);
                deidos(uu, u, vv, s, r, p, q);
                read(vv);
            }
            s -= o;
            r += o;
        }
    }
}

int main(int argc, char *argv[]) {

    printf("                                                                         \n");
    printf(" ,--.      o    |              ,---.                               |     \n");
    printf(" |   |,---..,---|,---.,---.    |    ,---..    ,,---.,---.,---.,---.|---  \n");
    printf(" |   ||---'||   ||   |`---.    |    |   | \\  / |---'|   |,---||   ||     \n");
    printf(" `--' `---'``---'`---'`---'    `---'`---'  `'  `---'`   '`---^`   '`---' \n");
    printf("                    `---'                             by Oscar Riveros \u2122 \n");
    printf("                                                                         \n");

    std::ifstream file(argv[1]);

    I len;
    file >> len;

    struct tape uu = {(U *)calloc(sizeof(U), len), 0, len};
    struct tape vv = {(U *)calloc(sizeof(U), len), 0, len};

    U s = 0, r = 0, t = 0, p = 0, q = 0, oo = 0, u = 0;

    file >> t;
    for (I i = 0; i < len; i++) {
        file >> u;
        write(&uu, u);
        oo += u;
    }

    file.close();

    list_3sort(uu.ram, uu.len);

    p = MAX(t, oo - t);
    q = MIN(t, oo - t);

    s = p;
    r = q;

    q = oo;
    p = oo;

    g = oo;
    c = 0;

    deidos(uu, oo, &vv, s, r, p, q);

    std::cout << "\nO(" << c << ")" << std::endl;

    return EXIT_SUCCESS;
}
