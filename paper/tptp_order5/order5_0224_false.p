% order5_0224  eq1=23182 eq2=61799  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,Y),X),f(Y,f(Z,Z))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,X),Y) != f(f(f(Y,Y),X),X) )).
