% order5_0059  eq1=9281 eq2=6769  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(X,f(f(Y,Z),f(W,f(U,U)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(X,f(f(Z,Z),f(Z,Y)))) )).
