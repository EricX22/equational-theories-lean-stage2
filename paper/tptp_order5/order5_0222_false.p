% order5_0222  eq1=8076 eq2=7722  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(X,Z)),U))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(f(Y,f(X,Y)),Z))) )).
