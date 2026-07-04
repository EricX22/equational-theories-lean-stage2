% order5v2_1637  eq1=11374 eq2=58386  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(X,Z)),f(X,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,X),Y) != f(Z,f(W,f(W,Z))) )).
