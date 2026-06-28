% hard3_0124  eq1=1014 eq2=1577  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,Z),f(Y,f(Z,X))) )).
