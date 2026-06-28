% hard3_0218  eq1=2059 eq2=462  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),X),f(Z,W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(X,f(Y,f(Z,f(W,U)))) )).
