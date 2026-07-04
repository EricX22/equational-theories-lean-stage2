% order5_0013  eq1=12723 eq2=38148  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,f(X,Z))),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,f(f(Y,Z),X)),X),Y) )).
