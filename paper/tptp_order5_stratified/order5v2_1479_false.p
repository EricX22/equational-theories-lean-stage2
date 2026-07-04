% order5v2_1479  eq1=303 eq2=19715  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(f(Y,f(Z,X)),Z)) )).
