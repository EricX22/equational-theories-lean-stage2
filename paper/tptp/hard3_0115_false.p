% hard3_0115  eq1=926 eq2=1502  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,X),f(Z,f(Y,X))) )).
