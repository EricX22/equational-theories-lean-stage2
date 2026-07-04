% order5_0158  eq1=32851 eq2=39176  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(f(f(Y,Y),X),Y)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(Y,X),f(Z,X)),X),Y) )).
