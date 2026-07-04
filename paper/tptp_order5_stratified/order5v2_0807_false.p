% order5v2_0807  eq1=13065 eq2=19713  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,f(Z,f(Z,W))),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(f(Y,f(Z,X)),X)) )).
