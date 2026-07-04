% order5v2_0200  eq1=50282 eq2=4639  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,f(U,W))),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),X) != f(f(Y,Z),Y) )).
