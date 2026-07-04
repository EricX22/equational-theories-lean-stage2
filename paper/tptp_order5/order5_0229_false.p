% order5_0229  eq1=21693 eq2=42736  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(X,Z)),f(W,f(Y,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(Z,f(f(W,X),Z))) )).
