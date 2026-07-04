% order5v2_1364  eq1=9675 eq2=51568  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(X,f(W,Y)))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(Y,Y),f(X,X)),Y) )).
