% order5_0100  eq1=37145 eq2=36292  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,f(X,f(X,X))),X),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(f(X,X),Y),f(Y,X)),X) )).
