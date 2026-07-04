% order5_0188  eq1=35426 eq2=18776  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(X,Y)),f(Z,X)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,X),f(f(Y,Z),f(W,Z))) )).
