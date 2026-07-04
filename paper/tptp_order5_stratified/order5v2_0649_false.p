% order5v2_0649  eq1=23965 eq2=61001  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(U,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,X),Y) != f(f(Z,f(W,X)),Y) )).
