% order5v2_0784  eq1=31427 eq2=43855  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Y),f(Z,Z))),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(f(X,W),f(W,Y))) )).
