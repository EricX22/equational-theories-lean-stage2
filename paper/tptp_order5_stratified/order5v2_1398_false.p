% order5v2_1398  eq1=20153 eq2=53714  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(X,f(Z,Z)),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(f(f(Z,W),Y),U),Z) )).
