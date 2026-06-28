% hard3_0196  eq1=1806 eq2=545  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,X),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Z,f(X,f(Z,X)))) )).
