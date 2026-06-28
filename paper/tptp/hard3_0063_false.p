% hard3_0063  eq1=423 eq2=1070  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(X,f(Y,f(Z,Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(Y,f(Z,W)),W)) )).
