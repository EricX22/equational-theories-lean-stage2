% order5v2_1161  eq1=23627 eq2=48022  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),f(X,f(Z,Z))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(Y,f(X,X)),f(X,X)) )).
