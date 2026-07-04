% order5v2_0873  eq1=37571 eq2=59861  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(Y,f(Y,Z))),W),U) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(W,f(f(Z,X),U)) )).
