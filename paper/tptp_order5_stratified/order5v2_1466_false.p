% order5v2_1466  eq1=18597 eq2=16466  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(f(X,Z),Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(f(Y,X),Y),Z),X)) )).
