% hard3_0289  eq1=2693 eq2=422  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Z,W)),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(X,f(Y,f(Z,X)))) )).
