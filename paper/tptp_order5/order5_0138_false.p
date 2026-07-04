% order5_0138  eq1=50857 eq2=24742  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(X,W),X)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),W),f(f(X,W),Z)) )).
