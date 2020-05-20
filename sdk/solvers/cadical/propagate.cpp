#include "internal.hpp"

namespace CaDiCaL {

/*------------------------------------------------------------------------*/

// We are using the address of 'decision_reason' as pseudo reason for
// decisions to distinguish assignment decisions from other assignments.
// Before we added chronological backtracking all learned units were
// assigned at decision level zero ('Solver.level == 0') and we just used a
// zero pointer as reason.  After allowing chronological backtracking units
// were also assigned at higher decision level (but with assignment level
// zero), and it was not possible anymore to just distinguish the case
// 'unit' versus 'decision' by just looking at the current level.  Both had
// a zero pointer as reason.  Now only units have a zero reason and
// decisions need to use the pseudo reason 'decision_reason'.

static Clause decision_reason_clause;
static Clause * decision_reason = &decision_reason_clause;

// If chronological backtracking is used the actual assignment level might
// be lower than the current decision level. In this case the assignment
// level is defined as the maximum level of the literals in the reason
// clause except the literal for which the clause is a reason.  This
// function determines this assignment level. For non-chronological
// backtracking as in classical CDCL this function always returns the
// current decision level, the concept of assignment level does not make
// sense, and accordingly this function can be skipped.

inline int Internal::assignment_level (int lit, Clause * reason) {

  assert (opts.chrono);
  if (!reason) return level;

  int res = 0;

  for (const auto & other : *reason) {
    if (other == lit) continue;
    assert (val (other));
    int tmp = var (other).level;
    if (tmp > res) res = tmp;
  }

  return res;
}

/*------------------------------------------------------------------------*/

inline void Internal::search_assign (int lit, Clause * reason) {

  if (level) require_mode (SEARCH);

  const int idx = vidx (lit);
  assert (!vals[idx]);
  assert (!flags (idx).eliminated () || reason == decision_reason);
  Var & v = var (idx);
  int lit_level;

  // The following cases are explained in the two comments above before
  // 'decision_reason' and 'assignment_level'.
  //
  if (!reason) lit_level = 0;   // unit
  else if (reason == decision_reason) lit_level = level, reason = 0;
  else if (opts.chrono) lit_level = assignment_level (lit, reason);
  else lit_level = level;
  if (!lit_level) reason = 0;

  v.level = lit_level;
  v.trail = (int) trail.size ();
  v.reason = reason;
  if (!lit_level) learn_unit_clause (lit);  // increases 'stats.fixed'
  const signed char tmp = sign (lit);
  vals[idx] = tmp;
  vals[-idx] = -tmp;
  assert (val (lit) > 0);
  assert (val (-lit) < 0);
  if (!searching_lucky_phases)
    phases.saved[idx] = tmp;                // phase saving during search
  trail.push_back (lit);
#ifdef LOGGING
  if (!lit_level) LOG ("root-level unit assign %d @ 0", lit);
  else LOG (reason, "search assign %d @ %d", lit, lit_level);
#endif

  if (watching ()) {
    const Watches & ws = watches (-lit);
    if (!ws.empty ()) {
      const Watch & w = ws[0];
      __builtin_prefetch (&w, 0, 1);
    }
  }
}

/*------------------------------------------------------------------------*/

// External versions of 'search_assign' which are not inlined.  They either
// are used to assign unit clauses on the root-level, in 'decide' to assign
// a decision or in 'analyze' to assign the literal 'driven' by a learned
// clause.  This happens far less frequently than the 'search_assign' above,
// which is called directly in 'propagate' below and thus is inlined.

void Internal::assign_unit (int lit) {
  assert (!level);
  search_assign (lit, 0);
}

// Just assume the given literal as decision (increase decision level and
// assign it).  This is used below in 'decide'.

void Internal::search_assume_decision (int lit) {
  require_mode (SEARCH);
  assert (propagated == trail.size ());
  level++;
  control.push_back (Level (lit, trail.size ()));
  LOG ("search decide %d", lit);
  search_assign (lit, decision_reason);
}

void Internal::search_assign_driving (int lit, Clause * c) {
  require_mode (SEARCH);
  search_assign (lit, c);
}

/*------------------------------------------------------------------------*/

// The 'propagate' function is usually the hot-spot of a CDCL SAT solver.
// The 'trail' stack saves assigned variables and is used here as BFS queue
// for checking clauses with the negation of assigned variables for being in
// conflict or whether they produce additional assignments.

// This version of 'propagate' uses lazy watches and keeps two watched
// literals at the beginning of the clause.  We also use 'blocking literals'
// to reduce the number of times clauses have to be visited (2008 JSAT paper
// by Chu, Harwood and Stuckey).  The watches know if a watched clause is
// binary, in which case it never has to be visited.  If a binary clause is
// falsified we continue propagating.

// Finally, for long clauses we save the position of the last watch
// replacement in 'pos', which in turn reduces certain quadratic accumulated
// propagation costs (2013 JAIR article by Ian Gent) at the expense of four
// more bytes for each clause.

bool Internal::propagate () {

  if (level) require_mode (SEARCH);
  assert (!unsat);

  START (propagate);

  // Updating statistics counter in the propagation loops is costly so we
  // delay until propagation ran to completion.
  //
  int64_t before = propagated;

  int old_trail_top = 0;
  Clause* old_trail_reason = 0;
  bool break_outer = false;
  if (save_trail && !opts.chrono) {
    if (old_trail_qhead != -1) {
      old_trail_top = old_trail[old_trail_qhead];
      old_trail_reason = old_trail_reasons[old_trail_qhead];
    }
  }
  
  while (!conflict && propagated != trail.size ()) {

    const int lit = -trail[propagated++];
    LOG ("propagating %d", -lit);
    
    if (save_trail && !opts.chrono) {
      if (old_trail_qhead != -1 && /*old_trail_top == -lit && old_trail_reason == 0*/ old_trail_top != 0 && val(old_trail_top) > 0) {
        old_trail_qhead--;
        if (old_trail_qhead != -1) {
          old_trail_top = old_trail[old_trail_qhead];
          old_trail_reason = old_trail_reasons[old_trail_qhead];
        }
        while (old_trail_qhead != -1 && old_trail_reason != 0 /*&& !(old_trail_reason->garbage)*/) {
          if (val(old_trail_top) < 0) {
            if (old_trail_reason->size > 10) break;
            //if (old_trail_reason->used <= 0 && !(old_trail_reason->keep) && old_trail_reason->glue > 5) break;
            conflict = old_trail_reason;
            /*literal_iterator lits = conflict->begin ();
             literal_iterator end = conflict->end ();
             printf("CONFLICT: ");
             while (lits != end) {
             printf("%d", lits);
             lits++;
             }
             printf("\n");*/
            break_outer = true;
            clear_old_trail();
            break;
          }
          else if (val(old_trail_top) == 0) {
            if (level == 0) {
              //if (old_trail_top == 859) {
              //printf("Here %d %d\n", old_trail_reason, old_trail_reason == decision_reason);
              //literal_iterator lits = old_trail_reason->begin ();
              //literal_iterator end = old_trail_reason->end ();
              //printf("[%d] REASON: ", old_trail_reason->garbage);
              /*while (lits != end) {
               printf("%d ", lits);
               lits++;
               }*/
              //for (auto lits: * old_trail_reason) {
              //printf("%d ", lits);
              //}
              //printf("\n");
              //}
              assign_unit(old_trail_top);
              //printf("Restoring: %d\n", old_trail_top);
            }
            else {
              //if (old_trail_top == 859) {
              //printf("Here %d %d\n", old_trail_reason, old_trail_reason == decision_reason);
              //literal_iterator lits = old_trail_reason->begin ();
              //literal_iterator end = old_trail_reason->end ();
              //printf("[%d] REASON: ", old_trail_reason->garbage);
              /*while (lits != end) {
               printf("%d ", lits);
               lits++;
               }*/
              //for (auto lits: * old_trail_reason) {
              //printf("%d ", lits);
              //}
              //printf("\n");
              //}
              if (old_trail_reason->size > 10) break;
              //if (old_trail_reason->used <= 0 && !(old_trail_reason->keep) && old_trail_reason->glue > 5 ) break;
              search_assign(old_trail_top, old_trail_reason);
              saved_lits++;
              //printf("Restoring: %d\n", old_trail_top);
            }
          }
          old_trail_qhead--;
          if (old_trail_qhead != -1) {
            old_trail_top = old_trail[old_trail_qhead];
            old_trail_reason = old_trail_reasons[old_trail_qhead];
          }
        }
        if (break_outer) break;
      }
      //not sure if below is needed
      if (old_trail_qhead == -1 || val(old_trail[old_trail_qhead]) < 0) {
        clear_old_trail();
      }
    }
    
    Watches & ws = watches (lit);

    const const_watch_iterator eow = ws.end ();
    const_watch_iterator i = ws.begin ();
    watch_iterator j = ws.begin ();

    while (i != eow) {

      const Watch w = *j++ = *i++;
      const signed char b = val (w.blit);

      if (b > 0) continue;                // blocking literal satisfied

      if (w.binary ()) {

        // In principle we can ignore garbage binary clauses too, but that
        // would require to dereference the clause pointer all the time with
        //
        // if (w.clause->garbage) { j--; continue; } // (*)
        //
        // This is too costly.  It is however necessary to produce correct
        // proof traces if binary clauses are traced to be deleted ('d ...'
        // line) immediately as soon they are marked as garbage.  Actually
        // finding instances where this happens is pretty difficult (six
        // parallel fuzzing jobs in parallel took an hour), but it does
        // occur.  Our strategy to avoid generating incorrect proofs now is
        // to delay tracing the deletion of binary clauses marked as garbage
        // until they are really deleted from memory.  For large clauses
        // this is not necessary since we have to access the clause anyhow.
        //
        // Thanks go to Mathias Fleury, who wanted me to explain why the
        // line '(*)' above was in the code. Removing it actually really
        // improved running times and thus I tried to find concrete
        // instances where this happens (which I found), and then
        // implemented the described fix.

        // Binary clauses are treated separately since they do not require
        // to access the clause at all (only during conflict analysis, and
        // there also only to simplify the code).

        if (b < 0) conflict = w.clause;          // but continue ...
        else search_assign (w.blit, w.clause);

      } else {

        if (conflict) break; // Stop if there was a binary conflict already.

        // The cache line with the clause data is forced to be loaded here
        // and thus this first memory access below is the real hot-spot of
        // the solver.  Note, that this check is positive very rarely and
        // thus branch prediction should be almost perfect here.

        if (w.clause->garbage) { j--; continue; }

        literal_iterator lits = w.clause->begin ();

        // Simplify code by forcing 'lit' to be the second literal in the
        // clause.  This goes back to MiniSAT.  We use a branch-less version
        // for conditionally swapping the first two literals, since it
        // turned out to be substantially faster than this one
        //
        //  if (lits[0] == lit) swap (lits[0], lits[1]);
        //
        // which achieves the same effect, but needs a branch.
        //
        const int other = lits[0]^lits[1]^lit;
        lits[0] = other, lits[1] = lit;

        const signed char u = val (other); // value of the other watch

        if (u > 0) j[-1].blit = other; // satisfied, just replace blit
        else {

          // This follows Ian Gent's (JAIR'13) idea of saving the position
          // of the last watch replacement.  In essence it needs two copies
          // of the default search for a watch replacement (in essence the
          // code in the 'if (v < 0) { ... }' block below), one starting at
          // the saved position until the end of the clause and then if that
          // one failed to find a replacement another one starting at the
          // first non-watched literal until the saved position.

          const int size = w.clause->size;
          const literal_iterator middle = lits + w.clause->pos;
          const const_literal_iterator end = lits + size;
          literal_iterator k = middle;

          // Find replacement watch 'r' at position 'k' with value 'v'.

          int r = 0;
          signed char v = -1;

          while (k != end && (v = val (r = *k)) < 0)
            k++;

          if (v < 0) {  // need second search starting at the head?

            k = lits + 2;
            assert (w.clause->pos <= size);
            while (k != middle && (v = val (r = *k)) < 0)
              k++;
          }

          w.clause->pos = k - lits;  // always save position

          assert (lits + 2 <= k), assert (k <= w.clause->end ());

          if (v > 0) {

            // Replacement satisfied, so just replace 'blit'.

            j[-1].blit = r;

          } else if (!v) {

            // Found new unassigned replacement literal to be watched.

            LOG (w.clause, "unwatch %d in", lit);

            lits[1] = r;
            *k = lit;
            watch_literal (r, lit, w.clause);

            j--;  // Drop this watch from the watch list of 'lit'.

          } else if (!u) {

            assert (v < 0);

            // The other watch is unassigned ('!u') and all other literals
            // assigned to false (still 'v < 0'), thus we found a unit.
            //
            search_assign (other, w.clause);

            // Similar code is in the implementation of the SAT'18 paper on
            // chronological backtracking but in our experience, this code
            // first does not really seem to be necessary for correctness,
            // and further does not improve running time either.
            //
            if (opts.chrono > 1) {

              const int other_level = var (other).level;

              if (other_level > var (lit).level) {

                // The assignment level of the new unit 'other' is larger
                // than the assignment level of 'lit'.  Thus we should find
                // another literal in the clause at that higher assignment
                // level and watch that instead of 'lit'.

                assert (size > 2);
                assert (lits[0] == other);
                assert (lits[1] == lit);

                int pos, s = 0;

                for (pos = 2; pos < size; pos++)
                  if (var (s = lits[pos]).level == other_level)
                    break;

                assert (s);
                assert (pos < size);

                LOG (w.clause, "unwatch %d in", lit);
                lits[pos] = lit;
                lits[1] = s;
                watch_literal (s, other, w.clause);

                j--;  // Drop this watch from the watch list of 'lit'.
              }
            }
          } else {

            assert (u < 0);
            assert (v < 0);

            // The other watch is assigned false ('u < 0') and all other
            // literals as well (still 'v < 0'), thus we found a conflict.

            conflict = w.clause;
            break;
          }
        }
      }
    }

    if (j != i) {

      while (i != eow)
        *j++ = *i++;

      ws.resize (j - ws.begin ());
    }
  }

  if (searching_lucky_phases) {

    if (conflict)
      LOG (conflict, "ignoring lucky conflict");

  } else {

    // Avoid updating stats eagerly in the hot-spot of the solver.
    //
    stats.propagations.search += propagated - before;

    if (!conflict) no_conflict_until = propagated;
    else {

      if (stable) stats.stabconflicts++;
      stats.conflicts++;

      LOG (conflict, "conflict");

      // The trail before the current decision level was conflict free.
      //
      no_conflict_until = control[level].trail;
    }
  }

  if (!conflict && save_trail && !opts.chrono) {
    old_trail_top = 0;
    old_trail_reason = 0;
    int levels_ahead = 0;
    int zz = old_trail_qhead;
    if (zz != -1) {
      old_trail_top = old_trail[zz];
      old_trail_reason = old_trail_reasons[zz];
    }
    if (zz != -1 && old_trail_reason == 0 && val(old_trail_top) == 0) {
      levels_ahead++;
      while (levels_ahead < 3 && val(old_trail_top) >= 0 && zz != -1) {
        zz--;
        if (zz != -1) {
          old_trail_top = old_trail[zz];
          old_trail_reason = old_trail_reasons[zz];
        }
        if (old_trail_reason == 0 && val(old_trail_top) == 0) {
          levels_ahead++;
        }
      }
      if (val(old_trail_top) < 0 && old_trail_reason != 0) {
        //printf("levels_ahead %d\n", levels_ahead);
        force_dec = true;
      }
    }
  }
  
  STOP (propagate);

  return !conflict;
}

}