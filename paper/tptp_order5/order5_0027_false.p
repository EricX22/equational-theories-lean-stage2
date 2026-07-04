% order5_0027  eq1=43353 eq2=9354  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(f(X,Y),f(Z,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(X,Y),f(Z,f(W,Z)))) )).
