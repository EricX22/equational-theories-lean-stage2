% hard3_0354  eq1=3360 eq2=379  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Y,f(Y,f(Z,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(X,Y),Z) )).
