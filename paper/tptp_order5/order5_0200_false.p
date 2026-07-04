% order5_0200  eq1=56007 eq2=5950  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Y)) = f(f(Z,Y),f(X,Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(X,f(f(Z,Y),X)))) )).
