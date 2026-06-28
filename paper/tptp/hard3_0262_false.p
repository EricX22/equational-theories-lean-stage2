% hard3_0262  eq1=2492 eq2=4149  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),W)),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(X,Z),W),X) )).
