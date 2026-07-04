% order5v2_1399  eq1=11222 eq2=35058  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,f(X,Z)),f(W,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Z),f(f(X,Z),Y)),Z) )).
