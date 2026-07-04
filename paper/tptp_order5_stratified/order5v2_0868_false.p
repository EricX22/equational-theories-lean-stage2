% order5v2_0868  eq1=30020 eq2=20027  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,f(Y,Y)))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Y),f(f(Y,f(Z,W)),X)) )).
