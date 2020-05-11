///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef MIP_SOLVER_SIMPLEX_HH
#define MIP_SOLVER_SIMPLEX_HH

#include "utils.hh"

struct simplex {
    std::vector<std::vector<double>> table;
    std::vector<unsigned int> idx;
    std::deque<bool> flags;
    unsigned int vc{}, ec{}, sc{}, ac{};

    simplex(const unsigned int vc,
            const unsigned int ec,
            const unsigned int sc,
            const unsigned int ac
    ) {
        const unsigned int row = ec + 1;
        const unsigned int col = vc + sc + ac + 2;
        table.resize(row);
        for (auto &&it : table) {
            it.resize(col, 0.0);
        }
        idx.resize(ec);
        flags.resize(ec, false);
        this->vc = vc;
        this->ec = ec;
        this->sc = sc;
        this->ac = ac;
    }

    bool sl() {
        unsigned int simplex_column = vc + sc + ac;
        while (true) {
            unsigned int column_idx = 0;
            for (unsigned int j = 1; j <= simplex_column && column_idx == 0; ++j) {
                if (table[ec][j] < -EPS)
                    column_idx = j;
            }
            if (column_idx == 0) {
                return true;
            } else {
                unsigned int row_index = 0;
                double min = 0.0;
                unsigned int k = std::numeric_limits<unsigned int>::max();
                for (unsigned int i = 0; i < ec; ++i) {
                    if (table[i][column_idx] < EPS)
                        continue;
                    double temp = table[i][0] / table[i][column_idx];
                    if ((row_index == 0 || temp <= min) || (temp == min && idx[i] <= k)) {
                        min = temp;
                        row_index = i + 1;
                        k = idx[i];
                    }
                }
                if (row_index == 0) {
                    return false;
                } else {
                    row_index = row_index - 1;
                    {
                        double temp = table[row_index][column_idx];
                        idx[row_index] = column_idx - 1;
                        for (unsigned int j = 0; j <= simplex_column; ++j) {
                            table[row_index][j] /= temp;
                        }
                    }
                    {
                        for (unsigned int i = 0; i <= ec; ++i) {
                            if (i == row_index)
                                continue;
                            double temp = table[i][column_idx];
                            for (unsigned int j = 0; j <= simplex_column; ++j) {
                                table[i][j] -= temp * table[row_index][j];
                            }
                        }
                    }
                }
            }
        }
    }

    bool is() const { return (table[ec][0] >= -EPS); }
};

#endif // MIP_SOLVER_SIMPLEX_HH
