% order5v2_1674  eq1=36939 eq2=54570  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Z),f(X,W)),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(W,f(Y,f(X,Y))) )).
