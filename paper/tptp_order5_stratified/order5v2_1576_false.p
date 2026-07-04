% order5v2_1576  eq1=19861 eq2=4853  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Y,f(Y,Z)),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(Y,f(Z,f(Y,f(W,W))))) )).
