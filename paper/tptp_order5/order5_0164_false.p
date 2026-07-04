% order5_0164  eq1=38121 eq2=8003  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,f(f(Y,Y),Y)),X),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Z,f(f(Z,f(Y,X)),Y))) )).
