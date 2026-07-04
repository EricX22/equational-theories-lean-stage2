% order5_0172  eq1=22261 eq2=3915  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(X,Y)),f(f(Y,X),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(X,f(X,X)),Y) )).
