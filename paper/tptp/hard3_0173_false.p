% hard3_0173  eq1=1539 eq2=524  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(Y,X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(Z,f(Y,X)))) )).
