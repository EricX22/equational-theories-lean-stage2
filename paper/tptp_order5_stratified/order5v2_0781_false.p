% order5v2_0781  eq1=17302 eq2=17899  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,f(X,Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,X),f(Y,f(f(Z,W),Z))) )).
