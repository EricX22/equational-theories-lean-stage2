% order5_0182  eq1=14724 eq2=4807  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,X),f(Z,Z)),X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(Y,f(Y,f(Z,f(X,W))))) )).
