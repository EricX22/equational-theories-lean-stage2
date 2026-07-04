% order5_0020  eq1=26637 eq2=33766  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,X),f(Y,X)),f(X,Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,Y),f(Z,f(X,Y))),X) )).
