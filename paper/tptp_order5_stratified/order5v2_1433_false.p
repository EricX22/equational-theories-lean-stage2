% order5v2_1433  eq1=13148 eq2=6011  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(X,f(W,X))),U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Y,f(Z,f(f(X,Z),W)))) )).
