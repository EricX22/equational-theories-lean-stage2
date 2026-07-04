% order5v2_0941  eq1=9359 eq2=5301  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,Z),f(X,f(X,Z)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(Y,f(Y,f(Y,W))))) )).
