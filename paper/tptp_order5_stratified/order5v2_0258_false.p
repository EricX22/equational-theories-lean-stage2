% order5v2_0258  eq1=23598 eq2=57301  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(W,f(Y,Z))) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( f(X,f(Y,Z)) != f(f(W,f(U,W)),V) )).
