% order5v2_0385  eq1=31425 eq2=18317  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,Y),f(Z,Z))),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Y),f(Z,f(f(Z,Y),Y))) )).
