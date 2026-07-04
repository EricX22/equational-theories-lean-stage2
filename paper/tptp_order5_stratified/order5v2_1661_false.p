% order5v2_1661  eq1=9643 eq2=37962  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,X),f(W,f(Y,Z)))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(W,W))),X),U) )).
