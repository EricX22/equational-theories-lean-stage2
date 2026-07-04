% order5v2_0179  eq1=22672 eq2=20265  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(f(X,Z),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Z),f(f(Z,f(X,X)),Z)) )).
