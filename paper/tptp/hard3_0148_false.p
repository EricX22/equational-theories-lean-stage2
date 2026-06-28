% hard3_0148  eq1=1217 eq2=2056  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,U)),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,Y),X),f(Z,X)) )).
