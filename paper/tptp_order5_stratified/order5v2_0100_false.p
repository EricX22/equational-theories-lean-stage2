% order5v2_0100  eq1=26218 eq2=32171  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),Z)),f(W,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(f(X,f(Z,X)),W)),X) )).
