% order5_0137  eq1=15668 eq2=56607  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,f(Z,Y)),Y),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,Y)) != f(f(Z,f(Z,Z)),Y) )).
