% order5v2_1122  eq1=12178 eq2=37159  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Z),f(Y,Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,f(X,f(Y,X))),X),X) )).
