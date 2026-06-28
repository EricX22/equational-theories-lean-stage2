% hard3_0347  eq1=3277 eq2=4440  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Z,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,X)) != f(f(X,Z),Z) )).
