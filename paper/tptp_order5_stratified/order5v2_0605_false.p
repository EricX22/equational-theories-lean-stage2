% order5v2_0605  eq1=1715 eq2=27569  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(Z,W),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,f(Y,X)),Z),f(X,X)) )).
