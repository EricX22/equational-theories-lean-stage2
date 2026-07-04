% order5_0130  eq1=20967 eq2=42236  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(f(Z,W),Y),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(Z,f(Z,f(W,Z)))) )).
