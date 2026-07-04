% order5v2_1266  eq1=37717 eq2=49965  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(X,W))),W),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,f(X,f(Z,Y))),X) )).
