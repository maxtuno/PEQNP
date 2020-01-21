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

namespace peqnp::science {

    template<typename R>
    class pixie {
    private:
        unsigned int vc{};
        unsigned int ec{};
        std::vector<R> obj;
        std::vector<std::vector<R>> ll;
        std::vector<C> cc;
        std::vector<R> rr;
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

        simplex<R> mt(const unsigned int st, const unsigned int at) const {
            simplex<R> sm(vc, ec, st, at);
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

        void cz(const unsigned int &st, simplex<R> &sm) const noexcept {
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

        void sb(const unsigned int &index, const R &border, const C &mode) {
            ++ec;
            std::vector<R> temp(vc, 0.0);
            temp[index] = 1.0;
            ll.push_back(temp);
            cc.push_back(mode);
            if (mode == C::L) {
                rr.push_back(floor(border));
            } else {
                rr.push_back(ceil(border));
            }
        }

        result<R> po() const {
            result<R> result(vc);
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
            if (result.z >= std::numeric_limits<R>::max()) {
                result.z = -std::numeric_limits<R>::max();
            }
            return result;
        }

        result<R> optimize(const result<R> &lb) {
            result<double> pr = po();
            if (pr.z < lb.z) {
                return lb;
            } else if (pr.z > lb.z) {
                size_t idx = 0;
                for (size_t i = 0; i < vc; ++i) {
                    if (ints[i] && !ii<R>(pr.x[i])) {
                        idx = i + 1;
                        auto p_l{*this};
                        p_l.sb(idx - 1, pr.x[idx - 1], C::L);
                        auto ub = p_l.optimize(lb);
                        auto p_r{*this};
                        p_r.sb(idx - 1, pr.x[idx - 1], C::G);
                        return p_r.optimize(ub);
                    }
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
            } else if (comparator == "==") {
                cc.push_back(C::E);
            } else if (comparator == ">=") {
                cc.push_back(C::G);
            }
            rr.push_back(right);
            ec++;
        }

        result<R> optimize() {
            result<R> result(vc);
            return optimize(result);
        }

        void add_objective(const std::vector<double> &objective) {
            obj = objective;
            vc = objective.size();
        }
    };
} // namespace peqnp::science

#endif // MIP_SOLVER_MIP_HH
