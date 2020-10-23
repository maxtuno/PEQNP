///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   Without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

#ifndef MIP_SOLVER_MIP_HH
#define MIP_SOLVER_MIP_HH

#include "result.hh"
#include "simplex.hh"

class pixie {
private:
    unsigned int vc{};
    unsigned int ec{};
    std::vector<double> obj;
    std::vector<std::vector<double>> ll;
    std::vector<C> cc;
    std::vector<double> rr;
    std::deque<bool> ints;

    std::tuple<unsigned int, unsigned int> sv() const {
        auto st = 0, at = 0;
        for (unsigned int i = 0; i < ec; ++i) {
            if (cc[i] == C::E) {
                ++at;
            } else {
                ++st;
                if ((rr[i] < 0.0 && cc[i] == C::L) || (rr[i] >= 0.0 && cc[i] == C::G)) {
                    ++at;
                }
            }
        }
        return std::make_tuple(st, at);
    }

    simplex mt(const unsigned int st, const unsigned int at) const {
        simplex sm(vc, ec, st, at);
        auto idx = vc + 1;
        for (unsigned int i = 0; i < ec; ++i) {
            sm.table[i][0] = rr[i];
            for (unsigned int j = 0; j < vc; ++j) {
                sm.table[i][j + 1] = ll[i][j];
            }
            if (sm.table[i][0] < 0.0) {
                for (unsigned int j = 0; j <= vc; ++j) {
                    sm.table[i][j] = -sm.table[i][j];
                }
            }
            if (cc[i] != C::E) {
                if ((rr[i] < 0.0 && cc[i] == C::L) || (rr[i] >= 0.0 && cc[i] == C::G)) {
                    sm.table[i][idx] = -1.0;
                } else {
                    sm.table[i][idx] = 1.0;
                    sm.idx[i] = idx - 1;
                }
                ++idx;
            }
        }
        for (unsigned int i = 0; i < ec; ++i) {
            if ((rr[i] < 0.0 && cc[i] != C::G) || (rr[i] >= 0.0 && cc[i] != C::L)) {
                sm.table[i][idx] = 1.0;
                sm.idx[i] = idx - 1;
                sm.flags[i] = true;
                ++idx;
            }
        }
        if (at == 0) {
            for (unsigned int i = 0; i < vc; ++i) {
                sm.table[ec][i + 1] = -obj[i];
            }
        } else {
            for (unsigned int i = 0; i < ec; ++i) {
                if (!sm.flags[i])
                    continue;
                for (unsigned int j = 0; j <= vc + st; ++j) {
                    sm.table[ec][j] -= sm.table[i][j];
                }
            }
        }
        return sm;
    }

    void cz(const unsigned int &st, simplex &sm) const noexcept {
        for (unsigned int j = 0; j <= vc + st; ++j) {
            sm.table[ec][j] = 0.0;
            if (1 <= j && j <= vc) {
                sm.table[ec][j] = -obj[j - 1];
            }
            for (unsigned int i = 0; i < ec; ++i) {
                if (sm.idx[i] < vc) {
                    sm.table[ec][j] += obj[sm.idx[i]] * sm.table[i][j];
                } else if (sm.idx[i] < vc + st) {

                } else {
                    sm.table[ec][j] += (-1.0) * sm.table[i][j];
                }
            }
        }
    }

    void sb(const unsigned int &index, const double &border, const C &mode) {
        ++ec;
        std::vector<double> temp(vc, 0.0);
        temp[index] = 1.0;
        ll.push_back(temp);
        cc.push_back(mode);
        if (mode == C::L) {
            rr.push_back(floor(border));
        } else {
            rr.push_back(ceil(border));
        }
    }

    result po() const {
        result result(vc);
        size_t sc, ac;
        std::tie(sc, ac) = sv();
        auto sm = mt(sc, ac);
        if (ac > 0) {
            if (!sm.sl()) {
                return result;
            }
            if (!sm.is()) {
                return result;
            }
            cz(sc, sm);
            sm.ac = 0;
            if (!sm.sl()) {
                return result;
            }
        } else {
            if (!sm.sl()) {
                return result;
            }
        }
        result.z = sm.table[ec][0];
        for (size_t i = 0; i < ec; ++i) {
            if (sm.idx[i] < vc) {
                result.x[sm.idx[i]] = sm.table[i][0];
            }
        }
        if (result.z >= std::numeric_limits<double>::max()) {
            result.z = -std::numeric_limits<double>::max();
        }
        return result;
    }

    result optimize(const result &lb) {
        result pr = po();
        if (pr.z < lb.z) {
            return lb;            
        }
        size_t idx = 0;
        for (size_t i = 0; i < vc; ++i) {
            if (ints[i] && !ii(pr.x[i])) {
                idx = i + 1;
                auto br{*this};
                br.sb(idx - 1, pr.x[idx - 1], C::L);         
                sb(idx - 1, pr.x[idx - 1], C::G);    
                return optimize(br.optimize(lb));
            }
        }
        return pr;
    }

public:
    pixie() = default;

    void set_integer_condition(const std::vector<bool> &integers) {
        ints.assign(integers.begin(), integers.end());
    }

    void add_constraint(const std::vector<double> &constraint, const std::string &comparator, const double &right) {
        ll.push_back(constraint);
        if (comparator == "<=") {
            cc.push_back(C::L);
        } else if (comparator == ">=") {
            cc.push_back(C::G);
        } else if (comparator == "==") {
            cc.push_back(C::E);
        }
        rr.push_back(right);
        ec++;
    }

    result optimize() {
        result result(vc);
        return optimize(result);
    }

    void add_objective(const std::vector<double> &objective) {
        obj = objective;
        vc = objective.size();
    }

    //! Show contents
    void put(char *lp_path) const noexcept {
        std::ofstream lp_file(lp_path);
        lp_file << "max: ";
        for (unsigned i = 0; i < vc; ++i) {
            lp_file << (obj[i] >= 0? "+" + std::to_string(std::abs(obj[i])) : "-" + std::to_string(std::abs(obj[i]))) << " * x" << (i + 1) << " ";
        }
        lp_file << ";" << std::endl;
        for (unsigned i = 0; i < ec; ++i) {
            for (unsigned j = 0; j < vc; ++j) {
                if (ll[i][j] != 0.0) {
                    lp_file << (ll[i][j] >= 0? "+" + std::to_string(std::abs(ll[i][j])) : "-" + std::to_string(std::abs(ll[i][j]))) << " * x" << (j + 1) << " ";
                }
            }
            std::string tt{"<> "};
            lp_file << tt[static_cast<unsigned int>(cc[i])] << "= ";
            lp_file << (rr[i] >= 0? "+" + std::to_string(std::abs(rr[i])) : "-" + std::to_string(std::abs(rr[i]))) << "; \n";
        }
        for (unsigned i = 0; i < vc; ++i) {
            if (ints[i]) {
                lp_file << "int " << "x" << (i + 1) << ";" << std::endl;
            }
        }
        lp_file << std::endl;

        lp_file.close();
    }
};

#endif // MIP_SOLVER_MIP_HH
